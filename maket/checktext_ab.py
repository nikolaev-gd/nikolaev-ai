"""Сверка текста с landing-text-ab.md. Аргументы: файл:шапка (А, Б или -), шапка - — без шапки."""
import re, html.parser, pathlib, sys
src = pathlib.Path('/Users/kenneth/Dev/nikolaev-ai/landing-text-ab.md').read_text()
norm = lambda s: re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()
ALLOW = {'Написать', 'Позвонить', 'Telegram', 'Max', 'WhatsApp', 'Почта', 'Написать в', 'nikolaev.gd@', 'gmail.com', '+7 995 509-82-67', '@nikolaev_gd', 'nikolaev.gd@gmail.com', 'Наставник по ИИ для руководителей и команд — Геннадий Николаев'}
secs = {}
for chunk in re.split(r'^## ', src, flags=re.M)[1:]:
    t, _, rest = chunk.partition('\n')
    secs[t.strip()] = [norm(p) for p in rest.split('\n\n') if p.strip()]
def paras(hero, body):
    out = []
    if hero in ('А', 'Б'):
        out += [p for p in secs['Шапка ' + hero] if not p.startswith('Кнопка:')]
    if body:
        for t, ps in secs.items():
            if t.startswith('Шапка'): continue
            if t != 'Последний экран': out.append(t)
            for p in ps:
                if p.startswith(('Кнопка:', 'Кнопки:')): continue
                out.append(p.split(': ', 1)[1] if p.startswith('Ещё:') else p)
    return out
class T(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.out = []; s.skip = 0
    def handle_starttag(s, t, a):
        if t in ('style', 'script', 'svg'): s.skip += 1
    def handle_endtag(s, t):
        if t in ('style', 'script', 'svg'): s.skip -= 1
    def handle_data(s, d):
        if not s.skip and d.strip(): s.out.append(norm(d))
ok = True
for arg in sys.argv[1:]:
    f, hero, body = arg.split(':')
    want = paras(hero, body == 'full')
    t = T(); t.feed(pathlib.Path(f).read_text()); page = ' '.join(t.out)
    bad = [x for x in t.out if x not in ALLOW and not any(x in p for p in want)]
    flat = re.sub(r'\s+', '', page)
    miss = [p[:60] for p in want if re.sub(r'\s+', '', p) not in flat]
    print(f'{f} [{hero}] | лишнее: {bad} | нет на странице: {miss}')
    ok = ok and not bad and not miss
print('ВСЁ СОВПАДАЕТ' if ok else 'ЕСТЬ РАСХОЖДЕНИЯ')
