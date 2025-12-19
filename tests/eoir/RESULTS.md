# EOIR executed case (Tier 1): receipts, completions, pending stock, and rework-pressure proxy

This page documents an executed Tier 1 OCC test on U.S. immigration courts (EOIR) using EOIR-published annual ledgers. The goal is not causal attribution. The goal is auditable measurement of the OCC bookkeeping objects and their morphology under stress.

## Sources
- EOIR “Pending Cases, New Cases, and Total Completions” (data generated 2025-07-31): `raw/EOIR_Pending_New_Completions_DataGenerated_2025-07-31.pdf`
- EOIR Adjudication Statistics (data generated 2025-11-18): `raw/EOIR_Adjudication_Statistics_2025-11-18.pdf`

Derived tables used in this test:
- `derived/EOIR_pending_receipts_completions.csv`
- `derived/EOIR_motions.csv`
- `derived/EOIR_merged_metrics.csv`

## OCC mapping (Tier 1)
- Initiation proxy: λ_exo(t) = initial receipts
- Attempted closure proxy: μ_a(t) = total completions
- Visible debt stock: L(t) = pending cases (end of fiscal year)
- Rework-pressure proxy: motions-to-reopen per completion
  - This is not an event-level reopen probability. It is a measurable reopen-pressure channel normalized by throughput.

## Plots
- Receipts vs completions: `outputs/EOIR_receipts_vs_completions.png`
- Pending stock L: `outputs/EOIR_pending_stock.png`
- Motions-to-reopen pressure proxy: `outputs/EOIR_mtr_per_completion.png`

## Results summary
### 1) Debt accumulation signature is present
Pending stock increases from 658,871 (FY2015) to 3,884,956 (FY2024), a 5.90× increase. Over the same period, the completion-to-receipt ratio falls from 0.744 (FY2015) to 0.395 (FY2024). This is Tier-1 binding exceedance morphology: initiation persistently exceeds durable settlement and the remainder accumulates as stock.

### 2) Accounting sanity check
For FY2016 onward, the discrete stock–flow residual (pending_end − (pending_prev + receipts − completions)) is small relative to the stock, typically around 1–2% of pending. Residuals are reported in the merged table and treated as boundary/definition artifacts, not evidence.

### 3) Rework-pressure proxy is mixed and not a sign test
Motions-to-reopen per completion fluctuates and falls after FY2021 because completions increase faster than motions. This ratio alone does not establish the nonstationarity trap. A clean sign test requires a precommitted compression proxy, lag structure, and a rework channel attributable to prior closures.

## Selected annual ledger (derived)
| FY | Pending L | Receipts λ | Completions μ | μ/λ | Stock-flow residual | Residual % of L | Motions to reopen | MTR per completion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 FY | 658,871 | 193,000 | 143,638 | 0.744 |  |  | 13,512 | 0.094 |
| 2018 FY | 1,039,403 | 316,133 | 195,146 | 0.617 | 22,739 | 2.19% | 17,760 | 0.091 |
| 2019 FY | 1,331,286 | 547,239 | 277,075 | 0.506 | 21,719 | 1.63% | 20,144 | 0.073 |
| 2020 FY | 1,504,246 | 369,598 | 232,311 | 0.629 | 35,673 | 2.37% | 17,887 | 0.077 |
| 2021 FY | 1,655,551 | 244,261 | 115,959 | 0.475 | 23,003 | 1.39% | 10,877 | 0.094 |
| 2022 FY | 2,063,123 | 707,527 | 314,788 | 0.445 | 14,833 | 0.72% | 16,263 | 0.052 |
| 2023 FY | 2,768,875 | 1,206,107 | 526,648 | 0.437 | 26,293 | 0.95% | 29,189 | 0.055 |
| 2024 FY | 3,884,956 | 1,783,915 | 704,514 | 0.395 | 36,680 | 0.94% | 44,655 | 0.063 |

## Interpretation discipline
This executed case supports Tier-1 OCC morphology claims: when receipts exceed completions, pending stock rises and the completion/receipt ratio deteriorates. It does not by itself establish causal claims about drift, compression, auditability collapse, or nonstationarity sign without Tier-3 driver proxies and a precommitted windowed design.
