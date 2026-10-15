import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from jv2 import build
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop5'); os.makedirs(OUT, exist_ok=True)
V = [('1row t26', dict()), ('1row t28 web2.4', dict(t=28, web=2.4, rim=4.4)), ('2rows t30', dict(t=30, rows=2, web=1.6, rim=3.6)),
     ('1row khatim', dict(star_m=2)), ('1row big vertex', dict(vertex_scale=1.25)), ('2rows t34', dict(t=34, H=132, rows=2, web=1.8, rim=4.0))]
files = []
for i, (name, kw) in enumerate(V):
    m = build(**kw)
    mm, _ = fit(m, 250, 250, 200, 200)
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        f = os.path.join(OUT, f'{i+1}{tag}.svg'); open(f, 'w').write(svg(400, 400, [(mm, fg)], bg=bg, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop5.png')] + files, check=True)
