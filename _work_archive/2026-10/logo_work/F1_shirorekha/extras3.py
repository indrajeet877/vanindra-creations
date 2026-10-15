"""context_global.png and sizes_global.png (F1): the global avatar is used as a profile picture (circle crop) at
32-110 px; favicons on every domain use the pixel-fitted va (mark_small.svg / favicon.ico)."""
import subprocess, base64
from r5system import *
from header3 import font_uri

B64 = lambda s: base64.b64encode(s.encode()).decode()
SV = lambda n: 'data:image/svg+xml;base64,' + B64(open(os.path.join(HERE, n)).read())


def shot(html, out, w):
    hp = os.path.join(HERE, '_work', '_x3.html')
    open(hp, 'w').write(f'''<!doctype html><html><head><style>
@font-face {{ font-family: Manrope; font-weight: 500; src: url({font_uri(500)}) format('woff2'); }}
body {{ margin:0; background:#8f8f8f; font-family: Manrope, sans-serif; }} .c {{ border-radius:50%; overflow:hidden; display:block }}
</style></head><body><div id="root" style="display:inline-block">{html}</div></body></html>''')
    subprocess.run(['node', os.path.join(HERE, '_r5', 'eshot.js'), hp, out, str(w)], check=True)


def context_global():
    av, fav, hdr = SV('mark_global_on_emerald.svg'), SV('mark_small.svg'), SV('global_header.svg')
    html = f'''<div style="padding:20px;display:grid;gap:20px;width:960px;font:14px Manrope">
      <div style="display:flex;gap:20px;align-items:center;background:#fff;padding:16px;border-radius:8px">
        <div style="width:150px;height:150px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #fff,0 0 0 5px #d62976"><img src="{av}" style="width:100%;height:100%"></div>
        <img class="c" src="{av}" width="56" height="56"><img class="c" src="{av}" width="40" height="40"><img class="c" src="{av}" width="32" height="32">
        <div style="display:flex;align-items:center;gap:8px;background:#f1f3f4;padding:8px 12px;border-radius:8px 8px 0 0"><img src="{fav}" width="16" height="16"><span>VanIndra Creations</span></div>
      </div>
      <div style="background:{IV};padding:16px 24px;display:flex;align-items:center;justify-content:space-between"><img src="{hdr}" style="height:46px"><span style="color:{EM};opacity:.7">Work · Services · Pricing</span></div>
      <div style="background:{EM};padding:16px 24px"><img src="{SV('global_on_emerald.svg')}" style="height:64px"></div>
    </div>'''
    shot(html, os.path.join(HERE, 'context_global.png'), 1000)


def sizes_global():
    av, avi = SV('mark_global_on_emerald.svg'), SV('mark_global_on_ivory.svg')
    row = lambda src, bg: (f'<div style="display:flex;gap:24px;align-items:flex-end;padding:20px;background:{bg}">' +
                           ''.join(f'<img class="c" src="{src}" width="{s}" height="{s}">' for s in (32, 40, 48, 56, 80, 110)) + '</div>')
    shot(row(av, '#FFFFFF') + row(avi, EM), os.path.join(HERE, 'sizes_global.png'), 520)


if __name__ == '__main__':
    context_global()
    sizes_global()
