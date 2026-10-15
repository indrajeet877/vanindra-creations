"""Round 9: one jaali star of light caught in the V (closure), at several scales."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore4 import star83
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5; S, C, TN = math.sin(TH*D2R), math.cos(TH*D2R), math.tan(TH*D2R)
TOP = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])

def caught(H=100.0, t=22.0, R=30.0, cy=None, kind=(8, 3), rot=90):
    V = P(v_pts(H, TH, t))
    dv = t / S
    ya = H - dv
    if cy is None:
        cy = ya - R * 1.0
    st = P(star_pts(0, cy, R, kind[0], kind[1], a0=rot))
    return inter(diff(V, st), TOP)

VARS = [('caught R30', lambda: caught()), ('caught R36 lower', lambda: caught(R=36, cy=40)),
        ('caught R44 severs', lambda: caught(R=44, cy=38)), ('caught khatim', lambda: caught(R=34, cy=36, kind=(8, 2))),
        ('caught 8/3 rot', lambda: caught(R=36, cy=40, rot=112.5)), ('caught thin V', lambda: caught(t=16, R=34, cy=40))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 250, 250, 200, 200)
        f = os.path.join(OUT, f'c{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r8.png')] + files, check=True)
