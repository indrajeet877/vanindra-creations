"""Loop H: a V made only of whole jaali units (V made of V's) -- no outline."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from hankin import oct_star, sq_star
from explore8 import contours, area
from jv import v_outline
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopH'); os.makedirs(OUT, exist_ok=True)

def units_of(pts, cx, cy, t, slit, n):
    band = diff(P(pts), P(offset(pts, t)))
    cuts = []
    for k in range(n):
        q = pts[2 * k + 1]
        a = math.degrees(math.atan2(-(q[1] - cy), q[0] - cx))
        cuts.append(vt.stroke_to_path(P([(cx, cy), polar(cx, cy, 1e3, a), polar(cx, cy, 1e3, a + 1e-4)]), slit))
    return contours(diff(band, merge(cuts)))

def all_units(a, t, slit, xr, yr, ox, oy):
    us = []
    for i in range(-xr, xr + 1):
        for j in range(-yr, yr + 1):
            cx, cy = ox + i * a, oy + j * a
            us += units_of(oct_star(cx, cy, a), cx, cy, t, slit, 8)
            sx, sy = cx + a / 2, cy + a / 2
            us += units_of(sq_star(sx, sy, a), sx, sy, t * 0.85, slit, 4)
    return us

def centroid(p):
    b = vt.bounds(p); return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

def vcluster(a=40.0, t=3.2, slit=1.0, H=124.0, tv=34.0, oy=0.0, ox=0.0, mode='centroid'):
    V = P(v_outline(H, tv))
    us = all_units(a, t, slit, 6, 6, ox, oy)
    keep = []
    for u in us:
        if mode == 'centroid':
            c = centroid(u)
            if V.contains(c):
                keep.append(u)
        else:
            if area(diff(u, V)) < 1e-6:
                keep.append(u)
    return merge(keep)

V = [('a40 centroid', dict()), ('a40 whole', dict(mode='whole')), ('a32 centroid', dict(a=32.0, t=2.8)), ('a48 centroid', dict(a=48.0, t=3.8, tv=38)),
     ('a40 shift', dict(oy=20.0)), ('a40 shiftx', dict(ox=20.0, oy=20.0))]
files = []
for i, (name, kw) in enumerate(V):
    m = vcluster(**kw)
    mm, _ = fit(m, 260, 260, 200, 200)
    f = os.path.join(OUT, f'{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(mm, GOLD_LT)], bg=EMERALD, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopH.png')] + files, check=True)
