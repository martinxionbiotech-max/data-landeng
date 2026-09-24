#!/usr/bin/env python3
"""Phase 4: expand terminology dataset 215 -> 235 terms (+20)."""
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
    # --- Direction 2: 香品形态 (incense forms) ---
    term(
        "xiangbing", "香饼",
        "香饼 — incense cake; a pressed, hardened cake of blended incense powder and binder, burned whole on a censer. 香譜 lists 造香饼子法 'the method for making incense cakes' as a distinct form.",
        "xiāngbǐng", "fragrant cake", "incense cake / pressed incense cake",
        sources=XP,
    ),
    term(
        "xianggao", "香膏",
        "香膏 — aromatic ointment; the oily, resinous balsam extracted from a resin such as storax, prized as the genuinely aromatic fraction and kept apart from the spent woody residue (大秦国人采得苏合香先煎其汁以为香膏 'the Daqin people first decoct the storax to take its juice as fragrant ointment').",
        "xiānggāo", "fragrant paste", "aromatic ointment / balsam extract",
        sources=XC,
    ),
    # --- Direction 3: 品香空间/礼仪 (scent space & ritual) ---
    term(
        "xunyi", "薰衣",
        "薰衣 — clothes fumigation; scenting garments by exposing them to incense smoke or storing them with scented material. 香譜 records 蜀王薰御衣法 'the Shu king's method of fumigating royal clothes' and the 衣香法 'clothes-scenting method'.",
        "xūnyī", "fumigate clothes", "clothes fumigation / scenting clothes",
        sources=XP,
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Not 薰衣草 (xūnyīcǎo, lavender); 薰衣 is the classical practice of scenting garments"}],
    ),
    term(
        "yixiang", "衣香",
        "衣香 — clothes-scenting incense; the wearable sachet and garment-perfume genre, as distinct from burned 合香. 香乘 records 南阳公主熏衣香 (Princess Nanyang's clothes-scenting incense) and the inner-court sachet 内苑蕊心衣香.",
        "yīxiāng", "clothes fragrance", "clothes-scenting incense / wearable sachet",
        sources=XC,
    ),
    # --- Direction 4: 现代流通分级 (modern market grading) ---
    term(
        "shiyongji", "食用级",
        "食用级 — food-grade; a market and quality grade for materials cleared for food and drink, as distinct from an incense-grade supply. Entity buyer sections flag food-grade material (chenpi, chrysanthemum) while noting incense combustion produces smoke and particulate.",
        "shíyòngjí", "edible-use grade", "food-grade",
        extra=[{"@type": "PropertyValue", "name": "Usage", "value": "Modern trade terminology; appears in entity-page buyer sections as 'food-grade'"}],
    ),
    term(
        "xiangyongji", "香用级",
        "香用级 — incense-grade; a market and quality grade for material destined for incense use, valued differently from the tea-grade or food-grade market (chrysanthemum: 'tea-grade and incense-grade markets value the flower differently').",
        "xiāngyòngjí", "incense-use grade", "incense-grade",
        extra=[{"@type": "PropertyValue", "name": "Usage", "value": "Modern trade terminology; appears in entity-page buyer sections as 'incense-grade'"}],
    ),
    # --- Direction 5: 古籍残余 (classical 香谱 residue) ---
    term(
        "muxiang", "木香",
        "木香 — costus root (Saussurea costus, syn. Dolomiaea costus / Aucklandia lappa); a classical Himalayan incense root with a deep, earthy, slightly musky-animalic fixative character. Not to be confused with 木香花 (Banksia rose) or 白木香 (Aquilaria sinensis).",
        "mùxiāng", "wood fragrance", "costus root (Saussurea costus)",
        sources=XP,
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Shares 木香 with 木香花 (Banksia rose) and 白木香 (Aquilaria sinensis) but is a different plant"}],
    ),
    term(
        "yujin2", "郁金",
        "郁金 — aromatic turmeric (Curcuma aromatica), the ginger-family rhizome behind the classical aromatic 鬱金香; the name literally means 'aromatic gold'. Distinct from the modern tulip 郁金香 and from culinary 姜黄 (Curcuma longa).",
        "yùjīn", "aromatic gold", "aromatic turmeric (Curcuma aromatica)",
        sources=XP,
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "The same two characters 郁金香 also name the tulip; the classical aromatic is the Curcuma rhizome"}],
    ),
    term(
        "ainaxiang", "艾纳香",
        "艾纳香 — Blumea balsamifera (sambong / Ngai camphor), the aromatic shrub whose leaves are the source of leaf-distilled l-borneol (艾片). 香譜 records it as 艾蒳香, and 本草纲目 notes its use 'to blend the many aromatics'.",
        "àinàxiāng", "mugwort-accepting fragrance", "Blumea balsamifera (sambong)",
        sources=XP,
    ),
    term(
        "baijiaoxiang", "白胶香",
        "白胶香 — 'white-gum fragrance,' the classical name for sweetgum resin 枫香脂 (Liquidambar formosana), recorded in 香乘 and rendered in the Golden Light Sutra in transliteration as 须萨析罗婆.",
        "báijiāoxiāng", "white gum fragrance", "sweetgum resin (Liquidambar formosana)",
        sources=XC,
    ),
    # --- Direction 6: 深化页二次扫描 (deepened entity-page terms) ---
    term(
        "danggui", "当归",
        "当归 — dong quai (Angelica sinensis), a famous materia-medica root and 香囊 sachet herb with a warm, sweet, herbal scent. Same genus, different species from 白芷 (Angelica dahurica); the shared English 'angelica' hides the distinction.",
        "dāngguī", "ought to return", "dong quai (Angelica sinensis)",
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Distinct from 白芷 (Angelica dahurica); both translate to 'angelica' in English"}],
    ),
    term(
        "lingmaoxiang", "灵猫香",
        "灵猫香 — civet; the glandular secretion of the civet (Civettictis civetta / Viverricula indica), an animal-derived fixative with an animalic, musky, sweet-warm scent, largely replaced in modern perfumery by synthetic civetone.",
        "língmāoxiāng", "spirit-cat fragrance", "civet",
    ),
    term(
        "hailixiang", "海狸香",
        "海狸香 — castoreum; the scent secretion of the beaver (Castor fiber / C. canadensis), a Western classical perfumery fixative with no Chinese incense role, now almost entirely synthetic.",
        "hǎilíxiāng", "beaver fragrance", "castoreum",
    ),
    term(
        "zicaorong", "紫草茸",
        "紫草茸 — shellac / lac resin; the insect-derived resinous secretion of the lac insect (Kerria lacca), a functional binder and historical red dye (classical 紫鉚/紫矿). Despite the herbal-sounding name, it is not a plant material.",
        "zǐcǎoróng", "purple herb velvet", "shellac / lac resin (Kerria lacca)",
        extra=[{"@type": "PropertyValue", "name": "Misinterpretation risk", "value": "Name suggests a herb but it is an insect-derived resin"}],
    ),
    term(
        "biluxiangzhi", "秘鲁香脂",
        "秘鲁香脂 — Peru balsam (Myroxylon balsamum), a sweet, vanilla-like legume resin used in Western perfumery as a fixative and sweetener; a modern crossover with no classical Chinese incense origin.",
        "bìlǔ xiāngzhī", "Peru aromatic resin", "Peru balsam (Myroxylon balsamum)",
    ),
    term(
        "awei", "阿魏",
        "阿魏 — asafoetida (Ferula assa-foetida), a fiercely pungent, sulfurous resin of the carrot family (Apiaceae) that entered China via the Silk Road; its raw garlic-onion odor mellows on heating into an allium-like depth.",
        "āwèi", "a-wei (loanword)", "asafoetida (Ferula assa-foetida)",
    ),
    term(
        "baiji", "白及",
        "白及 — bletilla (Bletilla striata), a mucilaginous orchid tuber used as a water-soluble binder that holds incense powders together; valued for function, not fragrance.",
        "báijí", "white reach", "bletilla (binder tuber)",
    ),
    term(
        "luole", "罗勒",
        "罗勒 — basil (Ocimum basilicum), a mint-family culinary herb whose older Chinese name is 兰香 ('orchid fragrance'), a taboo-name substitution recorded in 本草纲目.",
        "luólè", "net-bind (loanword)", "basil (Ocimum basilicum)",
    ),
    term(
        "sharen", "砂仁",
        "砂仁 — amomum villosum (syn. Wurfbainia villosa), a ginger-family spice fruit used as a warm, camphoraceous 香药 accent in blended incense; 香乘 records it in the 南阳公主熏衣香 recipe.",
        "shārén", "sand kernel", "amomum villosum (cardamom husk)",
        sources=XC,
    ),
    term(
        "shannai", "山柰",
        "山柰 — sand ginger / kencur (Kaempferia galanga), a ginger-family rhizome used as a pungent, camphoraceous spice; not common ginger (生姜, Zingiber officinale).",
        "shānnài", "mountain nai", "sand ginger (Kaempferia galanga)",
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
d["version"] = "1.3"
d["changelog"] = (
    "Phase 4: added 20 terms (215 -> 235) across incense forms (香饼/香膏), scent space & ritual "
    "(薰衣/衣香), modern market grading (食用级/香用级), classical 香谱 residue (木香/郁金/艾纳香/白胶香), "
    "and deepened entity-page terms (当归/灵猫香/海狸香/紫草茸/秘鲁香脂/阿魏/白及/罗勒/砂仁/山柰)."
)

P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(new_terms)} new terms; total now {len(d['mainEntity'])}")
