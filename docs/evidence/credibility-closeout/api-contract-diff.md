# API contract diff

Version 0.2.0 intentionally changes the public contract.

## Regions

- Removed `has_live_forecast`.
- Added `supports_live_forecast` as a capability flag.

## Forecast and optimise provenance

- Replaced loose source strings with `gb_live_forecast`, `ni_eirgrid_typical_profile`, `gb_sample_profile`, or `unavailable`.
- Added `carbon_source_label`, `is_live_forecast`, `is_fallback`, `fallback_reason`, and retrieval/valid timestamps.
- Added `price_source`, `price_source_label`, `price_is_live`, and `price_unavailable_reason`.
- Optimise responses now carry the provenance of the carbon curve and tariff actually used.

## Recommendation explanation

- Removed `confidence` and `confidence_band` from scheduled-task responses.
- Added `robustness_score` and `robustness_band`.

The Pydantic schema is canonical. `web/lib/types.gen.ts` was regenerated from that OpenAPI schema, then imported by the web client through `web/lib/types.ts`.
