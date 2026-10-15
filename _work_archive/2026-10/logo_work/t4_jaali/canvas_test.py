import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from canvas import canvas
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopD'); os.makedirs(OUT, exist_ok=True)
files = []
for name, kw in (('c1', dict()), ('c2', dict(t=7.0, slit=2.2)), ('c3', dict(square=False, t=6.0, slit=2.0))):
    c = canvas(**kw)
    box = P([(-250, -250), (250, -250), (250, 250), (-250, 250)])
    c = inter(c, box)
    c = vt.transform(c, 0.8, 0, 0, 0.8, 200, 200)
    f = os.path.join(OUT, name + '.svg'); open(f, 'w').write(svg(400, 400, [(c, GOLD_LT)], bg=EMERALD)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'canvas.png')] + files, check=True)
