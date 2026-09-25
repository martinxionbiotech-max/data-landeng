# Relationships Database

Derived entity relationships between the 150 botanical incense ingredient entities and the entities of the other LanDeng datasets — aroma families, comparison profiles, techniques, and categories.

Every relationship is **derived from the seven source datasets** (`ingredients.json`, `aroma.json`, `comparisons.json`, `techniques.json`, `forms.json`, `materials.json`, `terminology.json`). No new fact is introduced.

## Structure

```json
{
  "@type": "DefinedTerm",
  "termCode": "agarwood",
  "name": "Agarwood",
  "relatedEntity": [
    { "type": "category",   "termCode": "woods",    "name": "Woods",            "inDataset": "ingredients.json" },
    { "type": "aroma",      "termCode": "woody",    "name": "Woody",            "inDataset": "aroma.json" },
    { "type": "aroma",      "termCode": "resinous", "name": "Resinous",         "inDataset": "aroma.json" },
    { "type": "comparison", "termCode": "agarwood", "name": "Agarwood",         "inDataset": "comparisons.json" },
    { "type": "technique",  "termCode": "indirect-fire", "name": "Indirect-Fire Incense", "inDataset": "techniques.json" }
  ]
}
```

## Relation types

| Type | Derivation source |
|---|---|
| `category` | ingredient `Category` field in `ingredients.json` |
| `aroma` | ingredient `Aroma` field, matched to the ten aroma families in `aroma.json` |
| `comparison` | ingredient `termCode` matched to a material profile in `comparisons.json` |
| `technique` | ingredient name referenced in the `Materials` field of `techniques.json` |

The `form` relation type is reserved in the schema. The current `forms.json` records delivery formats (stick, coil, cone, …) without ingredient-level references, so no `form` relations are derived yet — none are fabricated.

## Coverage

| Type | Edges |
|---|---|
| `category` | 150 |
| `aroma` | 280 |
| `comparison` | 7 |
| `technique` | 13 |
| **Total** | **450** |

[Download the JSON](https://data.incenseherbs.com/datasets/relationships.json) · [Download CSV](https://data.incenseherbs.com/downloads/relationships.csv)
