"""Живые страницы А/Б на nikolaev-mentor.ru/ai/ из того же макета, что на холсте дизайна.

python3 build_site.py — пишет в ~/Dev/consulting/teen-mentor/ai/:
  a/index.html  — шапка А,  b/index.html — шапка Б,
  index.html    — общий адрес: делит посетителей поровну и запоминает выбор,
  tg-avatar.jpg — аватарка для кнопки «Написать».
Текст — ~/Dev/nikolaev-ai/landing-text-ab.md. Вёрстка — build_ab.py (одна на холст и сайт).
"""
import re, sys, shutil, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_ab as B

OUT = pathlib.Path('/Users/kenneth/Dev/consulting/teen-mentor/ai')
BASE = 'https://nikolaev-mentor.ru/ai/'
IMG = {
    B.AV: '/ai/tg-avatar.jpg',
    B.P1: '/portrait-1.webp',
    '/_blob/75d0ee8eee8cb8e337d9ccea4b06a69f': '/portrait-2.webp',
}
METRIKA = 106335095

def parts(dc, hero):
    """Стиль и разметка из .dc.html: другая шапка убрана, окошко «Написать» спрятано до нажатия."""
    style = re.search(r'<style>(.*?)</style>', dc, re.S).group(1)
    body = dc.split('<x-dc>')[1].split('</x-dc>')[0]
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
    other = 'isB' if hero == 'А' else 'isA'
    body = re.sub(r'<sc-if value="\{\{' + other + r'\}\}".*?</sc-if>', '', body, flags=re.S)
    body = re.sub(r'<sc-if value="\{\{open\}\}"[^>]*>(.*?)</sc-if>', r'<div data-open hidden>\1</div>', body, flags=re.S)
    sheet = (HERE / 'design/project/Sheet2.dc.html').read_text().split('<x-dc>')[1].split('</x-dc>')[0]
    sheet = re.sub(r'<helmet>.*?</helmet>', '', sheet, flags=re.S)
    sheet = re.sub(r'<sc-if value="\{\{studio\}\}".*?</sc-if>', '', sheet, flags=re.S)
    # Ника в Instagram пока нет — строку-заглушку на живой странице не показываем
    sheet = re.sub(r'<a [^>]*href="#"[^>]*>.*?</a>', '', sheet, flags=re.S)
    body = re.sub(r'<dc-import name="Sheet2"[^>]*></dc-import>', lambda m: sheet, body)
    body = re.sub(r'<sc-if[^>]*>|</sc-if>', '', body)
    body = body.replace('onClick="{{openSheet}}"', 'data-openbtn').replace('aria-expanded="{{open}}"', 'aria-expanded="false"')
    body = body.replace('onClick="{{close}}"', 'data-close')
    # Адреса Telegram-канала пока нет — ссылку-заглушку на живой странице не показываем
    body = re.sub(r'<a class="ch" href="#">.*?</a>', '', body, flags=re.S)
    for k, v in IMG.items():
        body = body.replace(k, v)
    assert '{{' not in body and '_blob' not in body, re.findall(r'.{40}(?:\{\{|_blob).{40}', body)[:3]
    return style, body.strip()

def page(hero):
    lat = 'a' if hero == 'А' else 'b'
    ds, db = parts(B.desk(900, hero), hero)
    ps, pb = parts(B.phone(844, hero), hero)
    h1, sub, lead = (re.sub(r'<[^>]+>', '', x).replace(' ', ' ') for x in B.hero(hero))
    css = ('@media (min-width:1024px){\n' + ds + '\n}\n@media (max-width:1023px){\n' + ps + '\n}\n'
           '@media (max-width:1023px){.pg{display:none}}\n@media (min-width:1024px){.m{display:none}}\n'
           'html,body{margin:0;background:#0C0C0C}\n'
           '.veil{position:fixed !important;left:0;top:0;width:100% !important;height:100% !important}\n'
           '.scr{position:fixed !important}\n[hidden]{display:none !important}')
    js = f'''(function(){{
var V='{lat.upper()}';
function ym_(){{try{{ym({METRIKA},'reachGoal',arguments[0],{{ai_variant:V}})}}catch(e){{}}}}
try{{ym({METRIKA},'params',{{ai_variant:V}})}}catch(e){{}}
function set(open,root){{
  document.querySelectorAll('[data-open]').forEach(function(x){{if(!open||root.contains(x))x.hidden=!open}});
  document.querySelectorAll('[data-openbtn]').forEach(function(b){{b.setAttribute('aria-expanded',open&&root.contains(b)?'true':'false')}});
}}
document.addEventListener('click',function(e){{
  var b=e.target.closest('[data-openbtn]');
  if(b){{set(true,b.closest('.pg,.m'));ym_('ai_open');return}}
  if(e.target.closest('[data-close]')){{set(false);return}}
  var a=e.target.closest('a[href]');
  if(a){{var h=a.getAttribute('href');
    ym_(h.indexOf('tel:')==0?'ai_call':h.indexOf('mailto:')==0?'ai_mail':h.indexOf('t.me')>-1?'ai_tg':h.indexOf('wa.me')>-1?'ai_wa':h.indexOf('max.ru')>-1?'ai_max':'ai_link')}}
}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')set(false)}});
}})();'''
    html = f'''<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow, noarchive, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h1} — Геннадий Николаев</title>
<meta name="description" content="{sub}">
<link rel="canonical" href="{BASE}{lat}/">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{lat}/">
<meta property="og:title" content="{h1}">
<meta property="og:description" content="{sub}">
<meta property="og:image" content="https://nikolaev-mentor.ru/portrait-1.jpeg">
<meta property="og:locale" content="ru_RU">
<meta name="theme-color" content="#0C0C0C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<!-- Yandex.Metrika counter -->
<script async src="https://mc.yandex.ru/metrika/tag.js?id={METRIKA}"></script><script>
(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})
(window,document,'script','https://mc.yandex.ru/metrika/tag.js?id={METRIKA}','ym');
ym({METRIKA},'init',{{ssr:true,webvisor:true,clickmap:true,referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA}" style="position:absolute;left:-9999px;" alt=""></div></noscript>
<!-- /Yandex.Metrika counter -->
<style>
{css}
</style>
</head>
<body>
{db}
{pb}
<script>
{js}
</script>
</body>
</html>
'''
    (OUT / lat).mkdir(parents=True, exist_ok=True)
    (OUT / lat / 'index.html').write_text(html)

SPLIT = '''<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow, noarchive, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ИИ для руководителей и команд — Геннадий Николаев</title>
<style>html,body{margin:0;background:#0C0C0C;color:#F1F1EF;font-family:system-ui,sans-serif}</style>
<script>
(function(){
  var v;
  try{v=localStorage.getItem('ai_ab')}catch(e){}
  if(v!=='a'&&v!=='b'){v=Math.random()<0.5?'a':'b';try{localStorage.setItem('ai_ab',v)}catch(e){}}
  location.replace('/ai/'+v+'/'+location.search+location.hash);
})();
</script>
</head>
<body><noscript><p style="padding:24px"><a href="/ai/a/" style="color:#F1F1EF">ИИ для руководителей и команд</a></p></noscript></body>
</html>
'''

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for h in ('А', 'Б'):
        page(h)
    (OUT / 'index.html').write_text(SPLIT)
    shutil.copy(HERE / 'photos/tg-avatar.jpg', OUT / 'tg-avatar.jpg')
    r = subprocess.run([sys.executable, str(HERE / 'checktext_ab.py'), f'{OUT}/a/index.html:А:full', f'{OUT}/b/index.html:Б:full'],
                       capture_output=True, text=True)
    print(r.stdout)
    miss_ok = all("нет на странице: ['Telegram-канал, где я выкладываю вкусняшки из работы']" in l or "нет на странице: []" in l
                  for l in r.stdout.splitlines() if '|' in l) and "лишнее: []" in r.stdout and r.stdout.count("лишнее: []") == 2
    if not miss_ok:
        sys.exit('ТЕКСТ НЕ СОВПАДАЕТ с landing-text-ab.md')
    print('ok:', OUT)
