"""Loop G: hero = the jaali star with OUR V as one of its eight points (colour + weight so it holds in one colour)."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopG'); os.makedirs(OUT, exist_ok=True)

def parts(tv, to, slit):
    v = unit(t=tv, k=0, slit=slit)
    o = merge([unit(t=to, k=k, slit=slit) for k in range(1, 8)])
    return v, o

def tf_all(v, o, size=400, fill=0.74):
    b = vt.bounds(merge([v, o])); s = fill * size / (b[3] - b[1])
    f = lambda p: vt.transform(p, s, 0, 0, s, size / 2 - (b[0] + b[2]) / 2 * s, size / 2 - (b[1] + b[3]) / 2 * s)
    return f(v), f(o)

files = []
for tv, to, sl in ((10, 10, 2.6), (11, 6, 2.6), (12, 5, 3.0), (11, 4, 3.0)):
    v, o = tf_all(*parts(tv, to, sl))
    for bg, cv, co, tag in ((IVORY, EMERALD, GOLD, 'two_i'), (EMERALD, IVORY, GOLD_LT, 'two_e'), (IVORY, EMERALD, EMERALD, 'one')):
        f = os.path.join(OUT, f'g_{tv}_{to}_{tag}.svg'); open(f, 'w').write(svg(400, 400, [(o, co), (v, cv)], bg=bg)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopG.png')] + files, check=True)
subprocess.run(['node', RENDER, 'context', os.path.join(OUT, 'ctxG.png'), os.path.join(OUT, 'g_11_6_two_e.svg'), os.path.join(OUT, 'g_11_6_two_e.svg')], check=True)
