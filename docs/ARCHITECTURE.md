# PostcodeLive architecture

PostcodeLive is the reusable orchestration and presentation layer for locality products such as LewesLive. It does not replace the specialist harvesting engines.

## Authoritative layers

1. **LocalEventsEngine** — event discovery, source recipes/plugins, provenance, source health, geocoding, deduplication, content/image enrichment, validation and public/site-bundle exports.
2. **LocalDirectory** — business/place harvesting, public-registry and first-party plugins, postcode enrichment, entity resolution, taxonomy, geospatial filtering, source policy, coverage gates and governed exports.
3. **LewesLive** — production reference implementation for map/location cards, icon governance, media provenance, cross-surface integrity, calendar/directory adapters and Hostinger deployment controls.
4. **PostcodeLive** — locality configuration, shared contracts, upstream orchestration, merged locality bundles, postcode/radius presentation and future social-output generation.

## Non-duplication rule

Harvesting logic stays in the specialist engines. PostcodeLive imports their governed outputs and normalises them to a stable common contract. Lewes-specific presentation rules become a locality profile or reusable contract rather than being copied into every town.

## Core contracts inherited from LewesLive

Lewes is the first production profile. The profile carries coordinate collision thresholds, bespoke icon requirements (320×320 PNG, <=50 KiB), card-image policy (WebP, <=100 KiB), postcode scope and quality gates. These contracts can be overridden by future localities without modifying engine code.

## Common locality bundle

`public_html/data/<slug>.bundle.v1.json` contains both places and events plus source/quality metadata. Front ends should depend on this contract, not on engine-internal file layouts.

## Migration principle

Existing LewesLive production assets remain authoritative until a PostcodeLive component passes parity/integrity tests. Migration is incremental and fail-closed; no working map, location card, directory or calendar surface should be removed simply because a shared replacement exists.
