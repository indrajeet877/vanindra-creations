import subprocess
from build import *
wm, st = build_word()
wm = norm(wm)
layers = []
y = 0
out = []
for fam, w in [('tiro-devanagari-hindi', 400), ('noto-serif-devanagari', 500), ('martel', 600), ('noto-serif-devanagari', 300)]:
    t = V.text_path('वनिंद्रा', family=fam, weight=w, subset='devanagari', size=100)
    top = -V.text_path('न', family=fam, weight=w, subset='devanagari', size=100).bounds[1]
    s = 100 / top
    dv = tr(t.path, s, 0, 0)
    bx = bbox(dv)
    x_off = bbox(wm)[2] + 46
    dv = tr(dv, 1, x_off - bx[0], 100)   # baseline y=100, headline top y=0
    db = bbox(dv)
    bar = rect(db[0] - 6, 0, db[2] + 5, 8.8)
    row = U(wm, dv, bar)
    out.append(tr(row, 1, 0, y + 60))
    y += 230
body = ''.join(f'<path fill="{EM}" d="{d(r)}"/>' for r in out)
open('study/bil.svg', 'w').write(V.svg_doc(1500, y + 40, body, bg=IV))
subprocess.run(['node', '../toolkit/render.js', 'png', 'study/bil.svg', 'study/bil.png', '1400'], check=True)
