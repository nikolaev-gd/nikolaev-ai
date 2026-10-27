#!/usr/bin/env python3
"""Собирает index.html из landing-text.md.

Текст берётся дословно: каждое слово страницы — из landing-text.md.
Правила разметки файла:
  - «## Заголовок» — раздел страницы. «Первый экран» и «Последний экран» —
    служебные названия, на странице не показываются.
  - В «Первом экране» первый абзац — заголовок страницы (h1), второй — подзаголовок.
  - «Кнопка: Текст» — кнопка со ссылкой на Telegram.
  - «Ещё: Текст» — обычная ссылка на Telegram-канал.
  - Абзац целиком в «ёлочках» («…».) — цитата.

После сборки скрипт сам сверяет текст страницы с файлом и падает, если они разошлись.

Запуск:  python3 build.py
"""

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "landing-text.md"
OUT = ROOT / "tmp" / "old-index.html"  # старый одностраничник; корень сайта теперь собирает maket/build_site.py

TELEGRAM_URL = "https://t.me/nikolaev_gd"
CHANNEL_URL = "#"  # ЗАГЛУШКА: адрес Telegram-канала Геннадий назовёт позже

QUOTE_RE = re.compile(r"^«[^»]*»\.?$")


# ---------- разбор landing-text.md ----------

def parse(text):
    """Возвращает список разделов: {"title": str, "items": [(kind, text), ...]}."""
    sections = []
    current = None
    buf = []

    def flush():
        if buf and current is not None:
            para = " ".join(s.strip() for s in buf)
            if para.startswith("Кнопка:"):
                current["items"].append(("button", para[len("Кнопка:"):].strip()))
            elif para.startswith("Ещё:"):
                current["items"].append(("channel", para[len("Ещё:"):].strip()))
            elif QUOTE_RE.match(para):
                current["items"].append(("quote", para))
            else:
                current["items"].append(("p", para))
        buf.clear()

    for line in text.splitlines():
        if line.startswith("# "):
            continue  # название файла, не страницы
        if line.startswith("## "):
            flush()
            current = {"title": line[3:].strip(), "items": []}
            sections.append(current)
            continue
        if not line.strip():
            flush()
            continue
        buf.append(line)
    flush()
    return sections


# ---------- сборка HTML ----------

def esc(s):
    return html.escape(s, quote=False)


def render_items(items):
    out = []
    for kind, text in items:
        if kind == "p":
            out.append(f"<p>{esc(text)}</p>")
        elif kind == "quote":
            out.append(f"<blockquote><p>{esc(text)}</p></blockquote>")
        elif kind == "button":
            out.append(
                f'<p class="cta"><a class="btn" href="{TELEGRAM_URL}" '
                f'target="_blank" rel="noopener">{esc(text)}</a></p>'
            )
        elif kind == "channel":
            out.append(
                f'<p class="channel"><a href="{CHANNEL_URL}" '
                f'target="_blank" rel="noopener">{esc(text)}</a></p>'
            )
    return "\n".join(out)


def render(sections):
    first, *middle, last = sections
    assert first["title"] == "Первый экран", first["title"]
    assert last["title"] == "Последний экран", last["title"]

    h1 = first["items"][0][1]
    lead = first["items"][1][1]
    hero = (
        f"<h1>{esc(h1)}</h1>\n"
        f'<p class="lead">{esc(lead)}</p>\n'
        + render_items(first["items"][2:])
    )

    body_sections = []
    for sec in middle:
        body_sections.append(
            f"<section>\n<h2>{esc(sec['title'])}</h2>\n{render_items(sec['items'])}\n</section>"
        )
    final = f'<section class="final">\n{render_items(last["items"])}\n</section>'

    # Описание для поисковиков и мессенджеров — первые два предложения подзаголовка, дословно.
    description = " ".join(lead.split(". ")[:2]).rstrip(".") + "."

    return TEMPLATE.format(
        title=html.escape(h1),
        description=html.escape(description),
        hero=hero,
        sections="\n\n".join(body_sections),
        final=final,
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:locale" content="ru_RU">
<meta name="theme-color" content="#faf9f6">
<link rel="icon" href="data:,">
<style>
:root {{
  --bg: #faf9f6;
  --text: #1f1f1d;
  --muted: #55534e;
  --rule: #e2ded5;
  --accent: #1a5dab;
  --accent-dark: #154c8c;
}}
html {{
  -webkit-text-size-adjust: 100%;
  background: var(--bg);
}}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 20px;
  line-height: 1.6;
  overflow-wrap: break-word;
}}
main {{
  max-width: 640px;
  margin: 0 auto;
  padding: 72px 24px 96px;
}}
h1 {{
  font-size: 40px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0 0 24px;
}}
h2 {{
  font-size: 28px;
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.005em;
  margin: 72px 0 20px;
}}
p {{
  margin: 0 0 20px;
}}
.lead {{
  margin-bottom: 32px;
}}
blockquote {{
  margin: 28px 0;
  padding: 2px 0 2px 20px;
  border-left: 3px solid var(--rule);
  color: var(--muted);
}}
blockquote p {{
  margin: 0;
}}
.cta {{
  margin: 32px 0 0;
}}
.btn {{
  display: inline-block;
  padding: 16px 30px;
  border-radius: 12px;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  line-height: 1.3;
  text-decoration: none;
}}
.btn:hover {{
  background: var(--accent-dark);
}}
.final {{
  margin-top: 80px;
  padding-top: 48px;
  border-top: 1px solid var(--rule);
}}
.channel {{
  margin: 28px 0 0;
}}
.channel a {{
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 3px;
}}
a:focus-visible {{
  outline: 3px solid var(--accent);
  outline-offset: 3px;
}}
@media (max-width: 520px) {{
  body {{
    font-size: 18px;
  }}
  main {{
    padding: 40px 20px 72px;
  }}
  h1 {{
    font-size: 30px;
    margin-bottom: 20px;
  }}
  h2 {{
    font-size: 24px;
    margin: 56px 0 16px;
  }}
  p {{
    margin-bottom: 18px;
  }}
  .lead {{
    margin-bottom: 28px;
  }}
  blockquote {{
    margin: 24px 0;
    padding-left: 16px;
  }}
  .cta {{
    margin-top: 28px;
  }}
  .btn {{
    display: block;
    text-align: center;
    padding: 16px 20px;
  }}
  .final {{
    margin-top: 64px;
    padding-top: 40px;
  }}
}}
</style>
</head>
<body>
<main>
<header class="hero">
{hero}
</header>

{sections}

{final}
</main>
</body>
</html>
"""


# ---------- сверка: текст страницы == текст файла ----------

class TextCollector(HTMLParser):
    """Собирает видимый текст страницы блоками: заголовки, абзацы, кнопки, ссылки."""

    BLOCKS = {"h1", "h2", "p"}

    def __init__(self):
        super().__init__()
        self.blocks = []
        self._cur = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "title"):
            self._skip += 1
        elif tag in self.BLOCKS:
            self._cur = []

    def handle_endtag(self, tag):
        if tag in ("style", "script", "title"):
            self._skip -= 1
        elif tag in self.BLOCKS and self._cur is not None:
            text = " ".join("".join(self._cur).split())
            if text:
                self.blocks.append(text)
            self._cur = None

    def handle_data(self, data):
        if self._skip == 0 and self._cur is not None:
            self._cur.append(data)


def expected_blocks(sections):
    out = []
    for sec in sections:
        if sec["title"] not in ("Первый экран", "Последний экран"):
            out.append(sec["title"])
        for _, text in sec["items"]:
            out.append(text)
    return out


def check(sections, html_text):
    parser = TextCollector()
    parser.feed(html_text)
    got = parser.blocks
    want = expected_blocks(sections)
    if got == want:
        print(f"Сверка: {len(want)} блоков текста совпадают с landing-text.md слово в слово.")
        return True
    print("ОШИБКА: текст страницы разошёлся с landing-text.md", file=sys.stderr)
    for i, (g, w) in enumerate(zip(got, want)):
        if g != w:
            print(f"  блок {i}:\n    страница: {g}\n    файл:     {w}", file=sys.stderr)
            break
    if len(got) != len(want):
        print(f"  блоков на странице: {len(got)}, в файле: {len(want)}", file=sys.stderr)
    return False


def main():
    sections = parse(SRC.read_text(encoding="utf-8"))
    page = render(sections)
    OUT.write_text(page, encoding="utf-8")
    print(f"Собрано: {OUT} ({len(page.encode('utf-8'))} байт)")
    if not check(sections, page):
        sys.exit(1)


if __name__ == "__main__":
    main()
