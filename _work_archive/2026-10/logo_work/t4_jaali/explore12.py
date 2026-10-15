"""Round 12: V cut from a true Hankin jaali (every star drawn from V's)."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore8 import P_off_path
from hankin import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5; S, C = math.sin(TH*D2R), math.cos(TH*D2R)
TOP = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])

def pattern_patch(a=20.0, w=1.6):
    webs = hankin_webs(a, w, 4, 4)
    sq = P([(-80, -80), (80, -80), (80, 80), (-80, 80)])
    return inter(webs, sq)

def v_cut(H=100.0, t=30.0, a=20.0, w=1.8, rim=3.0, tip_on=True, oy=None):
    region = P(v_pts(H, TH, t))
    # align: an octagon's bottom star point (an X node) sits on the V axis
    if oy is None:
        oy = H - t / S / 2 - a / 2
    webs = hankin_webs(a, w, 6, 8, 0.0, oy)
    inner = P_off_path(region, rim)
    holes = diff(inner, webs)
    return inter(diff(region, holes), TOP)

VARS = [('hankin pattern', pattern_patch), ('V cut a20', lambda: v_cut()), ('V cut a26', lambda: v_cut(a=26.0, w=2.0)),
        ('V cut a16 thin', lambda: v_cut(a=16.0, w=1.4, rim=2.6)), ('V cut a24 thick', lambda: v_cut(t=34, a=24.0, w=2.4, rim=4.0)),
        ('V cut shift', lambda: v_cut(a=22.0, w=2.0, oy=40))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 260, 260, 200, 200)
        f = os.path.join(OUT, f'h{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r11.png')] + files, check=True)
