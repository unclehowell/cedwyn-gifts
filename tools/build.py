#!/usr/bin/env python3
"""Build public/index.html from public/data/chronology.json (Gifts, webapp 56 of 59). Static, no-JS first. — Sion's Tab agent"""
import json, html, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / 'public' / 'data' / 'chronology.json', encoding='utf-8'))
E = lambda s: html.escape(str(s or ''), quote=True)
HOLD = D['holders']; ROWS = sorted(D['rows'], key=lambda r: r['sort'])
CAT = 'https://bucklerfamily.estate/catalogue/?id='
GIFT = {'recorded': ('g-rec', '●', 'Gift (recorded)'), 'noprice': ('g-np', '◐', 'No price stated'),
        'unchecked': ('g-un', '○', 'Consideration not checked'), 'none': ('g-no', '–', 'No transfer on the record')}
def parcel_tags(p):
    t = []
    for k in ('A1', 'A2', 'A', 'B', 'C'):
        if (' ' + p.replace(',', ' ').replace('(', ' ') + ' ').find(' ' + k + ' ') >= 0 or p.startswith(k + ' ') or p == k: t.append(k)
    return ' '.join(sorted(set(t))) or 'other'
def row(r, i):
    band = [h for h in r.get('band', []) if h in HOLD]
    inb = bool(band)
    cols = [HOLD[h]['colour'] for h in band] or ['#888']
    rib = cols[0] if len(cols) == 1 else 'linear-gradient(180deg,' + ','.join(cols) + ')'
    g = r.get('gift')
    gh = ''
    if g in GIFT:
        c, sym, lab = GIFT[g]
        gh = f'<p class="gift {c}"><span class="gm" aria-hidden="true">{sym}</span> <strong>{lab}.</strong> {E(r.get("gift_note"))}</p>'
    elif r.get('gift_note'):
        gh = f'<p class="gift g-na">{E(r["gift_note"])}</p>'
    src = ' · '.join(f'<a href="{CAT}{E(s)}">{E(s)}</a>' for s in r['src'])
    chips = ''.join(f'<span class="chip" style="--c:{HOLD[h]["colour"]}">{E(HOLD[h]["name"])}</span>' for h in band)
    cls = 'ev in' if inb else 'ev out'
    if g in ('recorded', 'noprice', 'unchecked'): cls += ' isgift-' + g
    return (f'<li class="{cls}" id="r{i+1}" data-parcels="{parcel_tags(r["parcels"])}" style="--rib:{rib}">'
            f'<div class="when">{E(r["date"])}</div><p class="what">{E(r["event"])}</p>'
            f'<div class="tc"><div><span class="lab">Title (freeholder)</span>{E(r["title"])}</div>'
            f'<div><span class="lab">Custody (tenant / occupier)</span>{E(r["custody"])}</div></div>'
            f'<p class="par"><span class="lab">Parcel</span> {E(r["parcels"])}</p>{gh}'
            + (f'<p class="chips">{chips}</p>' if chips else '') +
            f'<p class="src"><span class="lab">Our records</span> {src} <span class="seen">— {E(r["seen"])}</span></p></li>')
n = len(ROWS); cnt = {k: sum(1 for r in ROWS if r.get('gift') == k) for k in GIFT}
legend = ''.join(f'<span class="chip" style="--c:{v["colour"]}">{E(v["name"])}</span>' for v in HOLD.values())
nc = ''.join(f'<li>{E(x)}</li>' for x in D['not_checked'])
log = ''.join(f'<tr><td>{E(c["version"])}</td><td>{E(c["date"])}</td><td>{E(c["editor"])}</td><td>{E(c["change"])}</td></tr>' for c in D['changelog'])
page = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="app-version" content="{E(D['version'])}">
<title>Gifts · title and custody of Parcels A, B and C, 1877 onwards · Great House, Cedwyn Estate</title>
<meta name="description" content="One chronology, 1877 onwards, of the known title chain and custody of Parcels A, B and C at Tŷ Mawr (Great House), Llandough, with every recorded gift and every transfer whose price we have not seen marked, each linked to its record.">
<link rel="canonical" href="https://bucklerfamily.estate/gifts/">
<meta property="og:title" content="Gifts · Parcels A, B and C, 1877 onwards">
<meta property="og:description" content="Who held the title and who held the land, side by side, with the recorded gifts marked.">
<meta property="og:url" content="https://bucklerfamily.estate/gifts/">
<link rel="alternate" type="application/json" href="data/chronology.json" title="Chronology (data)">
<script>window.__cedwynLP="/gifts/"</script><script src="/_cedwyn/ghf/ghf-boot.js?v=2.1.30"></script>
<meta name="theme-color" content="#f7f5ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16161d" media="(prefers-color-scheme: dark)">
<style>
:root{{--bg:#f7f5ef;--fg:#1d1d24;--mut:#5d5d6b;--card:#fff;--line:#d9d5c8;--acc:#7a3b12;--gold:#b8860b;--goldbg:#fff4d6;--box:#fff8e6;--boxl:#d9a441}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16161d;--fg:#e9e9f0;--mut:#a3a3b5;--card:#1f1f29;--line:#33333f;--acc:#f0b27a;--gold:#e7b84a;--goldbg:#2e2614;--box:#2a2416;--boxl:#b8862b}}}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:anywhere}}
a{{color:var(--acc)}}main{{max-width:52rem;margin:0 auto;padding:16px}}
h1{{font-size:1.5rem;line-height:1.25;margin:.2em 0 .3em}}h2{{font-size:1.08rem;margin:1.6em 0 .5em}}
.lede{{font-size:1.02rem;margin:.2em 0 .8em}}.muted,.seen{{color:var(--mut);font-size:14px}}
.key{{display:flex;flex-wrap:wrap;gap:6px 14px;margin:8px 0;font-size:14px;padding:0;list-style:none}}
.stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:12px 0}}@media(min-width:560px){{.stats{{grid-template-columns:repeat(4,1fr)}}}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 10px}}.stat b{{display:block;font-size:1.3rem}}
.ctl{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}.ctl button{{font:inherit;font-size:14px;padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}}
.ctl button[aria-pressed=true]{{background:var(--acc);color:var(--bg);border-color:var(--acc)}}
ol.chron{{list-style:none;margin:0;padding:0}}
.ev{{position:relative;padding:10px 12px 10px 20px;background:var(--card)}}
.ev::before{{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:var(--rib)}}
.ev.in{{border-left:0;border-right:1px solid var(--line)}}
.ev.in:first-child,.ev.out+.ev.in{{border-top:1px solid var(--line);border-radius:10px 10px 0 0}}
.ev.in:has(+.ev.out),.ev.in:last-child{{border-bottom:1px solid var(--line);border-radius:0 0 10px 10px;margin-bottom:10px}}
.ev.out{{border:1px solid var(--line);border-radius:10px;margin:10px 0}}.ev.out::before{{border-radius:10px 0 0 10px}}
.when{{font-weight:700;color:var(--acc);font-size:15px}}.what{{margin:2px 0 6px}}
.tc{{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:4px 0;font-size:15px}}
.tc>div{{padding:6px 8px 6px 0}}.tc>div+div{{padding-left:8px}}
.lab{{display:block;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut)}}
.par .lab,.src .lab{{display:inline;margin-right:4px}}.par,.src{{margin:4px 0;font-size:14px}}
.gift{{margin:6px 0;padding:6px 8px;border-radius:8px;font-size:14px}}.gm{{font-size:16px}}
.g-rec{{background:var(--goldbg);border:2px solid var(--gold)}}.g-rec .gm{{color:var(--gold)}}
.g-np{{background:var(--box);border:1px dashed var(--boxl)}}.g-un{{border:1px dashed var(--line)}}.g-no,.g-na{{color:var(--mut)}}
.ev.isgift-recorded{{box-shadow:inset 0 0 0 2px var(--gold)}}
.chips{{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0 2px}}.chip{{font-size:12px;padding:1px 8px;border-radius:999px;border:1px solid var(--c);color:var(--fg);background:color-mix(in srgb,var(--c) 14%,transparent)}}
.interp{{background:var(--box);border-left:4px solid var(--boxl);padding:10px 12px;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}}
[hidden]{{display:none!important}}
@media(max-width:330px){{.tc{{grid-template-columns:1fr}}.tc>div+div{{padding-left:0}}}}
</style>
</head>
<body>
<main id="top">
<h1>Gifts</h1>
<p class="lede">Title and custody of Parcels A, B and C at Tŷ Mawr (Great House), Llandough, 1877 onwards: who held the title and who held the land, side by side, in one chronology. Every transfer recorded as a gift, or with no price stated, is marked, and so is every transfer whose price we have not seen.</p>
<p class="muted">Parcels: A = the house parcel (A1 the north woods, A2 the house and garden); B = the meadow; C = the green (village green VG41). Bute and Cardiff Corporation, Daniel Thomas &amp; Son, Mountjoy Ltd, Western Ground Rents, BP and the Williams family are drawn as one continuous band: their hand-offs run into one another with no dividing line. Later holders sit outside the band.</p>
<div class="stats"><div class="stat"><b>{n}</b>dated rows</div><div class="stat"><b>{cnt['recorded']}</b>gift recorded</div><div class="stat"><b>{cnt['noprice']}</b>no price stated</div><div class="stat"><b>{cnt['unchecked']}</b>price not checked</div></div>
<ul class="key"><li><span style="color:var(--gold)">●</span> Gift (recorded)</li><li>◐ No price stated</li><li>○ Consideration not checked</li><li>– No transfer on the record</li></ul>
<p class="chips">{legend}</p>
<div class="ctl" id="ctl" hidden><button data-p="all" aria-pressed="true">All</button><button data-p="A">A</button><button data-p="A1">A1</button><button data-p="A2">A2</button><button data-p="B">B</button><button data-p="C">C</button><button data-g="1" aria-pressed="false">Gift markers only</button></div>
<ol class="chron" id="chron">
{''.join(row(r, i) for i, r in enumerate(ROWS))}
</ol>
<h2>Interpretation</h2>
<div class="interp"><p>{E(D['interpretation'])}</p></div>
<h2>Not checked</h2>
<ul>{nc}</ul>
<p class="muted">Each record link opens our own catalogue entry. The chronology as data: <a href="data/chronology.json">data/chronology.json</a>. Interpretation boxes are our reading of the evidence, not findings of any court or authority.</p>
<details><summary>Version {E(D['version'])} · change log</summary><table><thead><tr><th>Version</th><th>Date (UTC)</th><th>Editor</th><th>Change</th></tr></thead><tbody>{log}</tbody></table><p class="muted">Version {E(D['version'])} is free to read.</p></details>
</main>
<script>
(function(){{var c=document.getElementById('ctl');if(!c)return;c.hidden=false;var p='all',g=false,li=[].slice.call(document.querySelectorAll('#chron>li'));
function run(){{li.forEach(function(e){{var tags=(e.getAttribute('data-parcels')||'').split(' ');var okp=p==='all'||tags.indexOf(p)>=0||(p==='A'&&(tags.indexOf('A1')>=0||tags.indexOf('A2')>=0));var okg=!g||/isgift-/.test(e.className);e.hidden=!(okp&&okg);}});}}
c.addEventListener('click',function(ev){{var b=ev.target.closest('button');if(!b)return;if(b.dataset.g){{g=!g;b.setAttribute('aria-pressed',g);}}else{{p=b.dataset.p;[].forEach.call(c.querySelectorAll('button[data-p]'),function(x){{x.setAttribute('aria-pressed',x===b);}});}}run();}});}})();
</script>
</body>
</html>
"""
out = ROOT / 'public' / 'index.html'
out.write_text(page, encoding='utf-8'); print('wrote', out, len(page))
