# BPI 2013 Tier-1 OCC harness

This directory contains a fully reproducible Tier-1 execution of the Operator Closure Constraint (OCC) measurement primitives on the BPI Challenge 2013 incident log. The goal is instrumentation validity and conservation-identity verification, not causal attribution.

## Reproduce

From this directory:

```bash
make reproduce

If you are not using make, run:

./run.sh

Verify outputs

Verify that regenerated outputs match the published hashes:

sha256sum -c submission/CHECKSUMS.sha256

Included artifacts

This folder is expected to contain:
	•	raw/bpi_incidents_ledger.csv
	•	occ_harness.py
	•	run.sh
	•	Makefile
	•	README.md
	•	submission/RUNLOG.txt
	•	submission/pip_freeze.txt
	•	submission/CHECKSUMS.sha256

Tier-1 scope and definitions

Exogenous arrivals λ_exo(t) are defined as the first Accepted event for a case on day t. Attempted completions μ_a(t) are defined as Completed events on day t. Any Accepted event after the first is treated as a reopen event.

Durability is evaluated at horizon T = 30 days. Bounce-backs ρ_gen(t;T) are counted as completion attempts followed by a reopen within T. Durable completions μ_d(t;T) are completion attempts not followed by a reopen within T. The stick fraction q(t;T) is μ_d(t;T) / μ_a(t) when μ_a(t) > 0.

Tier-1 requires the daily conservation identity:

μ_a(t) = μ_d(t;T) + ρ_gen(t;T)

Backlog L(t) is defined as the stock of open cases in the event-log state machine. Durable Clearance Ratio DCR(t) is computed as a rolling window W = 90 days of durable completions divided by exogenous arrivals:

DCR(t) = (sum_{s=t-W+1}^{t} μ_d(s;T)) / (sum_{s=t-W+1}^{t} λ_exo(s))

Observability limits

Tier-1 does not attempt driver separation or causal attribution. Any information not contained in the ledger, including external quality standards beyond the Completed marker, staffing, policy changes, or exogenous drivers, is treated as unobservable and excluded.




