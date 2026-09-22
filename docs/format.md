# Format & Governance

- JSON, Schema.org `Dataset` + `DefinedTerm` / `Product`, served at stable URLs.
- Build-time static generation (MkDocs); no runtime database in Phase 1.
- Never expose sensitive or proprietary data.
- Data changes require source traceability (`termCode` / reference fields).

## License & versioning

- Every dataset is licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (share-alike, attribution required) and carries a `license`, `version`, `dateModified`, and `changelog` field.
- Bump the minor `version` on any entity or structure change; record the change in `changelog`.

## Evidence level

Every `source` object carries an `evidenceLevel` field, assigned by source nature:

| Tier | Label | Source nature |
|---|---|---|
| Tier 1 | Scientific / Government | government checklists and regulatory lists (e.g. CITES) |
| Tier 2 | Academic / Museum / Institutional | botanical and taxonomic institutions (e.g. GBIF, Flora of China / eFloras) |
| Tier 3 | Historical primary source | classical Chinese texts (e.g. 本草綱目 / 香乘 on Wikisource) |
| Tier 4 | Industry / Trade terminology | trade and industry sources |
| Tier 5 | Traditional knowledge | traditional-knowledge sources |
| Tier 6 | Editorial synthesis | this site's own editorial pages |

## Source status

- Every source is a citation object `{ type, title, url, accessed, evidenceLevel }`.
- Source URLs must be on the allow-list (efloras.org / gbif.org / wikisource.org / checklist.cites.org / data.incenseherbs.com / incenseherbs.com / schema.org); the `license` field is the only exception (creativecommons.org).

## Deprecation

- To retire an entity without deleting it, set `"deprecated": true` on the entity.
- To replace an entity, point the old one at its successor with `"supersededBy": "<termCode>"`.
- Deprecated entities remain resolvable at their stable `termCode`; they are excluded from new relationships.
