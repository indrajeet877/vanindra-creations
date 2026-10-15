import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from jv3 import build
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop7'); os.makedirs(OUT, exist_ok=True)
V = [('n3 square', dict()), ('n3 pointed', dict(ends='pointed')), ('n2 pointed big', dict(n=2, t=28, rail=4.2, ends='pointed')),
     ('n4 square', dict(n=4, t=24, rail=3.6)), ('khatim n3 pointed', dict(kind=2, ends='pointed')), ('n3 pointed tight', dict(ends='pointed', web=1.4, rail=3.4))]
files = []
for i, (name, kw) in enumerate(V):
    m = build(**kw)
    mm, _ = fit(m, 250, 250, 200, 200)
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        f = os.path.join(OUT, f'{i+1}{tag}.svg'); open(f, 'w').write(svg(400, 400, [(mm, fg)], bg=bg, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop7.png')] + files, check=True)
