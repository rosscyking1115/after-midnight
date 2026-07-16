# Verification summary

Source commit `d73acd5332e99557fe62c4400487a3bb20daadbc` implements the bounded credibility, provenance, terminology, rebrand, and feature-freeze work for Community Energy Flex v0.2.0.

## Release gates

| Gate | Result | Evidence |
|---|---|---|
| Python/API suite | pass | 157 passed, 1 skipped |
| Ruff | pass | `All checks passed!` |
| TypeScript | pass | `tsc --noEmit` |
| Next.js production build | pass | 8 routes generated/compiled |
| GitHub required checks | pass | CI run 29462275690 |
| OpenAPI/generated TypeScript parity | pass | generated client exposes carbon, price, and robustness fields; hashes in `manifest.json` |
| Controlled provenance matrix | pass | `provenance-matrix.json` and API tests |
| Public deployment smoke | pass | `deployment-smoke.md` |
| Claims/evidence language | pass | claim ledger plus public-copy regression tests |
| Independent code review | pass after fixes | 7 important findings corrected; re-review found no remaining blocker |

## Corrected or rejected claims

- Replaced “realised savings” with conditional ex-post results and an explicit `schedule_adherence_observed = false` boundary.
- Renamed the uncalibrated confidence score to a robustness indicator while preserving numerical behaviour.
- Removed unqualified 108%/95%, weekly, and annualised lead claims.
- Separated region capability (`supports_live_forecast`) from response state (`is_live_forecast`).
- Made GB live, GB sample fallback, NI typical profile, and unavailable sources distinct.
- Added actual price provenance for user-entered and successfully retrieved Agile tariffs.
- Retired the After Midnight public brand while preserving the fixed historical Vercel hostname.

## Known limitations

- No observed appliance execution, smart-meter consumption, or customer counterfactual.
- Robustness bands are heuristic and uncalibrated.
- NI uses a typical profile rather than a same-day live forecast.
- GB can degrade to a labelled sample profile during upstream failure.
- The reporting/warehouse paths use synthetic demonstration data.
