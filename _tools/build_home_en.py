"""從中文首頁 index.html 產生英文首頁 en/index.html。

首頁本身是中英雙語（按鈕切換），但同一個網址 Google 只會收一種語言，
所以英文版另外輸出到 /en/：拿掉中文區塊、預設英文、換成英文的 head 與結構化資料。
改完首頁後重跑：python3 -I _tools/build_home_en.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://momoxie0202.github.io"

TITLE = "Apps by H.C: Dance Practice and Party Game Apps for iPhone"
DESC = ("9 free apps by indie developer H.C: SyncMirror for dance practice, party games like "
        "Who's the Spy? and Charades, plus photo cleanup, a snippet keyboard and an ad-free reader.")
OG_TITLE = "Apps by H.C: dance practice, party games and everyday tools"
OG_DESC = "Nine apps made by one indie developer. Find each app's guide and download link here."


def strip_blocks(s, lang):
    """拿掉所有 <div ... data-block="lang"> 元素（含巢狀的 div）。"""
    pat = re.compile(r'<div[^>]*data-block="%s"[^>]*>' % lang)
    while True:
        m = pat.search(s)
        if not m:
            return s
        depth, i = 1, m.end()
        tag = re.compile(r"<div\b|</div>")
        while depth:
            t = tag.search(s, i)
            depth += 1 if t.group(0) != "</div>" else -1
            i = t.end()
        s = s[: m.start()] + s[i:]


def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, (a[:80], c)
    return s.replace(a, b)


def en_jsonld(s, zh):
    """英文版的結構化資料：作品清單與常見問題都取自頁面上看得到的英文內容（s 是已拿掉中文區塊的頁面）。"""
    person, website = zh["@graph"][0], zh["@graph"][1]
    tools = s[s.index('id="en-dance"'):s.index('id="faq"')]
    items = []
    cards = [re.search(r'<h3>(?:<img[^>]*>)?([^<]+)</h3><p>([^<]+)</p>.*?<a class="lk" href="([^"]+)"', a, re.S).groups()
             for a in re.findall(r'<article class="[go]".*?</article>', tools, re.S)]
    hero = re.search(r'<a class="lk" href="([^"]+)"', tools)
    items.append(("SyncMirror", "Learn dances from video: mirror, slow down, loop a section, then record and compare.", hero.group(1)))
    items += [(n, d, u) for n, d, u in cards]
    faq_html = s[s.index('id="faq"'):s.index('class="policy-section')]
    faq = re.findall(r'<h3>(.*?)</h3>.*?<p>(.*?)</p>', faq_html, re.S)
    unesc = lambda x: x.replace("&amp;", "&")
    graph = [
        person,
        website,
        {
            "@type": "CollectionPage",
            "@id": SITE + "/en/#page",
            "name": TITLE,
            "description": DESC,
            "url": SITE + "/en/",
            "inLanguage": "en",
            "isPartOf": {"@id": website["@id"]},
            "about": {"@id": person["@id"]},
            "dateModified": zh["@graph"][2]["dateModified"],
            "mainEntity": {
                "@type": "ItemList",
                "name": "Apps by H.C",
                "numberOfItems": len(items),
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": unesc(n), "description": unesc(d),
                     "url": SITE + "/" + u.lstrip("/")}
                    for i, (n, d, u) in enumerate(items)
                ],
            },
        },
        {
            "@type": "FAQPage",
            "@id": SITE + "/en/#faq",
            "inLanguage": "en",
            "mainEntity": [
                {"@type": "Question", "name": unesc(q.strip()),
                 "acceptedAnswer": {"@type": "Answer", "text": unesc(a.strip())}}
                for q, a in faq
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")


def main():
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    s = strip_blocks(s, "zh")
    s = rep(s, '<html lang="zh-Hant">', '<html lang="en">')
    # 中文首頁裡英文大標是 <p class="h1">（一頁只留一個 h1），英文首頁換回 h1
    i = s.index('<p class="h1">')
    j = s.index("</p>", i)
    s = s[:i] + "<h1>" + s[i + len('<p class="h1">'):j] + "</h1>" + s[j + 4:]
    # 站內相對路徑改成從根目錄起算
    s = re.sub(r'(src|href|data-zh-src|data-en-src)="apps/', r'\1="/apps/', s)
    s = rep(s, '<a class="identity" href="./">', '<a class="identity" href="/en/">')
    # head
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
    s = rep(s, f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/en/">')
    s = re.sub(r'<meta property="og:site_name" content="[^"]*">', '<meta property="og:site_name" content="Apps by H.C">', s)
    s = rep(s, '<meta property="og:locale" content="zh_TW">', '<meta property="og:locale" content="en_US">')
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{OG_TITLE}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{OG_DESC}">', s)
    s = rep(s, f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/en/">')
    s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="Apps by H.C">', s)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{OG_TITLE}">', s)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{OG_DESC}">', s)
    zh_ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    s = re.sub(r'(<script type="application/ld\+json">).*?(</script>)',
               lambda m: m.group(1) + "\n" + en_jsonld(s, zh_ld) + "\n  " + m.group(2),
               s, count=1, flags=re.S)
    # 靜態內容直接是英文（不靠腳本換字），搜尋引擎不跑腳本也看得到
    en = dict(re.findall(r'^\s+(\w+): "([^"]*)",?$', s[s.index("var en = {"):s.index("};", s.index("var en = {"))], re.M))
    s = re.sub(r'(<[^>]*data-i18n="(\w+)"[^>]*>)[^<]*', lambda m: m.group(0) if m.group(2) not in en else m.group(1) + en[m.group(2)], s)
    # 截圖預設用英文版
    def en_img(m):
        t = m.group(0)
        src, alt = re.search(r'data-en-src="([^"]*)"', t), re.search(r'data-en-alt="([^"]*)"', t)
        t = re.sub(r' src="[^"]*"', f' src="{src.group(1)}"', t, count=1) if src else t
        return re.sub(r' alt="[^"]*"', f' alt="{alt.group(1)}"', t, count=1) if alt else t
    s = re.sub(r"<img[^>]*data-en-src=[^>]*>", en_img, s)
    s = re.sub(r'href="([^"]*)" data-zh-href="([^"]*)" data-en-href="([^"]*)"', r'href="\3" data-zh-href="\2" data-en-href="\3"', s)
    s = rep(s, 'data-set-lang="zh" aria-pressed="true"', 'data-set-lang="zh" aria-pressed="false"')
    s = rep(s, 'data-set-lang="en" aria-pressed="false"', 'data-set-lang="en" aria-pressed="true"')
    out = ROOT / "en" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(s, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
