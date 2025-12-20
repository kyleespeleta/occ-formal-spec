# DEFINITIONS LOCK (frozen meanings)

## Global OCC meanings
- Durable settlement: closure that does not reopen within declared horizon T via declared reopen channels R_T.
- Attempted closure μ_a(t): closures completed (attempts), regardless of durability.
- Durable settlement μ_d(t;T): closures that remain closed through horizon T.
- Durability fraction q(t;T): fraction of a cohort that remains closed through horizon T.
- Return-work / reopen: any declared channel that re-enters the boundary as attributable work after an attempt.

## Case: EOIR — Tier 1a

### Boundary B (LOCK)
- B = EOIR published annual caseflow ledger boundary as operationalized in EOIR “Pending Cases, New Cases, and Total Completions.”
- Boundary objects are defined by the ledger’s initiation and completion events and the published pending stock at fiscal year end.

### Obligation unit (LOCK)
- U = EOIR “case” as counted in the published annual ledger.
- Stability caveat: this deployment does not claim unit stability under splits/merges/reclassifications; residual checks partially bound obvious inconsistencies.

### Time step (LOCK)
- Δt = Annual (fiscal year).

### Horizon semantics (LOCK)
- No durability horizons are declared in this Tier 1a deployment.
- Reason: cohort durability q(t;T) is not measurable in annual ledgers; durable settlement μ_d(t;T) is out of scope.

### Reopen channels status (LOCK)
- Event-level reopen linkage is not available in annual ledgers.
- Therefore reopen channels are not enumerated as a complete set for q(t;T) construction.
- Motions-to-reopen are used only as a normalized pressure proxy, not as cohort return-work.

### OCC mapping at this boundary (LOCK)
- Initiation proxy: λ_exo(t) = EOIR “new cases” / receipts (annual).
- Attempted closure proxy: μ_a(t) = EOIR “total completions” (annual). This is a ledger-boundary attempted-closure proxy and is not restricted to merits determinations.
- Visible unresolved stock: L(t) = EOIR “pending cases” at fiscal year end.

### Rework-pressure proxy (LOCK; not cohort return-work)
- Motions-to-reopen per completion = (annual motions-to-reopen count) / (annual completions).
- This proxy is not q(t;T) and not generated return-work ρ_gen(t;T). It is a measurable reopen-pressure channel normalized by throughput without cohort attribution.

### Counting rule X (LOCK)
- X rule for return-work counting is NOT executed in this Tier 1a deployment because cohort linkage is unavailable.
- This deployment does not estimate ρ_nd or ρ_evt as reopen-attributable return-work.

### Tier claim (LOCK)
- Tier = 1a
- Limitation = no q(t;T), no μ_d

### Explicit out-of-scope (LOCK)
- Event-level reopen linkage and cohort tracking for q(t;T).
- Durable settlement μ_d(t;T) and realized durable outflow μ_d^real(t;T).
- Generated return-work ρ_gen(t;T), displacement accounting X(t), and total unresolved stock L_tot(t).
- Driver separation for drift V(t), coupling J(t), opacity M_0(t), or contestability regime Z(t) without additional instrumentation and precommitted design.
