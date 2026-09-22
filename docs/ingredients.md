# Ingredient Database

150 botanical incense ingredients as `DefinedTerm` entities.

Fields per entity: `termCode` · `name` · `alternateName` (Chinese, pinyin) · `description` · `additionalProperty` (Chinese / Pinyin / Scientific name / Type / Aroma / Category) · `sameAs` · `sources` (with `evidenceLevel`).

[Download the JSON](https://data.incenseherbs.com/datasets/ingredients.json)
Every entity has a full research article with an Evidence & Sources layer on the main site — see the [ingredient encyclopedia](https://incenseherbs.com/ingredients/).

## Data governance

- **Last updated:** 2026-09-22
- **License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Version:** 1.1
- **Sources:** every entity carries a `sources` array; each citation is tagged with an `evidenceLevel` (Evidence Tier).
