"""А/Б: две полные страницы с переключателем шапки и четыре отдельные шапки. Текст — landing-text-ab.md."""
import re, pathlib

P = pathlib.Path(__file__).resolve().parent / 'design/project'
d09 = (P / 'D09Tiles.dc.html').read_text()
p8 = (P / 'P08Tg.dc.html').read_text()

def svg_in(src, cls):
    return re.search(r'<span class="lg ' + cls + r'">(<svg.*?</svg>)</span>', src, re.S).group(1)

TG, MX, WA, ML, PH = (svg_in(d09, c) for c in ('tgl', 'mxl', 'wal', 'mll', 'phl'))
PH_LINE = re.search(r'<a class="p"[^>]*>(<svg.*?</svg>)Позвонить</a>', p8, re.S).group(1)
MINI = ''.join(f'<span class="lg {c}">{s}</span>' for c, s in (('tgl', TG), ('mxl', MX), ('wal', WA), ('mll', ML)))

def middle(name):
    src = (P / name).read_text()
    part = src.split('</header>', 1)[1].split('<section class="final">', 1)[0]
    part = part.replace('style="color: {{accent}}"', 'style="color: #E4570F"')
    assert '{{' not in part, name
    return part.strip()

AV = '/_blob/ccd2a2424da7cd555a2ab35526e17923'
P1 = '/_blob/2985a1c7c0e333a1ad74d350b32c5412'
MAX_URL = 'https://max.ru/u/f9LHodD0cOJkASyXXA3Vpr4QfCJV2S_tXXJb1efebr37kKnVIfBLA5ljKOA'

WRITE_BTN = (f'<button type="button" class="w" onClick="{{{{openSheet}}}}" aria-haspopup="dialog" aria-expanded="{{{{open}}}}">'
             f'<span class="av"><img src="{AV}" alt=""></span><span class="tt"><b>Написать</b>'
             f'<span class="mini" aria-hidden="true">{MINI}</span></span></button>')
CALL_BTN = f'<a class="p" href="tel:+79955098267">{PH_LINE}Позвонить</a>'
WRITE_BTN2 = WRITE_BTN.replace('{{openSheet}}', '{{openSheet2}}')
OPEN = lambda k: f'<sc-if value="{{{{{k}}}}}" hint-placeholder-val="{{{{ false }}}}">'
# Низ страницы: те же две кнопки, что в шапке («Написать» с мессенджерами и «Позвонить»)

def tiles(wide_call):
    call_cls = 'ct wide' if wide_call else 'ct'
    call_nm = 'nm' if wide_call else 'nm sm'
    return ('<div class="tiles">\n'
            f'<a class="ct" href="https://t.me/nikolaev_gd"><span class="lg tgl">{TG}</span><span class="t"><span class="sub">Написать в</span><span class="nm">Telegram</span></span></a>\n'
            f'<a class="ct" href="{MAX_URL}"><span class="lg mxl">{MX}</span><span class="t"><span class="sub">Написать в</span><span class="nm">Max</span></span></a>\n'
            f'<a class="ct" href="https://wa.me/79955098267"><span class="lg wal">{WA}</span><span class="t"><span class="sub">Написать в</span><span class="nm">WhatsApp</span></span></a>\n'
            f'<a class="ct" href="mailto:nikolaev.gd@gmail.com"><span class="lg mll">{ML}</span><span class="t"><span class="sub">Почта</span><span class="nm sm">nikolaev.gd@<wbr>gmail.com</span></span></a>\n'
            f'<a class="{call_cls}" href="tel:+79955098267"><span class="lg phl">{PH}</span><span class="t"><span class="sub">Позвонить</span><span class="{call_nm}">+7 995 509-82-67</span></span></a>\n'
            '</div>')


import html as _html
MD = pathlib.Path('/Users/kenneth/Dev/nikolaev-ai/landing-text-ab.md').read_text()
SECS = {}
for chunk in re.split(r'^## ', MD, flags=re.M)[1:]:
    title, _, rest = chunk.partition('\n')
    SECS[title.strip()] = [p.strip() for p in rest.split('\n\n') if p.strip()]
e = lambda t: _html.escape(t, quote=False)
def first(t):
    a, _, b = t.partition('. ')
    return a + '.', b

SHORT = ['а','в','и','к','о','с','у','я','во','до','за','из','ко','на','не','ни','но','об','от','по','со','то','для','без','при','про','под','над','или']
_TIE = re.compile(r'(?<![\w-])(' + '|'.join(SHORT + [w.capitalize() for w in SHORT]) + r'|[а-яё]{1,2}|[А-ЯЁ][а-яё]?|\d+)\s')
_NW = re.compile(r'(?<![\w-])([0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)+)')
def T(t):
    """Текст для страницы: короткие слова привязаны к следующему, слова через дефис не рвутся."""
    t = _TIE.sub(lambda m: m.group(1) + ' ', t)
    t = re.sub(r'(?<![\w-])(бы|б|ли|ль|же|ж) ', '\\1 ', t)
    t = re.sub(r'\s(бы|б|ли|ль|же|ж)(?![\w-])', ' \\1', t)
    if len(t) > 60 and ' ' in t:
        a, _, b = t.rpartition(' ')
        if len(b) <= 16 and ' ' not in b: t = a + ' ' + b
    return _NW.sub(r'<span class="nw">\1</span>', e(t))

def middle_html():
    q = SECS['С чем приходят']
    st_a, _, st_b = q[4].rpartition('. ')
    now = SECS['Что ИИ может делать за руководителя уже сейчас']
    hw = SECS['Как идёт работа']
    cs = SECS['Что просили и что получилось']
    br = SECS['К чему это может прийти']
    tm = SECS['Для команды']
    on = SECS['Про онлайн']
    ab = SECS['Обо мне']
    assert (len(q), len(now), len(hw), len(cs), len(br), len(tm), len(ab)) == (5, 7, 6, 5, 10, 6, 2), \
        (len(q), len(now), len(hw), len(cs), len(br), len(tm), len(ab))
    def pair(t):
        a, b = first(t)
        return f'<div class="pair"><p class="req">{T(a)}</p><p class="ans">{T(b)}</p></div>'
    def story(t, full=False, sep='. '):
        a, _, b = t.partition(sep)
        a += sep.strip()
        return f'<article class="story{" full" if full else ""}"><h3>{T(a)}</h3><p>{T(b)}</p></article>'
    def case(t, full=False):
        a, b = first(t)
        return f'<article class="case{" full" if full else ""}"><h3>{T(a)}</h3><p>{T(b)}</p></article>'
    out = f"""<section class="sec"><div class="wrap">
<div class="head">
<h2>{T('С чем приходят')}</h2>
<div class="intro">
<p>{T(q[0])}</p>
<p>{T(q[1])}</p>
</div>
</div>
<div class="bento">
{chr(10).join(f'<blockquote class="tile s6">{T(x)}</blockquote>' for x in q[2:4])}
</div>
<p class="statement">{T(st_a)}. <span class="acc">{T(st_b)}</span></p>
</div></section>

<section class="sec now tight"><div class="wrap">
<h2 class="wide">{T('Что ИИ может делать за руководителя уже сейчас')}</h2>
<p class="kicker">{T(now[0])}</p>
<div class="grid2 five">
{chr(10).join(f'<p class="card">{T(t)}</p>' for t in now[1:6])}
</div>
<p class="trust">{T(now[6])}</p>
</div></section>

<section class="sec inv work"><div class="wrap">
<div class="head">
<h2>{T('Как идёт работа')}</h2>
<div class="intro">
<p>{T(hw[0])}</p>
<p>{T(hw[1])}</p>
</div>
</div>
<p class="trust">{T(hw[2])}</p>
<div class="three">
{chr(10).join(f'<p class="card">{T(t)}</p>' for t in hw[3:6])}
</div>
</div></section>

<section class="sec"><div class="wrap">
<h2>{T('Что просили и что получилось')}</h2>
<div class="cases">
{chr(10).join(case(t, i == len(cs) - 1) for i, t in enumerate(cs))}
</div>
</div></section>

<section class="sec inv"><div class="wrap">
<div class="head">
<h2>{T('К чему это может прийти')}</h2>
<div class="intro">
<p>{T(br[0])}</p>
<p>{T(br[1])}</p>
</div>
</div>
<div class="pairs five">
{chr(10).join(pair(t) for t in br[2:7])}
</div>
<div class="stories">
{story(br[7], True)}
<div class="pair note"><p class="ans">{T(br[8])}</p></div>
</div>
<p class="trust">{T(br[9])}</p>
</div></section>

<section class="sec team"><div class="wrap">
<div class="head">
<h2>{T('Для команды')}</h2>
<div class="intro">
<p class="hook">{T(tm[0])}</p>
<p>{T(tm[1])}</p>
<p>{T(tm[2])}</p>
</div>
</div>
<div class="grid2">
{story(tm[3], sep=': ')}
{story(tm[4])}
</div>
<p class="trust">{T(tm[5])}</p>
</div></section>

<section class="sec online"><div class="wrap">
<div class="head">
<h2>{T('Про онлайн')}</h2>
<div class="intro"><p>{T(on[0])}</p></div>
</div>
</div></section>

<section class="about-sec">
<div class="apic"><img src="/_blob/75d0ee8eee8cb8e337d9ccea4b06a69f" alt="Геннадий Николаев"><div class="fr" aria-hidden="true"></div><div class="fe" aria-hidden="true"></div><div class="ft" aria-hidden="true"></div><div class="fb" aria-hidden="true"></div></div>
<div class="wrap about">
<div class="gap" aria-hidden="true"></div>
<div>
<h2>{T('Обо мне')}</h2>
<p class="text">{T(ab[0])}</p>
<p class="text2">{T(ab[1])}</p>
</div>
</div>
</section>"""
    return out

def hero(v):
    h = SECS['Шапка ' + v]
    assert h[3].startswith('Кнопка:'), h
    return T(h[0]), T(h[1]), T(h[2])

def sw(v, inner):
    """Блок, видимый только при выбранной шапке v (на полной странице)."""
    if v is None:
        return inner
    return (f'<sc-if value="{{{{is{"A" if v == "А" else "B"}}}}}" hint-placeholder-val="{{{{ {"true" if v == "А" else "false"} }}}}">'
            + inner + '</sc-if>')

def desk_text(v, switch):
    out = []
    for x in ('А', 'Б') if switch else (v,):
        h1, sub, lead = hero(x)
        out.append(sw(x if switch else None, f'<h1>{h1}</h1>\n<p class="sub">{sub}</p>\n<p class="lead">{lead}</p>'))
    return '\n'.join(out)

def phone_top(v, switch):
    out = []
    for x in ('А', 'Б') if switch else (v,):
        h1, sub, lead = hero(x)
        out.append(sw(x if switch else None, f'<h1>{h1}</h1>\n<p class="sub">{sub}</p>'))
    return '\n'.join(out)

def phone_lead(v, switch):
    out = []
    for x in ('А', 'Б') if switch else (v,):
        h1, sub, lead = hero(x)
        out.append(sw(x if switch else None, f'<p class="lead">{lead}</p>'))
    return '\n'.join(out)

LAST = SECS['Последний экран']
_b1, _, _b2 = LAST[0].rpartition('. ')
BIG = f'<p class="big">{T(_b1)}. <span>{T(_b2)}</span></p>'
CH = f'<a class="ch" href="#">{T(LAST[2].split(": ", 1)[1])}</a>'

LOGO_CSS = '''.lg{position:relative;display:inline-flex;align-items:center;justify-content:center;flex:none;border-radius:50%;overflow:hidden}
.lg svg{display:block}
.tgl svg{width:100%;height:100%}
.mxl{background:linear-gradient(45deg,#3FBAFC 0%,#2A72F8 35%,#4A3EEC 62%,#9038DA 100%)}
.mxl svg,.wal svg{width:62%;height:62%}
.wal{background:#25D366}
.mll{background:#F4F4F1}
.mll svg{width:72%;height:72%}
.phl{background:#30D158;color:#FFFFFF}
.phl svg{width:52%;height:52%}'''

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<style>
{css}
</style>
</helmet>
'''

SCRIPT = '''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{{props}"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
const s = this.state || {{}};
const b = (this.props.hero ?? 'А') === 'Б';
return {{
isA: !b,
isB: b,
open: s.open === true,
openTop: s.open === true && s.at !== 'end',
openEnd: s.open === true && s.at === 'end',
openSheet: () => this.setState({{ open: true, at: 'top' }}),
openSheet2: () => this.setState({{ open: true, at: 'end' }}),
close: () => this.setState({{ open: false }})
}};
}}
}}
</script>
</body>
</html>
'''

SHEET = '<dc-import name="Sheet2" on-close="{{close}}" tg="{{ true }}" hint-size="374px,342px"></dc-import>'
VEIL = '<button type="button" class="veil" aria-label="Закрыть" onClick="{{close}}"></button>'

# ---------- десктоп ----------
DESK_CSS = '''body{margin:0;background:#0C0C0C}
.pg{position:relative;background:#0C0C0C;color:#F1F1EF;font-family:"Manrope",system-ui,sans-serif;font-size:19px;line-height:1.6;-webkit-font-smoothing:antialiased}
p,blockquote{margin:0}
.pg a{color:#F1F1EF}
.pg button{font-family:inherit}
.wrap{width:100%;max-width:1280px;margin:0 auto;padding:0 56px;box-sizing:border-box}
''' + LOGO_CSS + '''
.hero{position:relative;height:900px;overflow:hidden}
.pic{position:absolute;top:0;right:max(0px,calc((100vw - 1440px) / 2));width:min(760px,54vw);height:900px}
.pic .fr{position:absolute;left:0;top:0;right:0;bottom:0;display:none;background:linear-gradient(to left,#0C0C0C 0%,rgba(12,12,12,0) 22%)}
.pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 34%}
.pic .fl{position:absolute;left:0;top:0;right:0;bottom:0;background:linear-gradient(to right,#0C0C0C 0%,rgba(12,12,12,0.8) 12%,rgba(12,12,12,0.2) 30%,rgba(12,12,12,0) 45%)}
.pic .fb{position:absolute;left:0;right:0;bottom:0;height:34%;background:linear-gradient(to bottom,rgba(12,12,12,0),#0C0C0C)}
.hin{position:relative;height:900px;display:flex;flex-direction:column;justify-content:center}
sc-if{display:contents}
.hero .sub{margin-top:24px;max-width:min(560px,42vw);text-wrap:pretty;font-size:clamp(24px,2.1vw,30px);line-height:1.25;font-weight:700;letter-spacing:-0.02em;color:#E9EAEA}
.hero h1,.pg h2,.big{word-spacing:0.06em}
.hero h1{margin:0;max-width:min(700px,46vw);text-wrap:balance;font-size:clamp(48px,4.45vw,64px);line-height:1.02;font-weight:800;letter-spacing:-0.045em;color:#FFFFFF}
.lead{margin-top:20px;max-width:min(560px,44vw);color:#AEB3B8}
.act{position:relative;width:min(560px,42vw);margin-top:36px}
.duo{display:grid;grid-template-columns:minmax(0,1.266fr) minmax(0,1fr);gap:10px}
.w{display:flex;align-items:center;justify-content:center;gap:12px;height:68px;padding:0 16px 0 11px;border:0;border-radius:22px;background:#1A1B1E;color:#F4F4F1;text-align:left;cursor:pointer;box-shadow:inset 0 0 0 1px #2C2E32;transition:background .15s}
.w:hover{background:#212327}
.av{position:relative;flex:none;width:48px;height:48px;border-radius:50%;overflow:hidden;background:#111111;box-shadow:0 0 0 2px #30D158}
.av img{display:block;width:100%;height:100%;object-fit:cover}
.tt{display:flex;flex-direction:column;gap:6px}
.tt b{font-size:18px;line-height:1;font-weight:800;letter-spacing:-0.01em}
.mini{display:flex;gap:4px}
.mini .lg{width:22px;height:22px}
.pg a.p{display:flex;align-items:center;justify-content:center;gap:9px;height:68px;padding:0 16px;border-radius:22px;background:#F4F4F1;color:#0C0C0C;font-size:18px;font-weight:800;letter-spacing:-0.01em;text-decoration:none;transition:background .15s}
.pg a.p:hover{background:#FFFFFF}
.p svg{width:20px;height:20px;flex:none}
.pop{position:absolute;left:0;bottom:80px;z-index:30;width:374px}
.veil{position:absolute;left:0;top:0;width:100%;height:100%;z-index:20;margin:0;padding:0;border:0;background:rgba(0,0,0,0.8);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);cursor:default}
.sec{padding-top:112px;padding-bottom:112px}
.nw{white-space:nowrap}
.tight{padding-top:0}
.step b,.case h3{text-wrap:balance}
.big,.statement,.trust,.tile,.card,.ans,.intro p,.case p,.step,.text,.kicker,.lead{text-wrap:pretty}
.pg h2{text-wrap:balance;font-size:clamp(44px,3.9vw,56px);line-height:1.02;font-weight:800;letter-spacing:-0.04em;margin:0;color:#FFFFFF}
.head{display:grid;grid-template-columns:5fr 7fr;gap:72px;align-items:start}
.head .intro{max-width:620px;color:#A9AEB3;padding-top:10px}
.head .intro p+p{margin-top:16px}
.bento{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:20px;margin-top:56px}
.tile{background:#18191B;border-radius:24px;padding:32px 34px;font-size:24px;line-height:1.36;font-weight:600;letter-spacing:-0.015em}
.s6{grid-column:span 6}
.s7{grid-column:span 7}
.s8{grid-column:span 8}
.s4{grid-column:span 4}
.s5{grid-column:span 5}
.statement{font-size:clamp(30px,2.9vw,40px);line-height:1.2;font-weight:700;letter-spacing:-0.03em;margin-top:80px;max-width:1040px}
.inv{background:#151618;color:#E9EAEA;border-top:1px solid #232528;border-bottom:1px solid #232528}
.pairs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:56px}
.pair{border:1px solid #2B2F34;border-radius:22px;padding:32px 34px;display:flex;flex-direction:column;gap:18px}
.req{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:19px;line-height:1.5;font-weight:500}
.ans{color:#C9CDD1;font-size:18px}
.trust{margin-top:64px;font-size:30px;line-height:1.3;font-weight:700;letter-spacing:-0.02em;color:#FFFFFF;max-width:1000px}
.opt-title{font-size:32px;line-height:1.2;font-weight:800;letter-spacing:-0.03em;margin-top:64px}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:28px}
.three .tile{font-size:23px;min-height:150px;box-sizing:border-box}
.acc{color:#E4570F}
.req{color:#E4570F}
.now .wide{max-width:900px}
.kicker{margin-top:24px;max-width:900px;font-size:28px;line-height:1.3;font-weight:700;letter-spacing:-0.02em;color:#D7DADD}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:56px}
.card{background:#18191B;border-radius:24px;padding:32px 34px;font-size:22px;line-height:1.45;font-weight:500;letter-spacing:-0.01em;color:#E9EAEA}
.pair.note{background:#1C1D20;border-color:#1C1D20;justify-content:center}
.pair.note .ans{color:#E9EAEA}
.team .grid2 .ans{font-size:19px}
.case.full{grid-column:1 / -1;display:grid;grid-template-columns:1fr 1fr;gap:16px 88px;align-items:start}
.case.full h3{margin:0}
.pair.note .ans{max-width:640px}
.pairs .pair.note{grid-column:1 / -1}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:56px}
.step{background:#18191B;border-radius:24px;padding:32px 34px;font-size:19px;line-height:1.55;color:#C9CDD1}
.step b{display:block;margin-bottom:12px;font-size:23px;line-height:1.3;font-weight:800;letter-spacing:-0.02em;color:#FFFFFF}
.online .head .intro{font-size:24px;line-height:1.45;font-weight:600;letter-spacing:-0.01em;color:#D7DADD;padding-top:6px}
.after{display:grid;grid-template-columns:5fr 7fr;gap:72px;margin-top:48px}
.after p{grid-column:2;max-width:620px;color:#A9AEB3}
.cases{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:56px}
.case{background:#18191B;border-radius:24px;padding:32px 34px}
.case h3{font-size:25px;line-height:1.28;font-weight:800;letter-spacing:-0.025em;margin:0 0 16px}
.case p{color:#A9AEB3;font-size:18px}
.about-sec{position:relative;overflow:hidden}
.apic{position:absolute;top:0;left:max(0px,calc((100vw - 1440px) / 2));width:min(720px,50vw);height:100%}
.apic .fe{position:absolute;left:0;top:0;right:0;bottom:0;display:none;background:linear-gradient(to right,#0C0C0C 0%,rgba(12,12,12,0) 22%)}
.apic img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 55%}
.apic .fr{position:absolute;left:0;top:0;right:0;bottom:0;background:linear-gradient(to left,#0C0C0C 0%,rgba(12,12,12,0.8) 12%,rgba(12,12,12,0.2) 30%,rgba(12,12,12,0) 45%)}
.apic .ft{position:absolute;left:0;right:0;top:0;height:24%;background:linear-gradient(to top,rgba(12,12,12,0),#0C0C0C)}
.apic .fb{position:absolute;left:0;right:0;bottom:-1px;height:48%;background:linear-gradient(to bottom,rgba(12,12,12,0) 0%,rgba(12,12,12,0.75) 55%,#0C0C0C 100%)}
.about{position:relative;display:grid;grid-template-columns:5fr 7fr;gap:72px;align-items:center;min-height:560px}
.sec.online{padding-bottom:0}
.about .text{font-size:28px;line-height:1.42;font-weight:600;letter-spacing:-0.02em;margin-top:28px;max-width:640px}
.final{padding:48px 0 128px}
.big{font-size:clamp(56px,5.6vw,72px);line-height:1.02;font-weight:800;letter-spacing:-0.045em;max-width:1120px;color:#FFFFFF}
.big span{color:#6F757B}
.tiles{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.5fr) minmax(0,1.3fr);gap:14px;margin-top:56px}
.pg a.ct{display:flex;flex-direction:column;justify-content:space-between;gap:28px;min-height:184px;padding:22px 22px 24px;border-radius:24px;background:#141517;color:#F1F1EF;text-decoration:none;box-sizing:border-box;box-shadow:inset 0 0 0 1px #232528;transition:transform .15s,background .15s}
.pg a.ct:hover{transform:translateY(-2px);background:#191A1D}
.ct .lg{width:46px;height:46px}
.ct .t{display:flex;flex-direction:column;gap:2px}
.ct .sub{font-size:14px;font-weight:700;color:#8E9399}
.ct .nm{font-size:21px;line-height:1.2;font-weight:800;letter-spacing:-0.02em;white-space:nowrap}
.ct .nm.sm{font-size:21px;line-height:1.2;letter-spacing:-0.02em}
.ch{display:inline-block;margin-top:30px;padding:10px 0;font-size:18px;font-weight:600;text-decoration:underline;text-underline-offset:4px}
.grid2.five{grid-template-columns:repeat(6,minmax(0,1fr))}
.grid2.five .card{grid-column:span 2}
.grid2.five .card:nth-child(n+4){grid-column:span 3}
.stories{display:flex;flex-direction:column;gap:20px;margin-top:56px}
.story{border:1px solid #2B2F34;border-radius:22px;padding:32px 34px}
.story h3{font-size:25px;line-height:1.28;font-weight:800;letter-spacing:-0.025em;margin:0 0 16px;color:#FFFFFF;text-wrap:balance}
.story p{color:#C9CDD1;font-size:18px;text-wrap:pretty}
.story.full{display:grid;grid-template-columns:5fr 7fr;gap:16px 72px;align-items:start}
.story.full h3{margin:0}
.story.full p{max-width:680px}
.team .trust{margin-top:56px}
.now .trust{margin-top:56px}
.work .trust{margin-top:56px;max-width:1040px}
.work .three{margin-top:40px}
.work .card,.inv .card{background:transparent;border:1px solid #2B2F34;font-size:20px;line-height:1.5}
.pairs.five{grid-template-columns:repeat(6,minmax(0,1fr))}
.pairs.five .pair{grid-column:span 2}
.pairs.five .pair:nth-child(n+4){grid-column:span 3}
.stories .pair.note{padding:32px 34px}
.stories .pair.note .ans{font-size:22px;line-height:1.45;font-weight:600;max-width:900px}
.team .intro .hook{font-size:24px;line-height:1.4;font-weight:700;color:#E9EAEA}
.about .text2{margin-top:20px;max-width:640px;color:#A9AEB3;font-size:19px}
.final .act{margin-top:48px}
@media (min-width:1441px){.pic .fr,.apic .fe{display:block}}
@media (max-width:1279px){.steps{grid-template-columns:1fr;gap:16px}.step{display:grid;grid-template-columns:5fr 7fr;gap:12px 48px;align-items:start}.step b{margin:0}.sec.online{padding-bottom:40px}}
@media (max-width:1279px){.pairs.five{grid-template-columns:repeat(2,minmax(0,1fr))}.pairs.five .pair,.pairs.five .pair:nth-child(n+4){grid-column:auto}.pairs.five .pair:last-child{grid-column:1 / -1}.work .three{grid-template-columns:1fr}}
@media (max-width:1279px){.grid2.five{grid-template-columns:repeat(2,minmax(0,1fr))}.grid2.five .card,.grid2.five .card:nth-child(n+4){grid-column:auto}.grid2.five .card:last-child{grid-column:1 / -1}}
@media (max-width:1279px){.tiles{grid-template-columns:repeat(6,minmax(0,1fr))}.pg a.ct{grid-column:span 2}.pg a.ct:nth-child(n+4){grid-column:span 3}}'''

PROPS = '"hero":{"editor":"enum","options":["А","Б"],"default":"А","section":"Шапка"},'

def desk(h, v='А', full=True, offset=0):
    switch = full
    clip = f' style="margin-top: -{offset}px"' if offset else ''
    body = f'''<div class="pg"{clip}>

<header class="hero">
<div class="pic"><img src="{P1}" alt="Геннадий Николаев"><div class="fl" aria-hidden="true"></div><div class="fr" aria-hidden="true"></div><div class="fb" aria-hidden="true"></div></div>
<div class="wrap hin">
{desk_text(v, switch)}
<div class="act">
<div class="duo">
{WRITE_BTN}
{CALL_BTN}
</div>
{OPEN('openTop')}
<div class="pop">{SHEET}</div>
</sc-if>
</div>
</div>
</header>
{(chr(10) + middle_html() + chr(10) + chr(10) + '<section class="final">' + chr(10) + '<div class="wrap">' + chr(10) + BIG + chr(10) + '<div class="act"><div class="duo">' + WRITE_BTN2 + CALL_BTN + '</div>' + OPEN('openEnd') + '<div class="pop">' + SHEET + '</div></sc-if></div>' + chr(10) + CH + chr(10) + '</div>' + chr(10) + '</section>' + chr(10)) if full else ''}

<sc-if value="{{{{open}}}}" hint-placeholder-val="{{{{ false }}}}">
{VEIL}
</sc-if>

</div>
'''
    title = ('Итог А/Б — компьютер, низ' if offset else 'Итог А/Б — компьютер') if full else f'Шапка {v} — компьютер'
    return HEAD.format(title=title, css=DESK_CSS) + body + SCRIPT.format(w=1440, h=h, props=PROPS if full else '')

# ---------- телефон ----------
PHONE_CSS = '''body{margin:0;background:#0C0C0C}
.m{position:relative;width:100%;background:#0C0C0C;color:#F1F1EF;font-family:"Manrope",system-ui,sans-serif;font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-wrap:break-word}
p,blockquote{margin:0}
.m a{color:#F1F1EF}
.m button{font-family:inherit}
''' + LOGO_CSS + '''
.hero{padding-bottom:36px}
.shot{position:relative;height:clamp(400px,100vw,560px);overflow:hidden}
.shot img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 66%}
.shot .fade{position:absolute;left:0;right:0;bottom:-1px;height:58%;background:linear-gradient(to bottom,rgba(12,12,12,0) 0%,rgba(12,12,12,0.7) 55%,#0C0C0C 100%)}
.in{position:relative;z-index:1;margin-top:-108px;padding:0 20px}
sc-if{display:contents}
.in .sub{margin-top:14px;text-wrap:balance;font-size:22px;line-height:1.28;font-weight:700;letter-spacing:-0.02em;color:#E9EAEA}
.in h1{margin:0;font-size:min(36px,9.4vw);overflow-wrap:normal;word-spacing:0.06em;text-wrap:balance;line-height:1.02;font-weight:800;letter-spacing:-0.045em;color:#FFFFFF}
.lead{margin-top:24px;color:#AEB3B8}
.duo{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin-top:24px}
.w{display:flex;align-items:center;justify-content:center;gap:11px;height:64px;padding:0 14px 0 10px;border:0;border-radius:20px;background:#1A1B1E;color:#F4F4F1;text-align:left;cursor:pointer;box-shadow:inset 0 0 0 1px #2C2E32}
.av{position:relative;flex:none;width:44px;height:44px;border-radius:50%;overflow:hidden;background:#111111;box-shadow:0 0 0 2px #30D158}
.av img{display:block;width:100%;height:100%;object-fit:cover}
.tt{display:flex;flex-direction:column;gap:5px}
.tt b{font-size:17px;line-height:1;font-weight:800;letter-spacing:-0.01em}
.mini{display:flex;gap:4px}
.mini .lg{width:20px;height:20px}
.m a.p{display:flex;align-items:center;gap:8px;height:64px;padding:0 18px 0 15px;border-radius:20px;background:#F4F4F1;color:#0C0C0C;font-size:17px;font-weight:800;letter-spacing:-0.01em;text-decoration:none}
.p svg{width:19px;height:19px;flex:none}
.veil{position:absolute;left:0;top:0;width:100%;height:100%;z-index:20;margin:0;padding:0;border:0;background:rgba(0,0,0,0.86);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);cursor:default}
.scr{position:absolute;left:0;right:0;top:0;height:844px;z-index:30;pointer-events:none}
@media (max-height:1400px){.scr{height:100svh}}
.sp{position:absolute;left:8px;right:8px;bottom:8px;margin:0 auto;pointer-events:auto}
.wrap{padding:0 20px}
.sec{padding:64px 0}
.m h2{font-size:min(34px,8.6vw);line-height:1.1;font-weight:800;letter-spacing:-0.04em;margin:0;color:#FFFFFF}
.intro{color:#A9AEB3;margin-top:18px}
.intro p+p{margin-top:16px}
.bento,.grid2,.pairs,.three,.cases{display:flex;flex-direction:column;gap:14px;margin-top:32px}
.three{margin-top:20px}
.tile{background:#18191B;border-radius:20px;padding:24px 22px;font-size:20px;line-height:1.36;font-weight:600;letter-spacing:-0.015em}
.statement{font-size:min(26px,6.7vw);line-height:1.2;font-weight:700;letter-spacing:-0.03em;margin-top:48px}
.acc{color:#E4570F}
.kicker{margin-top:18px;font-size:22px;line-height:1.3;font-weight:700;letter-spacing:-0.02em;color:#D7DADD}
.card{background:#18191B;border-radius:20px;padding:24px 22px;font-size:18px;line-height:1.5;font-weight:500;color:#E9EAEA}
.inv{background:#151618;color:#E9EAEA;border-top:1px solid #232528;border-bottom:1px solid #232528}
.pair{border:1px solid #2B2F34;border-radius:20px;padding:24px 22px;display:flex;flex-direction:column;gap:16px}
.pair.note{background:#1C1D20;border-color:#1C1D20}
.pair.note .ans{color:#E9EAEA}
.online .intro{font-size:20px;line-height:1.45;font-weight:600;color:#D7DADD}
.req{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:18px;line-height:1.5;font-weight:500;color:#E4570F}
.ans{color:#C9CDD1;font-size:17px}
.trust{margin-top:40px;font-size:22px;line-height:1.3;font-weight:700;letter-spacing:-0.02em;color:#FFFFFF}
.opt-title{font-size:24px;line-height:1.2;font-weight:800;letter-spacing:-0.03em;margin-top:40px}
.after{margin-top:32px}
.steps{display:flex;flex-direction:column;gap:14px;margin-top:32px}
.step{background:#18191B;border-radius:20px;padding:24px 22px;font-size:17px;line-height:1.55;color:#C9CDD1}
.step b{display:block;margin-bottom:10px;font-size:20px;line-height:1.3;font-weight:800;letter-spacing:-0.02em;color:#FFFFFF}
.after p{color:#A9AEB3}
.case{background:#18191B;border-radius:20px;padding:26px 22px}
.stories{display:flex;flex-direction:column;gap:14px;margin-top:32px}
.work .card,.inv .card{background:transparent;border:1px solid #2B2F34}
.work .three{margin-top:28px}
.stories .pair.note .ans{font-size:19px;line-height:1.45;font-weight:600}
.team .intro .hook{font-size:20px;line-height:1.4;font-weight:700;color:#E9EAEA}
.about .text2{margin-top:16px;color:#A9AEB3;font-size:17px}
.final .duo{margin-top:32px}
.scr.end{top:auto;bottom:0}
.story{border:1px solid #2B2F34;border-radius:20px;padding:24px 22px}
.story h3{font-size:21px;line-height:1.28;font-weight:800;letter-spacing:-0.025em;margin:0 0 14px;color:#FFFFFF;text-wrap:balance}
.story p{color:#C9CDD1;font-size:17px;text-wrap:pretty}
.case h3{font-size:21px;line-height:1.28;font-weight:800;letter-spacing:-0.025em;margin:0 0 14px}
.case p{color:#A9AEB3;font-size:17px}
.apic{position:relative;height:500px;overflow:hidden}
.apic img{position:absolute;display:block;width:128%;max-width:none;height:auto;left:-14%;top:calc(90px - 59.5vw)}
.apic .fe{display:none}
.sec.online{padding-bottom:16px}
.nw{white-space:nowrap}
.tight{padding-top:32px}
.m h2,.big{word-spacing:0.06em}
.apic .fr{display:none}
.apic .ft{position:absolute;left:0;right:0;top:-1px;height:26%;background:linear-gradient(to top,rgba(12,12,12,0),#0C0C0C)}
.apic .fb{position:absolute;left:0;right:0;bottom:-1px;height:58%;background:linear-gradient(to bottom,rgba(12,12,12,0) 0%,rgba(12,12,12,0.7) 55%,#0C0C0C 100%)}
.about{position:relative;z-index:1;margin-top:-120px;padding-bottom:64px}
.about .gap{display:none}
.about .text{font-size:22px;line-height:1.42;font-weight:600;letter-spacing:-0.02em;margin-top:18px}
.final{padding:40px 0 80px}
.big{font-size:38px;line-height:1.04;font-weight:800;letter-spacing:-0.045em;color:#FFFFFF}
.big span{color:#6F757B}
.tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:36px}
.m a.ct{display:flex;flex-direction:column;justify-content:space-between;gap:18px;min-height:136px;padding:16px 16px 18px;border-radius:20px;background:#141517;color:#F1F1EF;text-decoration:none;box-sizing:border-box;box-shadow:inset 0 0 0 1px #232528}
.ct .lg{width:40px;height:40px}
.ct .t{display:flex;flex-direction:column;gap:2px}
.ct .sub{font-size:13px;font-weight:700;color:#8E9399}
.ct .nm{font-size:20px;line-height:1.2;font-weight:800;letter-spacing:-0.02em}
.ct .t{min-height:70px}
.m a.ct.wide .t{min-height:0}
.m a.ct.wide .nm{white-space:nowrap}
.ct .nm.sm{font-size:min(20px,5vw);line-height:1.2;letter-spacing:-0.02em}
.m a.ct.wide{grid-column:1 / -1;min-height:0;flex-direction:row;align-items:center;justify-content:flex-start;gap:14px}
.ch{display:inline-block;margin-top:22px;padding:10px 0;font-size:17px;font-weight:600;text-decoration:underline;text-underline-offset:4px}
.m h2,.step b,.case h3{text-wrap:balance}
.big,.statement,.trust,.tile,.card,.ans,.intro p,.case p,.step,.text,.kicker,.lead,.after p{text-wrap:pretty}
@media (max-width:374px){.w{gap:9px;padding:0 10px 0 9px}.mini{gap:3px}.mini .lg{width:18px;height:18px}.m a.p{padding:0 14px 0 12px;gap:6px}}
@media (min-width:600px){.in,.wrap{max-width:600px;margin-left:auto;margin-right:auto;box-sizing:border-box}.sp{max-width:560px}.duo{grid-template-columns:minmax(0,1.266fr) minmax(0,1fr)}.w{justify-content:center}.m a.p{justify-content:center}.shot{height:min(75vw,720px)}.shot img{object-position:50% 52%}.big{font-size:36px}.veil{background:rgba(0,0,0,0.92)}.apic{height:600px}.apic img{position:static;width:100%;height:100%;object-fit:cover;object-position:50% 50%}}'''

def phone(h, v='А', full=True, offset=0):
    switch = full
    clip = (f' style="margin-top: -{offset}px"' if offset else '') if full else ' style="height: 844px; overflow: hidden"'
    body = f'''<div class="m"{clip}>

<header class="hero">
<div class="shot"><img src="{P1}" alt="Геннадий Николаев"><div class="fade" aria-hidden="true"></div></div>
<div class="in">
{phone_top(v, switch)}
<div class="duo">
{WRITE_BTN}
{CALL_BTN}
</div>
{phone_lead(v, switch)}
</div>
</header>
{(chr(10) + middle_html() + chr(10) + chr(10) + '<section class="final"><div class="wrap">' + chr(10) + BIG + chr(10) + '<div class="duo">' + WRITE_BTN2 + CALL_BTN + '</div>' + chr(10) + CH + chr(10) + '</div></section>' + chr(10)) if full else ''}

<sc-if value="{{{{open}}}}" hint-placeholder-val="{{{{ false }}}}">
{VEIL}
</sc-if>
{OPEN('openTop')}
<div class="scr"><div class="sp">{SHEET}</div></div>
</sc-if>
{OPEN('openEnd')}
<div class="scr end"><div class="sp">{SHEET}</div></div>
</sc-if>

</div>
'''
    title = ('Итог А/Б — телефон, низ' if offset else 'Итог А/Б — телефон') if full else f'Шапка {v} — телефон'
    return HEAD.format(title=title, css=PHONE_CSS) + body + SCRIPT.format(w=390, h=h, props=PROPS if full else '')

if __name__ == '__main__':
    import sys
    hd, hp = int(sys.argv[1]), int(sys.argv[2])
    suf = sys.argv[3] if len(sys.argv) > 3 else '4'
    (P / f'FinalDesk{suf}.dc.html').write_text(desk(hd))
    (P / f'FinalPhone{suf}.dc.html').write_text(phone(hp))
    if len(sys.argv) > 4:
        off = int(sys.argv[4])
        (P / f'FinalPhone{suf}End.dc.html').write_text(phone(hp - off, offset=off))
    if len(sys.argv) > 5:
        off = int(sys.argv[5])
        (P / f'FinalDesk{suf}End.dc.html').write_text(desk(hd - off, offset=off))
    for v, lat in (('А', 'A'), ('Б', 'B')):
        (P / f'HeroDesk{lat}{suf}.dc.html').write_text(desk(900, v, full=False))
        (P / f'HeroPhone{lat}{suf}.dc.html').write_text(phone(844, v, full=False))
    print('ok', suf)
