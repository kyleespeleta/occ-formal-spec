# Operator Closure Constraint (OCC): Formal Specification and Falsification Protocol

**Author:** Kyle Espeleta  
**Contact:** closure.rate@pm.me  
**Status:** Preprint  
**Revision:** 2025-12-20  

**Zenodo DOIs (canonical; always resolve to latest versions):**  
- Document 1 — OCC: The First Principle: https://doi.org/10.5281/zenodo.17973989  
- Document 2 — OCC: Formal Specification and Falsification Protocol: https://doi.org/10.5281/zenodo.17980647  
- Document 3 — Closure-Pathogen Postulates (CHP): https://doi.org/10.5281/zenodo.17980809  
- Map — OCC Framework Map: https://doi.org/10.5281/zenodo.17994480  

## Abstract
Large-scale coordination often fails for a simple reason: the rate at which obligations are created can exceed the rate at which they can be settled *durably* under real accountability and challenge. This preprint formalizes that bottleneck as the Operator Closure Constraint (OCC), a domain-general constraint on consequence-bearing systems mediated by accountable, contestable human determinations. At any declared consequence boundary, durable settlement is bounded by a finite closure channel. When uncertainty-reduction demands persistently outpace effective closure capacity—under drift, opacity, coupling, or required fidelity—the unmet remainder is conserved in boundary accounting and reappears as measurable outputs: return-work (reopens/corrections), thickening delays and tails, displacement of obligations off-ledger or into adjacent ledgers/client burden, degradation of auditability or actuation, and hysteresis after saturation. This repository hosts the canonical preprint and supporting materials.

## Paper
- `OCC_Formal_Spec_and_Falsification_Protocol.pdf`  
- How to test: [HOW_TO_TEST.md](HOW_TO_TEST.md)

## Reproducible tests
- EOIR executed case (Tier 1): [tests/eoir/RESULTS.md](tests/eoir/RESULTS.md)

## What this is
This repository provides the **canonical technical specification** of OCC:
- Operational definitions (loop boundary, closure, durable settlement with reopen horizon \(T\))
- Observable closure accounting (initiation, attempted closure, return-work, durable settlement, debt stocks)
- Mechanism specification (finite channel; allocation under drift; throughput–fidelity overshoot; displacement as explicit pathway; auditability/actuation limits; hysteresis)
- Explicit disconfirmation criteria and an adversarial empirical test charter
- Tiered claim discipline (Tier 0/1/2/2.5/3/H) with a hard non-circularity constraint

## What this is not
- Not a point-forecasting model
- Not a universal parameter set
- Not a “physics of society”
- Not a claim that automation eliminates the constraint (it can shift where the binding interface sits)

## How to cite
**Suggested citation:**
> Espeleta, Kyle. *Operator Closure Constraint (OCC): Formal Specification and Falsification Protocol.* Preprint, 2025. https://doi.org/10.5281/zenodo.17980647

## Tool-use disclosure
Text-to-text generative AI was used to assist drafting and editing. The author reviewed and takes full responsibility for all content and references.

## License
**CC BY 4.0** (reuse permitted with attribution). See `LICENSE`.

## Repository structure
- `OCC_Formal_Spec_and_Falsification_Protocol.pdf` — the preprint
- `paper/` — (optional) source files / alternate formats
- `data/` — (optional) raw public datasets or download instructions
- `notebooks/` — (optional) reproducible analyses for public-domain stress tests
- `CHANGELOG.md` — revision notes by date

## Notes on versions
- Minor copyedits: update revision date only.
- Any semantic/mechanism change: log in `CHANGELOG.md` and tag a new release.

## Contact
For critique, replication attempts, counterexamples, or collaboration: **closure.rate@pm.me**


