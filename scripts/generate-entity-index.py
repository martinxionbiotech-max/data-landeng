#!/usr/bin/env python3
"""Generate the per-entity index in docs/ingredients.md.

Rewrites everything between the ENTITY-INDEX markers with one section per
ingredient entity, each carrying a stable anchor URL:

    https://data.incenseherbs.com/ingredients/#<termCode>

Source of truth is datasets/ingredients.json (no facts are invented; the
index is a projection of the dataset). Idempotent: re-runs replace the
marked region only. The main-site article link uses the stable pattern
https://incenseherbs.com/ingredients/<termCode>/ (termCode == main-site slug).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ING = ROOT / 'datasets' / 'ingredients.json'
DOC = ROOT / 'docs' / 'ingredients.md'
START = '<!-- ENTITY-INDEX:START -->'
END = '<!-- ENTITY-INDEX:END -->'


def prop(ent, name, default=''):
    for p in ent.get('additionalProperty', []):
        if p.get('name') == name:
            return p.get('value', default)
    return default


def main():
    data = json.load(open(ING, encoding='utf-8'))
    me = data['mainEntity']
    items = me['itemListElement'] if isinstance(me, dict) else me
    items = sorted(items, key=lambda e: e.get('termCode', ''))

    lines = []
    for e in items:
        code = e.get('termCode')
        name = e.get('name', code)
        zh = prop(e, 'Chinese')
        py = prop(e, 'Pinyin')
        sci = prop(e, 'Scientific name')
        cat = prop(e, 'Category')
        aroma = prop(e, 'Aroma')
        lines.append(f'## {name} ({zh}) {{#{code}}}\n')
        facts = [f'**termCode:** `{code}`']
        if zh:
            facts.append(f'**Chinese:** {zh}')
        if py:
            facts.append(f'**Pinyin:** {py}')
        if sci:
            facts.append(f'**Scientific:** *{sci}*')
        if cat:
            facts.append(f'**Category:** {cat}')
        if aroma:
            facts.append(f'**Aroma:** {aroma}')
        lines.append(' · '.join(facts) + '\n')
        lines.append(
            f'**Main site article:** [{name}](https://incenseherbs.com/ingredients/{code}/) · '
            f'**Dataset:** [ingredients.json](https://data.incenseherbs.com/datasets/ingredients.json)\n'
        )

    text = DOC.read_text(encoding='utf-8')
    if START not in text or END not in text:
        raise SystemExit(f'{DOC}: ENTITY-INDEX markers missing — add them first')

    head, _, tail = text.partition(START)
    _, _, tail = tail.partition(END)
    body = f'{START}\n\n' + '\n'.join(lines) + f'\n{END}'
    DOC.write_text(head + body + tail, encoding='utf-8')
    print(f'generated {len(items)} entity sections in docs/ingredients.md')


if __name__ == '__main__':
    main()
