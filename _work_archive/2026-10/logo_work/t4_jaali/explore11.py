"""Round 11: a star of light breaking through the V at its vertex (knot)."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5; S, C, TN = math.sin(TH*D2R), math.cos(TH*D2R), math.tan(TH*D2R)
TOP = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])

def knot(H=100.0, t=20.0, R=None, dy=0.0, kind=(8, 3), rot=90, minA=6.0):
    V = P(v_pts(H, TH, t))
    dv = t / S
    O = (0.0, H - dv / 2 + dy)
    R = R or t * 0.9
    st = P(star_pts(O[0], O[1], R, kind[0], kind[1], a0=rot))
    m = inter(diff(V, st), TOP)
    from explore8 import contours, area
    parts = [c for c in contours(m) if area(c) > minA]
    return merge(parts)

VARS = [('knot R=t*0.9', lambda: knot()), ('knot R=t*1.1', lambda: knot(R=22)), ('knot R=t*1.3', lambda: knot(R=26)),
        ('knot lower', lambda: knot(R=24, dy=4)), ('knot thick V', lambda: knot(t=26, R=30)), ('knot khatim', lambda: knot(R=24, kind=(8, 2), rot=90)),
        ('knot thin V big star', lambda: knot(t=15, R=24)), ('knot 8/3 rot', lambda: knot(R=24, rot=112.5)), ('knot higher', lambda: knot(R=24, dy=-6))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 250, 250, 200, 200)
        f = os.path.join(OUT, f'k{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r10.png')] + files, check=True)
