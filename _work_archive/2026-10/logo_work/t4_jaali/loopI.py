"""Loop I: every cut in the V points to the jaali's centre -- mitres on the notch radii + axial split on the tip radius."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopI'); os.makedirs(OUT, exist_ok=True)

def split_v(t=9.0, g=1.1):
    u = unit(R=100.0, t=t)
    cut = P([(-g / 2, -10), (g / 2, -10), (g / 2, 120), (-g / 2, 120)])
    return diff(u, cut)

files = []
for name, m in (('plain9', unit(t=9.0)), ('split9_g1.1', split_v(9.0, 1.1)), ('split10_g1.4', split_v(10.0, 1.4)), ('split9_g0.8', split_v(9.0, 0.8))):
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        x0, y0, x1, y1 = vt.bounds(m); s = 600 / (y1 - y0)
        p = vt.transform(m, s, 0, 0, s, 500 - (x0 + x1) / 2 * s, 500 - (y0 + y1) / 2 * s + 12)
        f = os.path.join(OUT, f'{name}_{tag}.svg'); open(f, 'w').write(svg(1000, 1000, [(p, fg)], bg=bg)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopI.png')] + files, check=True)
subprocess.run(['node', RENDER, 'context', os.path.join(OUT, 'ctxI.png'), os.path.join(OUT, 'split9_g1.1_e.svg'), os.path.join(OUT, 'split9_g1.1_e.svg')], check=True)
