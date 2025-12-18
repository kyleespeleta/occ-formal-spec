# How to Test OCC

This is a minimal, reproducible testing workflow that does not require fitting the full dynamical model. Start with Tier 1. Only move to Tier 2/3 if the proxies exist.

## 0) Choose a domain that qualifies as an OCC loop
A domain qualifies if you can name all three in the system’s own language:

1) **Initiation event**: a countable “new obligation” enters the loop.  
2) **Settlement event**: a timestampable “resolved/closed” state exists.  
3) **Rework channel**: a counted pathway where “closed” can reopen, be corrected, be appealed, be remanded, be re-entered.

If you cannot identify all three, do not test OCC in that domain.

## 1) Freeze definitions before looking at outcomes
Write a one-page Domain Test Sheet (copy/paste template):

- D0 Domain and loop boundary  
- D1 Closure event definition  
- D2 λ_exo(t) definition  
- D3 μ_a(t) definition  
- D4 ρ(t) definition and reopen horizon T_r  
- D5 μ_d(t) = μ_a(t) − ρ(t)  
- D6 L(t) and age/aging proxy  
- D7 X(t) displacement proxy (if any)  
- D8 Tail metric definition (p90/p95 or proxy)  
- D9 Drift proxy V(t) (optional Tier 3)  
- D10 Coupling/opacity proxy J(t), M_0(t) (optional Tier 3)  
- D11 Verification budget proxy B(t) (optional Tier 3)  
- D12 Falsifiers you will treat as failures (F1–F3 style)

Do not change these after you compute the first plot.

## 2) Tier 1 test (observable-only). This is the default.
### 2.1 Required time series
Pick a uniform time step (weekly, monthly, quarterly). Build:

- **λ_exo(t)**: new obligations received
- **μ_a(t)**: attempted closures / disposals / completed actions
- **ρ(t)**: reopenings/appeals/corrections within T_r (or the best available proxy)
- **μ_d(t)**: durable settlement  
  μ_d(t) = μ_a(t) − ρ(t)
- **L(t)**: visible backlog / pending inventory
- **Tail proxy**: median duration, “% older than X,” or p90/p95 if available

### 2.2 Accounting sanity checks (must pass)
These are not model claims; they are data integrity checks.

1) **Event identity check**  
If you computed ρ and μ_a, verify:  
μ_d(t) = μ_a(t) − ρ(t)

2) **Stock–flow check at your chosen boundary**
If you have L (and X if available), verify the discrete approximation:
L_tot(t+1) ≈ L_tot(t) + λ_exo(t) − μ_d(t)

If it does not approximately hold, you either:
- mixed incompatible definitions, or
- the dataset changed definitions midstream, or
- the boundary is wrong.

Stop and fix before interpretation.

### 2.3 Minimal plots (Tier 1)
Make four plots over time:

1) λ_exo(t) and μ_d(t) on the same axes  
2) L(t) and an aging/tail proxy (e.g., median duration or % older than 1 year)  
3) μ_a(t) and μ_d(t) (the “hinge”)  
4) ρ(t) (return-work) and tail proxy

### 2.4 Tier-1 decision rule (what counts as an OCC signature)
OCC is supported (not proven) if you see:

- **Debt accumulation**: sustained λ_exo > μ_d and rising L or aging share  
- **Tail thickening**: tail proxy worsens as L grows  
- **Hinge signature**: μ_a rises or stays high while μ_d stalls/falls and ρ rises  
  (μ_a − μ_d = ρ by construction)

OCC is weakened if you see the wrong sign repeatedly:

- Under high apparent drift/complexity, compression/throughput pushes cause **ρ to fall** and tails to stabilize while μ_d rises, without displacement.

## 3) Tier 2 test (anti-cheat displacement)
Tier 2 asks: is “improvement” real closure or cost-shifting?

### 3.1 Add displacement proxy X(t) if possible
X can be approximated by any counted off-ledger channel:
- clock-paused statuses
- deflections to other queues
- abandonment/attrition that later re-enters
- external appeals that re-enter later

### 3.2 Tier 2 plots
- L(t), X(t), and L_tot(t) = L + X  
- δ(t) and ω(t) if you can approximate them  
- Compare “visible improvement” (L falling) vs “total debt” (L_tot stable/rising)

Tier 2 result: if L improves but X rises and later ω spikes with worse tails, that is displacement, not engineered closure.

## 4) Tier 3 test (driver separation: drift, coupling, auditability)
Only do Tier 3 if you have independent proxies. Do not use L, tails, or ρ as RHS drivers.

### 4.1 Add independent proxies
- V(t): drift proxy (rule changes, policy changes, guideline updates, input novelty)
- J(t): coupling proxy (handoffs, interfaces, dependencies)
- B(t): verification budget proxy (staffing, adjudicator hours, sitting days, audit staff)
- U(t): independent endogenous burden proxy (complaints, escalations, disputes, audits)

### 4.2 Test the nonstationarity claim (rate–distortion sign)
Define a compression proxy q(t) (deadlines, throughput targets, shortened reviews, reduced verification steps).
Then test:

When drift proxy V(t) is high:
- does increased compression q(t) predict higher ρ(t) and worse tails more often than improvement?

If the opposite holds reliably across multiple domains, OCC’s nonstationarity trap is weakened.

## 5) Minimal falsifiers (what would force revision)
Treat these as failures if observed cleanly in multiple independent domains:

- **F1 Nonstationarity sign failure**: under high drift, compression reliably reduces ρ and improves tails while μ_d rises, without displacement.
- **F2 Auditability cliff failure**: opacity rises beyond auditability proxies with no increase in delay/shielding and no increase in downstream correction burden.
- **F3 Hysteresis failure**: after prolonged overload, forcing drops and the system reliably returns to baseline tails/aging without structural change.

## 6) What to publish as “a test”
For a publishable, auditable test, include:
- the frozen Domain Test Sheet
- the raw source links and the raw files (or exact download steps)
- the code that builds λ, μ_a, ρ, μ_d, L, tails
- the four Tier-1 plots
- the accounting sanity checks and any definition breaks

## 7) Quick start domain suggestion
Pick a domain where receipts, disposals, backlog, and an aging/tail proxy are already published on a regular cadence. That lets you complete Tier 1 in a single sitting and produce interpretable figures without hand-waving.
