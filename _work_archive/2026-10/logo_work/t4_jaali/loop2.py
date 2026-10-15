"""Loop 2: lace V -- which cell family reads as JAALI (not 'stars')? octagon / khatim / 8-3, rim & web weights."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore8 import P_off_path, contours, area
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop2'); os.makedirs(OUT, exist_ok=True)
TH = 22.5; S, C = math.sin(TH*D2R), math.cos(TH*D2R)
TOPCUT = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])

def cell(kind, c, rr, ang):
    if kind == '83':
        return star_pts(c[0], c[1], rr, 8, 3, a0=ang + 22.5)
    if kind == 'khatim':
        return star_pts(c[0], c[1], rr, 8, 2, a0=ang + 22.5)
    if kind == 'oct':
        return ngon_pts(c[0], c[1], rr / math.cos(22.5*D2R), 8, a0=ang + 22.5)
    if kind == 'oct2':   # octagon with a point on the arm axis
        return ngon_pts(c[0], c[1], rr, 8, a0=ang)

def lace_v(kind='83', H=100.0, t=30.0, w=2.2, rim=4.4, gap=None, toprim=None, minA=3.0, scale=1.0):
    region = P(v_pts(H, TH, t))
    O = (0.0, H - t/S/2)
    rr = (t/2 - rim) * scale
    g = w if gap is None else gap
    seeds = []
    for side in (-1, 1):
        u = (side*S, -C); ang = math.degrees(math.atan2(-u[1], u[0]))
        pitch = 2*rr + g
        if kind in ('oct',):
            pitch = 2*rr + g
        for k in range(1, 10):
            c = (O[0]+u[0]*pitch*k, O[1]+u[1]*pitch*k)
            seeds.append(cell(kind, c, rr, ang))
    seeds.append(cell(kind, O, rr, 90.0))
    inner = P_off_path(region, rim)
    if toprim:
        inner = inter(inner, P([(-300, toprim), (300, toprim), (300, 300), (-300, 300)]))
    grown = merge([P(offset(s, -w/2)) for s in seeds])
    left = [c for c in contours(diff(inner, grown)) if area(c) > minA]
    holes = inter(merge([P(offset(s, w/2)) for s in seeds] + left), inner)
    return inter(diff(region, holes), TOPCUT)

VARS = [('8/3 lace', lambda: lace_v('83')), ('khatim lace', lambda: lace_v('khatim')), ('octagon lace', lambda: lace_v('oct', w=2.4)),
        ('octagon pt lace', lambda: lace_v('oct2', w=2.4)), ('8/3 lace heavy', lambda: lace_v('83', t=32, w=3.0, rim=5.4)),
        ('8/3 lace top lintel', lambda: lace_v('83', toprim=7.0)), ('khatim heavy', lambda: lace_v('khatim', t=32, w=3.0, rim=5.4)),
        ('octagon heavy', lambda: lace_v('oct', t=32, w=3.2, rim=5.4)), ('8/3 small cells', lambda: lace_v('83', w=1.8, rim=4.0, scale=0.72, gap=1.6))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 250, 250, 200, 200)
        f = os.path.join(OUT, f'L{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop2.png')] + files, check=True)
