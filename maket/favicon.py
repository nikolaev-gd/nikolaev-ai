"""Значки сайта nikolaev-ai.ru — та же аватарка, что в кнопке «Написать»: фото в зелёном кольце, круг на весь значок.

Исходник — photos/favicon-master.png: снимок этой аватарки со страницы (элемент .av, увеличен в 10 раз,
кольцо 2 px вокруг 48 px — как на сайте), углы за кругом прозрачные, край круга взят на 3 px внутрь,
чтобы не попала тёмная кайма от фона снимка. Поменялась аватарка — переснять.

python3 favicon.py <папка> — пишет туда favicon.ico, favicon-16x16.png, favicon-32x32.png,
favicon-192.png, favicon-512.png, apple-touch-icon.png и site.webmanifest.
"""
import sys, json, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / 'photos/favicon-master.png'


def icon(size):
    return Image.open(SRC).convert('RGBA').resize((size, size), Image.LANCZOS)


def make(out):
    out = pathlib.Path(out)
    for size, name in ((16, 'favicon-16x16.png'), (32, 'favicon-32x32.png'),
                       (192, 'favicon-192.png'), (512, 'favicon-512.png')):
        icon(size).save(out / name)
    icon(256).save(out / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    # Прозрачные углы и тут: этот значок берут карточки ссылок в мессенджерах, тёмный квадрат там виден рамкой
    icon(180).save(out / 'apple-touch-icon.png')
    (out / 'site.webmanifest').write_text(json.dumps({
        'name': 'Геннадий Николаев — наставник по ИИ',
        'short_name': 'Николаев ИИ',
        'icons': [{'src': '/favicon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/favicon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
        'theme_color': '#0C0C0C', 'background_color': '#0C0C0C', 'display': 'browser',
    }, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    make(sys.argv[1])
