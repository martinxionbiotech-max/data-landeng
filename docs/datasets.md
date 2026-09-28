# Datasets Overview

Eight machine-readable knowledge datasets for the LanDeng (澜灯) platform — Chinese botanical incense, documented in English with source transparency. All datasets are licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), are free to access, and are served as stable JSON from `data.incenseherbs.com`.

<!-- AUTO:counts:datasets-table -->
| Dataset | File | CSV | Entities | Last updated | Version |
|---|---|---|---|---|---|
| Ingredient database | [ingredients.json](https://data.incenseherbs.com/datasets/ingredients.json) | [ingredients.csv](https://data.incenseherbs.com/downloads/ingredients.csv) | 150 | 2026-09-28 | 1.3 |
| Terminology database | [terminology.json](https://data.incenseherbs.com/datasets/terminology.json) | [terminology.csv](https://data.incenseherbs.com/downloads/terminology.csv) | 249 | 2026-09-28 | 1.5 |
| Aroma database | [aroma.json](https://data.incenseherbs.com/datasets/aroma.json) | [aroma.csv](https://data.incenseherbs.com/downloads/aroma.csv) | 10 | 2026-09-28 | 1.1 |
| Material database | [materials.json](https://data.incenseherbs.com/datasets/materials.json) | [materials.csv](https://data.incenseherbs.com/downloads/materials.csv) | 15 | 2026-09-28 | 1.2 |
| Comparison database | [comparisons.json](https://data.incenseherbs.com/datasets/comparisons.json) | [comparisons.csv](https://data.incenseherbs.com/downloads/comparisons.csv) | 17 | 2026-09-28 | 1.2 |
| Technique database | [techniques.json](https://data.incenseherbs.com/datasets/techniques.json) | [techniques.csv](https://data.incenseherbs.com/downloads/techniques.csv) | 12 | 2026-09-28 | 1.1 |
| Form database | [forms.json](https://data.incenseherbs.com/datasets/forms.json) | [forms.csv](https://data.incenseherbs.com/downloads/forms.csv) | 12 | 2026-09-28 | 1.2 |
| Relationships database | [relationships.json](https://data.incenseherbs.com/datasets/relationships.json) | [relationships.csv](https://data.incenseherbs.com/downloads/relationships.csv) | 150 | 2026-09-28 | 1.2 |
<!-- /AUTO:counts:datasets-table -->

<!-- AUTO:counts:h2-ingredients -->
## Ingredient database — 150 entities
<!-- /AUTO:counts:h2-ingredients -->

`DefinedTerm` entities for botanical incense ingredients.

- **Fields:** `termCode` · `name` · `alternateName` (Chinese, pinyin) · `description` · `additionalProperty` (Chinese / Pinyin / Scientific name / Type / Aroma / Category) · `url` (canonical main-site page) · `sameAs` · `sources` (with `evidenceLevel`)
- **Download:** [ingredients.json](https://data.incenseherbs.com/datasets/ingredients.json) · [ingredients.csv](https://data.incenseherbs.com/downloads/ingredients.csv)

<!-- AUTO:counts:h2-terminology -->
## Terminology database — 249 terms
<!-- /AUTO:counts:h2-terminology -->

Chinese–English terminology with pinyin, literal meaning, preferred translation, and context. Chinese is the source of truth; English is the agreed translation.

- **Fields:** `termCode` · `name` · `description` · `additionalProperty` (Pinyin / Literal meaning / Preferred English / Alternate forms / Misinterpretation risk) · `sources` (where applicable, with `evidenceLevel`)
- **Download:** [terminology.json](https://data.incenseherbs.com/datasets/terminology.json) · [terminology.csv](https://data.incenseherbs.com/downloads/terminology.csv)

<!-- AUTO:counts:h2-aroma -->
## Aroma database — 10 families
<!-- /AUTO:counts:h2-aroma -->

The ten aroma families, each listing its member ingredients.

- **Fields:** `termCode` · `name` · `memberIngredients`
- **Download:** [aroma.json](https://data.incenseherbs.com/datasets/aroma.json) · [aroma.csv](https://data.incenseherbs.com/downloads/aroma.csv)

<!-- AUTO:counts:h2-materials -->
## Material database — 15 entities
<!-- /AUTO:counts:h2-materials -->

Functional materials — binders, bases, cores, fuels, and loose aromatic materials.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Type / Source / Processing / Physical characteristics / Aroma / Burning behavior / Applications) · `sources` (where applicable, with `evidenceLevel`)
- **Download:** [materials.json](https://data.incenseherbs.com/datasets/materials.json) · [materials.csv](https://data.incenseherbs.com/downloads/materials.csv)

<!-- AUTO:counts:h2-comparisons -->
## Comparison database — 17 profiles
<!-- /AUTO:counts:h2-comparisons -->

Comparison profiles for incense formats and classical materials.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Material / Aroma / Smoke / Burn characteristics / Traditional context / Common uses / Quality factors) · `sources` (with `evidenceLevel`)
- **Download:** [comparisons.json](https://data.incenseherbs.com/datasets/comparisons.json) · [comparisons.csv](https://data.incenseherbs.com/downloads/comparisons.csv)

<!-- AUTO:counts:h2-techniques -->
## Technique database — 12 techniques
<!-- /AUTO:counts:h2-techniques -->

Heating, pressing, blending, appreciation, and carrying methods.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Type / Period / Materials / Equipment / Smoke level / Related) · `sources` (with `evidenceLevel`)
- **Download:** [techniques.json](https://data.incenseherbs.com/datasets/techniques.json) · [techniques.csv](https://data.incenseherbs.com/downloads/techniques.csv)

<!-- AUTO:counts:h2-forms -->
## Form database — 12 forms
<!-- /AUTO:counts:h2-forms -->

Delivery forms — sticks, coils, cones, powder, pills, beads, and low-smoke / smokeless categories.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Form / Construction / Burn time / Intensity / Use case) · `sources` (with `evidenceLevel`)
- **Download:** [forms.json](https://data.incenseherbs.com/datasets/forms.json) · [forms.csv](https://data.incenseherbs.com/downloads/forms.csv)

<!-- AUTO:counts:h2-relationships -->
## Relationships database — 150 entities
<!-- /AUTO:counts:h2-relationships -->

Derived entity relationships linking each ingredient to its aroma families, category, comparison profiles, and techniques.

- **Fields:** `termCode` · `name` · `relatedEntity` (`type` / `termCode` / `name` / `inDataset`)
- **Download:** [relationships.json](https://data.incenseherbs.com/datasets/relationships.json) · [relationships.csv](https://data.incenseherbs.com/downloads/relationships.csv)
- **Governance:** every relationship is derived from the seven source datasets — no new fact is introduced. See [Relationships Database](relationships.md).

## License & governance

All datasets are licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — free to share and adapt with attribution, share-alike. Data changes require source traceability. See [Format & Governance](format.md).
