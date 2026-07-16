# Deployment smoke — 2026-07-16

The fixed production URLs were checked after source commit `d73acd5332e99557fe62c4400487a3bb20daadbc` reached `main` and the API was deployed with Fly's rolling strategy.

| Check | Observed | Result |
|---|---|---|
| `https://after-midnight-beta.vercel.app/` | HTTP 200; Community Energy Flex brand present | pass |
| `https://community-energy-flex-api.fly.dev/v1/health` | `status: ok` | pass |
| `/openapi.json` | API 0.2.0; robustness and price-provenance fields present | pass |
| Fly London forecast | `gb_live_forecast`, `is_live_forecast: true`, `is_fallback: false` | pass |
| Vercel London proxy | source agrees with Fly (`gb_live_forecast`) | pass |
| Fly Northern Ireland forecast | `ni_eirgrid_typical_profile`, `is_live_forecast: false` | pass |
| Vercel Northern Ireland proxy | source agrees with Fly (`ni_eirgrid_typical_profile`) | pass |
| Public optimise request | succeeds; carbon source, `user_entered_tariff`, and `robustness_score` present | pass |
| Fly machine checks | rolling deployment completed; active machine health check passed | pass |

The GB upstream happened to return live data during this smoke. Fallback was verified through the controlled provider seam in tests; production was not intentionally disrupted. Availability remains a dated observation, not a service-level guarantee.
