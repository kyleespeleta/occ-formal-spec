# Operator Closure Constraint (OCC): Formal Specification and Falsification Protocol

**Author:** Kyle Espeleta  
**Contact:** closure.rate@pm.me  
**Status:** Preprint (arXiv submission in progress)  
**Revision:** 2025-12-17

## Abstract
Civilization-scale coordination faces a fundamental bottleneck: the finite rate at which human decision-makers can resolve uncertain, consequential tasks under contestability. This preprint formalizes this bottleneck as the Operator Closure Constraint (OCC), a domain-general constraint mechanism for consequence-bearing coordination systems. OCC states that durable settlement of obligations is bounded by a finite closure channel at the consequence interface. When required uncertainty reduction persistently exceeds this channel, the conserved remainder reappears as return-work (reopenings/corrections), tail thickening, off-ledger displacement, auditability/actuation collapse, and slow-variable hysteresis. This repository hosts the canonical technical preprint and supporting materials.

## Paper
- `OCC_Formal_Spec_and_Falsification_Protocol.pdf`
- - How to test: [HOW_TO_TEST.md](HOW_TO_TEST.md)

## What this is
This repository provides the **canonical technical specification** of OCC:
- Operational definitions (loop boundary, closure, durable settlement with reopen horizon \(T_r\))
- Observable closure accounting (initiation, attempted closure, return-work, durable settlement, debt stocks)
- Mechanism specification (finite channel, drift allocation, rate–distortion overshoot, displacement as state, auditability/actuation gate, hysteresis)
- Explicit falsification surfaces and an adversarial empirical test charter
- Tiered identifiability discipline (Tier 1/2/3) with a hard non-circularity constraint

## What this is not
- Not a point-forecasting model
- Not a universal parameter set
- Not a “physics of society”
- Not a claim that automation eliminates the constraint (it can shift the binding interface)

## How to cite
**Suggested citation (update DOI/URL when available):**
> Espeleta, Kyle. *Operator Closure Constraint (OCC): Formal Specification and Falsification Protocol.* Preprint, 2025. URL/DOI:(https://doi.org/10.5281/zenodo.17973990)

## Tool-use disclosure
Text-to-text generative AI was used to assist drafting and editing. The author reviewed and takes full responsibility for all content and references.

## License
This work is intended to be released under **CC BY 4.0** (reuse permitted with attribution). See `LICENSE`.

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

