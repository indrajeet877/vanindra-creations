"""Loop 4: unit-V proportions + lockup with wordmark candidates."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit, rosette
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop4')
files = []
for t in (8.0, 10.0, 12.0, 14.0):
    m, _ = fit(unit(t=t), 230, 230, 200, 200)
    f = os.path.join(OUT, f'u_t{int(t)}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY)); files.append(f)
for fam, wt in (('marcellus', 400), ('cormorant-garamond', 600)):
    for t in (10.0, 12.0):
        mk = unit(t=t)
        mk, s = scale_to_height(mk, 120, 40, 40)
        w1 = vt.text_path('VANINDRA', family=fam, weight=wt, size=74, x=0, y=0, tracking=0.14)
        x0, y0, x1, y1 = vt.bounds(w1.path)
        capH = y1 - y0
        sc = 62 / capH
        mb = vt.bounds(mk)
        wx = mb[2] + 40
        wm = vt.transform(w1.path, sc, 0, 0, sc, wx - x0 * sc, 40 + 6 - y0 * sc)
        w2 = vt.text_path('CREATIONS', family=fam, weight=wt, size=24, x=0, y=0, tracking=0.62)
        b2 = vt.bounds(w2.path); wb = vt.bounds(wm)
        sc2 = 18 / (b2[3] - b2[1])
        cr = vt.transform(w2.path, sc2, 0, 0, sc2, wx - b2[0] * sc2 + 3, wb[3] + 22 - b2[1] * sc2)
        W = vt.bounds(cr)[2] if vt.bounds(cr)[2] > wb[2] else wb[2]
        f = os.path.join(OUT, f'lock_{fam[:4]}_{int(t)}.svg')
        open(f, 'w').write(svg(W + 40, 200, [(mk, EMERALD), (wm, EMERALD), (cr, GOLD)], bg=IVORY)); files.append(f)
mr, _ = fit(rosette(t=10, slit=3), 260, 260, 200, 200)
f = os.path.join(OUT, 'rosette.svg'); open(f, 'w').write(svg(400, 400, [(mr, GOLD_LT)], bg=EMERALD)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop4.png')] + files, check=True)
