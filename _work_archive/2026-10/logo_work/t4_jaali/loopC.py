import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from lace import build
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopC'); os.makedirs(OUT, exist_ok=True)
V = [('83 rot22 k1.5', dict()), ('83 rot0 k1.5', dict(rot=0.0)), ('khatim rot22 k1.5', dict(m=2)),
     ('83 rot22 k1.4 tight', dict(k0=1.35, web=1.6)), ('83 rot0 no vstar k1', dict(rot=0.0, k0=1.0, vstar=False)), ('khatim rot0', dict(m=2, rot=0.0))]
files = []
for i, (name, kw) in enumerate(V):
    m = build(**kw)
    mm, _ = fit(m, 330, 330, 200, 200)
    f = os.path.join(OUT, f'{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(mm, EMERALD)], bg=IVORY, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopC.png')] + files, check=True)
