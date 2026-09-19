# data-landeng — LanDeng Open Datasets

Machine-readable, link-worthy knowledge datasets for the LanDeng (澜灯) platform — Chinese botanical incense, documented in English with source transparency.

Per `ORIGINAL-DATA-ASSETS.md` (LanDeng main repo): every dataset must be accurate, traceable, structured, maintainable, reviewable. No sensitive or proprietary data.

## Datasets

| Dataset | File | Status |
|---|---|---|
| Ingredient database | datasets/ingredients.json | live (94 entities) |
| Terminology database | datasets/terminology.json | live (104 terms, CC BY-SA 4.0) |
| Aroma database | datasets/aroma.json | live (10 aroma families) |
| Material database | datasets/materials.json | live (15 entities) |
| Comparison database | datasets/comparisons.json | live (17 profiles) |

## Format

- JSON, Schema.org `Dataset` + `DefinedTerm` / `Product`, served at stable URLs.
- Build-time static generation; no runtime database in Phase 1.

## Governance

- Never expose sensitive or proprietary data.
- Data changes require source traceability (termCode / reference fields).
