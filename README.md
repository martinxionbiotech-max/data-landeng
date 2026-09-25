# data-landeng — LanDeng Open Datasets

Machine-readable, link-worthy knowledge datasets for the LanDeng (澜灯) platform — Chinese botanical incense, documented in English with source transparency.

Per `ORIGINAL-DATA-ASSETS.md` (LanDeng main repo): every dataset must be accurate, traceable, structured, maintainable, reviewable. No sensitive or proprietary data.

## Datasets

| Dataset | File | CSV | Status |
|---|---|---|---|
| Ingredient database | datasets/ingredients.json | [ingredients.csv](https://data.incenseherbs.com/downloads/ingredients.csv) | live (150 entities) |
| Terminology database | datasets/terminology.json | [terminology.csv](https://data.incenseherbs.com/downloads/terminology.csv) | live (235 terms, CC BY-SA 4.0) |
| Aroma database | datasets/aroma.json | [aroma.csv](https://data.incenseherbs.com/downloads/aroma.csv) | live (10 aroma families) |
| Material database | datasets/materials.json | [materials.csv](https://data.incenseherbs.com/downloads/materials.csv) | live (15 entities) |
| Comparison database | datasets/comparisons.json | [comparisons.csv](https://data.incenseherbs.com/downloads/comparisons.csv) | live (17 profiles) |
| Technique database | datasets/techniques.json | [techniques.csv](https://data.incenseherbs.com/downloads/techniques.csv) | live (12 techniques) |
| Form database | datasets/forms.json | [forms.csv](https://data.incenseherbs.com/downloads/forms.csv) | live (12 forms) |
| Relationships database | datasets/relationships.json | [relationships.csv](https://data.incenseherbs.com/downloads/relationships.csv) | live (150 entities, 450 edges) |

## Format

- JSON, Schema.org `Dataset` + `DefinedTerm` / `Product`, served at stable URLs.
- Flat CSV distribution packages (UTF-8 BOM for Excel) generated at build time from the JSON source; see [scripts/export_csv.py](scripts/export_csv.py).
- Build-time static generation; no runtime database in Phase 1.

## Governance

- Never expose sensitive or proprietary data.
- Data changes require source traceability (termCode / reference fields).
- Every dataset carries `license` (CC BY-SA 4.0), `version`, `dateModified`, and `changelog`.
- Every source citation carries an `evidenceLevel` (Evidence Tier). See [docs/format.md](docs/format.md).
