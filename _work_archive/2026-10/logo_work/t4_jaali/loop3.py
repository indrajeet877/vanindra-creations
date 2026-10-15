import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from jv import build
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop3'); os.makedirs(OUT, exist_ok=True)
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
V = [('a t24 H124', dict()), ('b t26 H124 rim4.2', dict(t=26, rim=4.2, web=2.2)), ('c t22 H118', dict(t=22, H=118, rim=3.4, web=1.8)),
     ('d lintel 6', dict(lintel=6.0)), ('e khatim', dict(star_m=2)), ('f t28 H132', dict(t=28, H=132, rim=4.6, web=2.3))]
files = []
for i, (name, kw) in enumerate(V):
    m = build(**kw)
    mm, _ = fit(m, 250, 250, 200, 200)
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        f = os.path.join(OUT, f'{chr(97+i)}_{tag}.svg'); open(f, 'w').write(svg(400, 400, [(mm, fg)], bg=bg, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop3.png')] + files, check=True)
subprocess.run(['node', RENDER, 'sizes', os.path.join(OUT, 'sizes_a.png'), os.path.join(OUT, 'a_e.svg')], check=True)
