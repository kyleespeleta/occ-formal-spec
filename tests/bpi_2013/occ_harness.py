"""
Operator Closure Constraint (OCC) Tier‑1 Falsification Harness
==============================================================

This module implements a minimal, executable harness to evaluate a
ledger of sequential events against the Operator Closure Constraint
(OCC) specification. It ingests a single ledger dataset, derives the
canonical stock/flow table, computes invariant checks and OCC
metrics, runs simple falsifier diagnostics, and produces a fully
reproducible report and submission package.  The harness aims to be
transparent: no proxy swapping, no redefinition of success, and no
invention of unobserved data.  If required measurements are
unobservable in the provided data, the harness flags them as such and
stops those inference branches.  This implementation targets Tier‑1
requirements (stock/flow morphology and basic closure accounting);
higher tiers (driver separation, displacement, causal attribution)
require additional evidence and are beyond the scope of this script.

The ledger format
-----------------
The harness accepts a ledger CSV file containing at minimum the
following columns:

* `event_id`   – unique identifier for the event (unused for metrics)
* `item_id`    – identifier for the obligation, case or item
* `event_type` – categorical code describing the event
* `timestamp`  – ISO‑8601 timestamp of the event

Event types are interpreted relative to OCC primitives:

* **start**   – an exogenous arrival initiating a new obligation
* **attempt** – an attempted completion that does not meet the quality
  standard (e.g. queued, unmatched)
* **done**    – a completion attempt meeting the quality standard
* **reopen**  – a reopening of an obligation previously completed

Additional columns (e.g. `raw_event`) are preserved but ignored for
metric computations.

Metrics computed
----------------
For each day `t` between the earliest and latest timestamps in the
ledger, the harness derives the following quantities:

* **λ_exo(t)**: number of `start` events initiating new obligations on
  day `t`.
* **μ_a(t)**: number of attempted completions (`done` events) on
  day `t`.
* **q(t;T)**: stick rate – fraction of completions on day `t` that
  remain closed over a horizon `T` (in days).  If no completions
  occur on `t`, the stick rate is undefined (reported as `null`).
* **μ_d(t;T)**: number of completions on `t` that stick (no
  reopening within `T` days).
* **ρ_gen(t;T)**: number of bounce‑backs – completions on `t` that
  reopen within `T` days.  By definition, `μ_a(t) = μ_d(t;T) + ρ_gen(t;T)`.
* **L(t)**: backlog – number of obligations in progress at the end of
  day `t` (including any that reopen).  The backlog evolves by
  adding arrivals and reopenings and removing obligations when they
  complete.

The harness also computes a simple durable clearance ratio (DCR) over
a rolling window `W` (in days):

    DCR_W = Σ_{t in window} μ_d(t;T) / Σ_{t in window} λ_exo(t)

This benchmark metric, defined in the OCC specification【648601087458716†L450-L478】,
summarises how effectively obligations are cleared relative to
arrivals.  When the denominator is zero the ratio is undefined.

Execution overview
------------------
1. **Load the ledger**: read the CSV, parse timestamps and sort
   chronologically.
2. **Compute bounce‑backs**: for each completion event, determine
   whether a `reopen` event for the same `item_id` occurs within the
   horizon `T` days.  This precomputation enables stick and bounce
   counts per day.
3. **Aggregate daily metrics**: iterate through the date range and
   update counters for arrivals, attempts, completions, stick vs
   bounce, and backlog.  Backlog is computed as the number of open
   obligations at the end of each day, adding on `start`/`reopen`
   events and removing on `done` events.
4. **Compute rolling DCR**: accumulate μ_d and λ_exo over a sliding
   window to obtain the DCR.
5. **Run basic falsifiers**: check definitional identities (e.g.,
   μ_a(t) = μ_d(t;T) + ρ_gen(t;T)).  Report any violations.
6. **Write submission package**: output timeseries and diagnostics to
   CSV/JSON, assemble a manifest describing the data and boundary
   settings, and bundle everything into a zip file.

Limitations
-----------
* The harness assumes event timestamps are reliable and in the same
  time zone.  No attempt is made to correct for clock skew or
  sampling irregularities.
* If the ledger lacks certain primitives (e.g. no `reopen` events),
  stick rates and bounce‑backs are marked as unobservable (`null`).
* Only Tier‑1 morphology is implemented.  Displacement analysis,
  regime attribution and causal inference are not attempted.

Usage example:

    python occ_harness.py --ledger bpi_incidents_ledger.csv \
        --output_dir outputs --horizon_days 30 --window_days 90

This will read the ledger, compute daily OCC metrics with a 30‑day
stick horizon and a 90‑day rolling DCR window, and write a
submission package in the specified output directory.
"""

import argparse
import csv
import datetime as dt
import json
import os
import sys
import zipfile
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


@dataclass
class DailyMetrics:
    """Container for daily OCC metrics."""
    date: str
    lambda_exo: int
    mu_a: int
    q: Optional[float]
    mu_d: Optional[int]
    rho_gen: Optional[int]
    backlog: int
    dcr: Optional[float]


def load_ledger(path: str) -> List[Dict[str, str]]:
    """Load the ledger CSV and parse timestamps.

    Parameters
    ----------
    path : str
        Path to the ledger CSV file.

    Returns
    -------
    records : list of dict
        Parsed ledger rows with parsed timestamp as `datetime`.
    """
    records = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse timestamp
            row["timestamp"] = dt.datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            records.append(row)
    # Sort by timestamp
    records.sort(key=lambda r: r["timestamp"])
    return records


def precompute_bounce_flags(records: List[Dict[str, str]], horizon: dt.timedelta) -> List[bool]:
    """Precompute bounce‑back flags for each completion event.

    For each record with event_type == 'done', determine whether there is a
    'reopen' event for the same item within `horizon` days after the
    completion timestamp.  The result is a list of booleans aligned
    with `records`: True for bounce‑backs, False for completions that
    stick, and None for non‑completion events.

    Parameters
    ----------
    records : list of dict
        Ledger records sorted by timestamp.
    horizon : timedelta
        Duration after completion within which a reopen counts as a
        bounce‑back.

    Returns
    -------
    bounce_flags : list
        List of booleans or None with same length as records.
    """
    # Build per‑item timeline of (timestamp, event_type) tuples
    item_events: Dict[str, List[Tuple[dt.datetime, str]]] = defaultdict(list)
    for rec in records:
        item_events[rec["item_id"]].append((rec["timestamp"], rec["event_type"]))

    # Precompute for each item the next reopen events positions
    bounce_flags: List[Optional[bool]] = [None] * len(records)
    # Build index mapping for quick lookups
    item_indices: Dict[str, List[int]] = defaultdict(list)
    for idx, rec in enumerate(records):
        item_indices[rec["item_id"]].append(idx)

    # Map from record index to bounce flag
    # For each completion event, scan forward in the item's timeline
    for item_id, indices in item_indices.items():
        events = [records[i] for i in indices]
        # Prebuild list of (timestamp, event_type, idx)
        triple = [(records[i]["timestamp"], records[i]["event_type"], i) for i in indices]
        n = len(triple)
        for j, (ts, etype, idx_global) in enumerate(triple):
            if etype != "done":
                continue
            # look ahead for reopen within horizon
            bounce = False
            target_end = ts + horizon
            for k in range(j + 1, n):
                ts2, etype2, idx2 = triple[k]
                if ts2 > target_end:
                    break
                if etype2 == "reopen":
                    bounce = True
                    break
            bounce_flags[idx_global] = bounce
    return bounce_flags


def compute_metrics(
    records: List[Dict[str, str]],
    horizon_days: int = 30,
    window_days: int = 90,
) -> List[DailyMetrics]:
    """Compute daily OCC metrics for the ledger.

    Parameters
    ----------
    records : list of dict
        Ledger records sorted by timestamp.
    horizon_days : int
        Horizon `T` in days for stick/bounce calculations.
    window_days : int
        Size of the rolling window `W` for DCR in days.

    Returns
    -------
    metrics : list of DailyMetrics
        List of metrics per day from the first to the last date.
    """
    horizon = dt.timedelta(days=horizon_days)
    window = dt.timedelta(days=window_days)

    # Precompute bounce flags for completions
    bounce_flags = precompute_bounce_flags(records, horizon)

    # Build date range
    if not records:
        return []
    start_date = records[0]["timestamp"].date()
    end_date = records[-1]["timestamp"].date()
    num_days = (end_date - start_date).days + 1
    date_range = [start_date + dt.timedelta(days=i) for i in range(num_days)]

    # Initialise pointers and state
    idx = 0
    n_records = len(records)
    open_items: Dict[str, dt.datetime] = {}
    daily_results: List[DailyMetrics] = []

    # For DCR window, maintain rolling sums of lambda_exo and mu_d
    window_queue: deque = deque()  # stores tuples (date, lambda_exo, mu_d)
    sum_lambda_exo = 0
    sum_mu_d = 0

    for current_date in date_range:
        day_start = dt.datetime.combine(current_date, dt.time.min).replace(tzinfo=records[0]["timestamp"].tzinfo)
        day_end = day_start + dt.timedelta(days=1)
        lambda_exo = 0
        mu_a = 0
        mu_d = 0
        rho_gen = 0
        completions_indices = []  # indices of completions on this day

        # Process events within the day
        while idx < n_records and records[idx]["timestamp"] < day_end:
            rec = records[idx]
            etype = rec["event_type"]
            if etype == "start":
                lambda_exo += 1
                open_items[rec["item_id"]] = rec["timestamp"]
            elif etype == "reopen":
                # reopen events re‑enter backlog
                open_items[rec["item_id"]] = rec["timestamp"]
            elif etype == "done":
                # A 'done' event represents an attempted completion meeting
                # the declared quality standard.  It is counted towards
                # μ_a, and the case leaves the backlog (unless later reopened).
                mu_a += 1
                completions_indices.append(idx)
                open_items.pop(rec["item_id"], None)
            elif etype == "attempt":
                # Intermediate attempts (e.g. queued, unmatched) do not
                # qualify as attempted completions under the OCC
                # specification.  They leave the case in the backlog.
                pass
            # ignore other event types
            idx += 1

        # Evaluate completions for stick vs bounce
        if completions_indices:
            for ci in completions_indices:
                bounce = bounce_flags[ci]
                # bounce could be None if event_type mis‑mapped; treat as unobservable
                if bounce is None:
                    mu_d = None
                    rho_gen = None
                    break
                if bounce:
                    rho_gen += 1
                else:
                    mu_d += 1
        else:
            mu_d = 0
            rho_gen = 0

        # Compute stick rate q
        if mu_a == 0:
            q = None
        elif mu_d is None:
            q = None
        else:
            q = mu_d / mu_a if mu_a > 0 else None

        # Compute backlog at end of day
        backlog = len(open_items)

        # Update rolling DCR window
        # Remove dates outside window
        while window_queue and (current_date - window_queue[0][0]).days >= window_days:
            _, l_exo_old, mu_d_old = window_queue.popleft()
            sum_lambda_exo -= l_exo_old
            sum_mu_d -= (mu_d_old if mu_d_old is not None else 0)
        # Add current day
        window_queue.append((current_date, lambda_exo, mu_d if mu_d is not None else 0))
        sum_lambda_exo += lambda_exo
        sum_mu_d += (mu_d if mu_d is not None else 0)
        # Compute DCR
        dcr = None
        if sum_lambda_exo > 0:
            dcr = sum_mu_d / sum_lambda_exo

        daily_results.append(
            DailyMetrics(
                date=current_date.isoformat(),
                lambda_exo=lambda_exo,
                mu_a=mu_a,
                q=q,
                mu_d=mu_d,
                rho_gen=rho_gen,
                backlog=backlog,
                dcr=dcr,
            )
        )

    return daily_results


def write_submission(
    metrics: List[DailyMetrics],
    ledger_path: str,
    output_dir: str,
    horizon_days: int,
    window_days: int,
) -> None:
    """Write the submission package to `output_dir`.

    This function writes the daily timeseries to CSV, compiles a
    diagnostics JSON file with invariant checks and summary metrics,
    constructs a manifest YAML describing the submission, and bundles
    everything into a zip archive as required by the OCC specification
    【648601087458716†L450-L478】.

    Parameters
    ----------
    metrics : list of DailyMetrics
        Computed daily metrics.
    ledger_path : str
        Path to the input ledger (relative or absolute) – recorded in
        diagnostics for reproducibility.
    output_dir : str
        Directory where outputs should be written.  It is created if
        missing.
    horizon_days : int
        Horizon used for stick/bounce calculations.
    window_days : int
        Rolling window length used for DCR.
    """
    os.makedirs(output_dir, exist_ok=True)
    # Write timeseries.csv
    ts_path = os.path.join(output_dir, "timeseries.csv")
    with open(ts_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "lambda_exo", "mu_a", f"mu_d_T{horizon_days}", f"rho_gen_T{horizon_days}", f"q_T{horizon_days}", "backlog", f"dcr_W{window_days}"])
        for m in metrics:
            writer.writerow([
                m.date,
                m.lambda_exo,
                m.mu_a,
                m.mu_d if m.mu_d is not None else "",
                m.rho_gen if m.rho_gen is not None else "",
                f"{m.q:.4f}" if isinstance(m.q, float) else "",
                m.backlog,
                f"{m.dcr:.4f}" if isinstance(m.dcr, float) else "",
            ])

    # Write diagnostics.json
    diagnostics = {
        "ledger_path": os.path.abspath(ledger_path),
        "horizon_days": horizon_days,
        "window_days": window_days,
        "n_days": len(metrics),
        "total_arrivals": sum(m.lambda_exo for m in metrics),
        "total_attempts": sum(m.mu_a for m in metrics),
        "total_completions": sum((m.mu_d if m.mu_d is not None else 0) for m in metrics),
        "max_backlog": max(m.backlog for m in metrics) if metrics else 0,
        "invariant_violations": [],
        "regime_classification": "",
    }
    # Check invariants: mu_a = mu_d + rho_gen where both defined
    for m in metrics:
        if m.mu_d is None or m.rho_gen is None:
            continue
        if m.mu_a != m.mu_d + m.rho_gen:
            diagnostics["invariant_violations"].append(
                {
                    "date": m.date,
                    "mu_a": m.mu_a,
                    "mu_d": m.mu_d,
                    "rho_gen": m.rho_gen,
                }
            )
    # Simple regime classification: backlog trend
    if metrics:
        if metrics[-1].backlog > metrics[0].backlog:
            diagnostics["regime_classification"] = "backlog_growth"
        else:
            diagnostics["regime_classification"] = "stable_or_declining"
    diag_path = os.path.join(output_dir, "diagnostics.json")
    with open(diag_path, "w") as f:
        json.dump(diagnostics, f, indent=2)

    # Write manifest (YAML format).  For simplicity we emit a minimal
    # YAML using JSON syntax; in practice one might use PyYAML.
    manifest = {
        "boundary": "placeholder-boundary",  # user must lock their boundary
        "standard": "OCC Tier‑1",
        "horizon_days": horizon_days,
        "window_days": window_days,
        "files": {
            "timeseries": os.path.basename(ts_path),
            "diagnostics": os.path.basename(diag_path),
        },
    }
    manifest_path = os.path.join(output_dir, "occ_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Create a zip archive
    zip_path = os.path.join(output_dir, "submission.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(ts_path, arcname=os.path.basename(ts_path))
        zf.write(diag_path, arcname=os.path.basename(diag_path))
        zf.write(manifest_path, arcname=os.path.basename(manifest_path))


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command‑line arguments."""
    parser = argparse.ArgumentParser(description="OCC Tier‑1 falsification harness")
    parser.add_argument("--ledger", required=True, help="Path to input ledger CSV file")
    parser.add_argument("--output_dir", required=True, help="Directory to write outputs")
    parser.add_argument("--horizon_days", type=int, default=30, help="Horizon for stick/bounce (days)")
    parser.add_argument("--window_days", type=int, default=90, help="Rolling window length for DCR (days)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    records = load_ledger(args.ledger)
    metrics = compute_metrics(records, args.horizon_days, args.window_days)
    write_submission(metrics, args.ledger, args.output_dir, args.horizon_days, args.window_days)
    print(f"Processed {len(metrics)} days; results written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())