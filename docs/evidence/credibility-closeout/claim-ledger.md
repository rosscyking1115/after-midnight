# Closeout claim-ledger snapshot

This is the release snapshot of the authoritative [`docs/CLAIM_LEDGER.md`](../../CLAIM_LEDGER.md).

| Claim | Closeout decision |
|---|---|
| Feasible-window recommendations with explicit baselines | supported by optimiser tests |
| GB live carbon forecast | conditional; only when `is_live_forecast` is true |
| NI live forecast | rejected; NI is a labelled typical profile |
| Always-live service | rejected; fallback/unavailable states are explicit |
| Calibrated confidence | rejected; robustness is a heuristic indicator |
| Realised household savings | rejected; adherence and consumption are not observed |
| Synthetic dashboard/case-study figures as customer outcomes | rejected |
| Excel/PDF exports | supported by serialisation tests |
| Public web/API availability | observed only at the dated deployment smoke |

Any future headline number or outcome claim requires new reproducible evidence and a new accepted scope decision.
