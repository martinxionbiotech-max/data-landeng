# Datasets Overview

Eight machine-readable knowledge datasets for the LanDeng (澜灯) platform — Chinese botanical incense, documented in English with source transparency. All datasets are licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), are free to access, and are served as stable JSON from `data.incenseherbs.com`.

| Dataset | File | Entities | Last updated | Version |
|---|---|---|---|---|
| Ingredient database | [ingredients.json](https://data.incenseherbs.com/datasets/ingredients.json) | 150 | 2026-09-22 | 1.1 |
| Terminology database | [terminology.json](https://data.incenseherbs.com/datasets/terminology.json) | 235 | 2026-09-24 | 1.3 |
| Aroma database | [aroma.json](https://data.incenseherbs.com/datasets/aroma.json) | 10 | 2026-09-22 | 1.0 |
| Material database | [materials.json](https://data.incenseherbs.com/datasets/materials.json) | 15 | 2026-09-22 | 1.1 |
| Comparison database | [comparisons.json](https://data.incenseherbs.com/datasets/comparisons.json) | 17 | 2026-09-22 | 1.1 |
| Technique database | [techniques.json](https://data.incenseherbs.com/datasets/techniques.json) | 12 | 2026-09-22 | 1.1 |
| Form database | [forms.json](https://data.incenseherbs.com/datasets/forms.json) | 12 | 2026-09-22 | 1.1 |
| Relationships database | [relationships.json](https://data.incenseherbs.com/datasets/relationships.json) | 150 | 2026-09-22 | 1.0 |

## Ingredient database — 150 entities

`DefinedTerm` entities for botanical incense ingredients.

- **Fields:** `termCode` · `name` · `alternateName` (Chinese, pinyin) · `description` · `additionalProperty` (Chinese / Pinyin / Scientific name / Type / Aroma / Category) · `sameAs` · `sources` (with `evidenceLevel`)
- **Download:** [ingredients.json](https://data.incenseherbs.com/datasets/ingredients.json)

## Terminology database — 235 terms

Chinese–English terminology with pinyin, literal meaning, preferred translation, and context. Chinese is the source of truth; English is the agreed translation.

- **Fields:** `termCode` · `name` · `description` · `additionalProperty` (Pinyin / Literal meaning / Preferred English / Alternate forms / Misinterpretation risk) · `sources` (where applicable, with `evidenceLevel`)
- **Download:** [terminology.json](https://data.incenseherbs.com/datasets/terminology.json)

## Aroma database — 10 families

The ten aroma families, each listing its member ingredients.

- **Fields:** `termCode` · `name` · `memberIngredients`
- **Download:** [aroma.json](https://data.incenseherbs.com/datasets/aroma.json)

## Material database — 15 entities

Functional materials — binders, bases, cores, fuels, and loose aromatic materials.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Type / Source / Processing / Physical characteristics / Aroma / Burning behavior / Applications) · `sources` (where applicable, with `evidenceLevel`)
- **Download:** [materials.json](https://data.incenseherbs.com/datasets/materials.json)

## Comparison database — 17 profiles

Comparison profiles for incense formats and classical materials.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Material / Aroma / Smoke / Burn characteristics / Traditional context / Common uses / Quality factors) · `sources` (with `evidenceLevel`)
- **Download:** [comparisons.json](https://data.incenseherbs.com/datasets/comparisons.json)

## Technique database — 12 techniques

Heating, pressing, blending, appreciation, and carrying methods.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Type / Period / Materials / Equipment / Smoke level / Related) · `sources` (with `evidenceLevel`)
- **Download:** [techniques.json](https://data.incenseherbs.com/datasets/techniques.json)

## Form database — 12 forms

Delivery forms — sticks, coils, cones, powder, pills, beads, and low-smoke / smokeless categories.

- **Fields:** `termCode` · `name` · `alternateName` · `description` · `additionalProperty` (Form / Construction / Burn time / Intensity / Use case) · `sources` (with `evidenceLevel`)
- **Download:** [forms.json](https://data.incenseherbs.com/datasets/forms.json)

## Relationships database — 150 entities

Derived entity relationships linking each ingredient to its aroma families, category, comparison profiles, and techniques.

- **Fields:** `termCode` · `name` · `relatedEntity` (`type` / `termCode` / `name` / `inDataset`)
- **Download:** [relationships.json](https://data.incenseherbs.com/datasets/relationships.json)
- **Governance:** every relationship is derived from the seven source datasets — no new fact is introduced. See [Relationships Database](relationships.md).

## License & governance

All datasets are licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — free to share and adapt with attribution, share-alike. Data changes require source traceability. See [Format & Governance](format.md).
