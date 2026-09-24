#!/usr/bin/env python3
"""Phase 3: expand terminology dataset 188 -> 215 terms."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "datasets" / "terminology.json"
d = json.loads(P.read_text(encoding="utf-8"))

existing = {t["termCode"] for t in d["mainEntity"]}
existing_names = {t["name"] for t in d["mainEntity"]}


def term(code, name, desc, pinyin, literal, preferred, sources=None, extra=None):
    ap = [
        {"@type": "PropertyValue", "name": "Pinyin", "value": pinyin},
        {"@type": "PropertyValue", "name": "Literal meaning", "value": literal},
        {"@type": "PropertyValue", "name": "Preferred English", "value": preferred},
    ]
    if extra:
        ap.extend(extra)
    obj = {
        "@type": "DefinedTerm",
        "termCode": code,
        "name": name,
        "description": desc,
        "additionalProperty": ap,
    }
    if sources:
        obj["sources"] = sources
    return obj


XC = [
    {
        "type": "traditional",
        "title": "香乘 (Xiang Cheng) on Wikisource",
        "url": "https://zh.wikisource.org/wiki/香乘",
        "accessed": "2026-09-24",
        "evidenceLevel": "Tier 3 — Historical primary source",
    }
]
XP = [
    {
        "type": "traditional",
        "title": "香譜 (Hong Chu's Incense Manual) on Wikisource",
        "url": "https://zh.wikisource.org/wiki/香譜",
        "accessed": "2026-09-24",
        "evidenceLevel": "Tier 3 — Historical primary source",
    }
]

new_terms = [
    # --- Direction 1: 品香/香评词汇 (scent-appreciation vocabulary) ---
    term(
        "qing", "清",
        "清 — clear / pure; a bright, clean fragrance character with no muddiness or heaviness (香乘: 清芬韵度 'clear-fragrance character').",
        "qīng", "clear", "clear / fresh", sources=XC,
    ),
    term(
        "tian", "甜",
        "甜 — sweet; a honeyed, sugary aroma facet, one of the primary 品香 descriptors (香乘: 香甜如蜜).",
        "tián", "sweet", "sweet", sources=XC,
    ),
    term(
        "xin", "辛",
        "辛 — pungent; a sharp, spicy-hot aromatic quality, the classical '味辛' of spices and resins (香乘: 辛辣之气).",
        "xīn", "pungent", "pungent / spicy", sources=XC,
    ),
    term(
        "liang", "凉",
        "凉 — cooling; a cold, minty sensation in the nose, associated with borneol (龙脑) and camphor (樟脑).",
        "liáng", "cool", "cooling",
    ),
    term(
        "hou", "厚",
        "厚 — thick / full-bodied; a dense, rich, substantial scent character, the opposite of 薄 (香乘: 味厚 / 结实厚).",
        "hòu", "thick", "full-bodied", sources=XC,
    ),
    term(
        "bo", "薄",
        "薄 — thin / light; a delicate, faint scent character (香乘: 香味亦浅薄 'the fragrance is also thin/light').",
        "bó", "thin", "thin / light", sources=XC,
    ),
    term(
        "chun", "醇",
        "醇 — mellow / rich; a smooth, well-rounded, matured scent character (香乘 uses 淳醇 for a full, aged aroma).",
        "chún", "mellow", "mellow / rich", sources=XC,
    ),
    term(
        "ya", "雅",
        "雅 — refined / elegant; an understated, cultured fragrance character prized in literati incense appreciation.",
        "yǎ", "elegant", "refined / elegant",
    ),
    # --- Direction 2: 调香结构 (modern perfume structure) ---
    term(
        "qiandiao", "前调",
        "前调 — top note; the modern perfumery term for the first, most volatile scent phase, parallel to the classical 头香.",
        "qiándiào", "front note", "top note",
        extra=[{"@type": "PropertyValue", "name": "Related", "value": "头香 (touxiang) — classical top note"}],
    ),
    term(
        "zhongdiao", "中调",
        "中调 — middle / heart note; the sustained central phase of a fragrance, parallel to the classical 本香.",
        "zhōngdiào", "middle note", "middle note / heart note",
        extra=[{"@type": "PropertyValue", "name": "Related", "value": "本香 (benxiang) — classical body note"}],
    ),
    term(
        "houdiao", "后调",
        "后调 — base note; the slow, lasting final phase of a fragrance, parallel to the classical 尾香.",
        "hòudiào", "back note", "base note",
        extra=[{"@type": "PropertyValue", "name": "Related", "value": "尾香 (weixiang) — classical tail note"}],
    ),
    # --- Direction 3: 燃烧/物性 (burn & physical) ---
    term(
        "fayanliang", "发烟量",
        "发烟量 — smoke output; how much visible smoke an incense emits when burned, a key format and comparison variable.",
        "fāyānliàng", "smoke-emission amount", "smoke output",
    ),
    term(
        "ranshaosulv", "燃烧速率",
        "燃烧速率 — burn rate; how fast an incense smolders, set by thickness, density, binder ratio, and moisture.",
        "ránshāo sùlǜ", "combustion rate", "burn rate",
    ),
    term(
        "duanhuo", "断火",
        "断火 — self-extinguishing; a stick that smolders too slowly or goes out mid-burn, treated as a quality-control defect.",
        "duànhuǒ", "broken fire", "going out / self-extinguish",
    ),
    # --- Direction 4: 现代行业术语 (modern industry) ---
    term(
        "xiangjing", "香精",
        "香精 — fragrance oil; a manufactured scent concentrate (often synthetic) applied to a neutral base, distinct from essential oil (精油).",
        "xiāngjīng", "fragrance essence", "fragrance oil",
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Not the same as 精油 (essential oil); 香精 is a manufactured, often synthetic concentrate"}],
    ),
    term(
        "kuoxiang", "扩香",
        "扩香 — scent diffusion / throw; how far and how strongly a scent projects into a room.",
        "kuòxiāng", "scent diffusion", "scent throw / diffusion",
    ),
    term(
        "liuxiang", "留香",
        "留香 — longevity / tenacity; how long a scent persists after burning, or on skin and fabric.",
        "liúxiāng", "lingering fragrance", "longevity / tenacity",
    ),
    term(
        "dingxiangji", "定香剂",
        "定香剂 — fixative; a material that slows the evaporation of volatile notes and stabilizes a blend's structure.",
        "dìngxiāngjì", "scent-fixing agent", "fixative",
    ),
    # --- Direction 5: 古籍残余 (classical 香谱 residue) ---
    term(
        "zhantangxiang", "詹糖香",
        "詹糖香 — a classical aromatic listed in 香譜; 本草 records it from 晋安, 岑州, and south of 交广.",
        "zhāntángxiāng", "Zhantang fragrance", "Zhantang aromatic", sources=XP,
    ),
    term(
        "bolvxiang", "波律香",
        "波律香 — a classical aromatic from the kingdom of Polu, from the same tree as borneol (龙脑), per 香譜 citing 本草拾遗.",
        "bōlǜxiāng", "Polu fragrance", "Polu aromatic (borneol-related)", sources=XP,
    ),
    term(
        "midiexiang", "迷迭香",
        "迷迭香 — rosemary; 香譜 records it from the Western Regions, with an ode by Emperor Wen of Wei.",
        "mídiéxiāng", "rosemary", "rosemary", sources=XP,
    ),
    term(
        "duliangxiang", "都梁香",
        "都梁香 — a classical aromatic named for Duling County, recorded in 香譜 via 荆州记.",
        "dūliángxiāng", "Duling fragrance", "Duling aromatic", sources=XP,
    ),
    # --- Direction 6: 深化页新术语扫描 (entity-page new terms) ---
    term(
        "zitan", "紫檀",
        "紫檀 — red sandalwood (Pterocarpus santalinus), a crimson dye-and-carving wood, unrelated to true sandalwood (檀香, Santalum album).",
        "zǐtán", "purple sandalwood", "red sandalwood (Pterocarpus santalinus)",
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Shares the character 檀 with 檀香 but is a different plant, a dye wood not an incense heartwood"}],
    ),
    term(
        "zhangnao", "樟脑",
        "樟脑 — camphor crystal; the distilled crystalline extract of the camphor laurel (樟木, Cinnamomum camphora), distinct from borneol (龙脑).",
        "zhāngnǎo", "camphor-brain", "camphor (crystal)",
    ),
    term(
        "zangxiang", "藏香",
        "藏香 — Tibetan incense; thick, coreless, herbal-blend sticks rooted in Tibetan medicine (Sowa Rigpa) and monastery ritual.",
        "zàngxiāng", "Tibetan incense", "Tibetan incense",
    ),
    term(
        "muxianghua", "木香花",
        "木香花 — Banksia rose (Rosa banksiae), a sweet honeyed floral; its name is easily confused with 木香 (costus root).",
        "mùxiānghuā", "muxiang flower", "Banksia rose (Rosa banksiae)",
    ),
    term(
        "baitan", "白檀",
        "白檀 — white sandalwood; usually specifies Santalum album among the Santalum species, distinguishing it from substitute species.",
        "báitán", "white sandalwood", "white sandalwood (Santalum album)",
    ),
]

# Dedup + validation before append
dupes = []
for t in new_terms:
    if t["termCode"] in existing:
        dupes.append(t["termCode"])
    if t["name"] in existing_names:
        dupes.append(f"{t['termCode']} (name dup: {t['name']})")
if dupes:
    raise SystemExit(f"Duplicate detected, aborting: {dupes}")

d["mainEntity"].extend(new_terms)
d["dateModified"] = "2026-09-24"
d["version"] = "1.2"
d["changelog"] = (
    "Phase 3: added 27 terms (188 -> 215) across scent-appreciation vocabulary (清/甜/辛/凉/厚/薄/醇/雅), "
    "modern perfume structure (前调/中调/后调), burn & physical properties (发烟量/燃烧速率/断火), "
    "modern industry terms (香精/扩香/留香/定香剂), classical 香谱 residue (詹糖香/波律香/迷迭香/都梁香), "
    "and entity-page terms (紫檀/樟脑/藏香/木香花/白檀)."
)

P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(new_terms)} new terms; total now {len(d['mainEntity'])}")
