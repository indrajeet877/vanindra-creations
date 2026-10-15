"""Loop F: terminal cut of the V-unit -- radial (jaali joint) vs 22.5 / 45 / horizontal; weights."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import K83
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopF'); os.makedirs(OUT, exist_ok=True)
S, C = math.sin(22.5 * D2R), math.cos(22.5 * D2R)

def vunit(t=8.0, cut='radial', R=100.0):
    s = star_pts(0, 0, R, 8, 3, a0=90)
    band = diff(P(s), P(offset(s, t)))
    # long V band: the bottom point region, generous wedge
    wedge = P([(0, 0), polar(0, 0, 4 * R, 247.5 - 20), polar(0, 0, 4 * R, 292.5 + 20)])
    # keep only the two edges of the bottom point: intersect with the strip regions of its two arms
    tip = (0.0, R)
    arms = []
    for side in (-1, 1):
        notch = polar(0, 0, R * K83, 270 + side * 22.5)
        ux, uy = notch[0] - tip[0], notch[1] - tip[1]; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
        nx, ny = -uy, ux
        if nx * (-notch[0]) < 0: nx, ny = -nx, -ny
        arms.append(P([(tip[0] - ux * 50, tip[1] - uy * 50), (tip[0] + ux * 300, tip[1] + uy * 300),
                       (tip[0] + ux * 300 + nx * t, tip[1] + uy * 300 + ny * t), (tip[0] - ux * 50 + nx * t, tip[1] - uy * 50 + ny * t)]))
    V = inter(union(*arms), P([(-400, -400), (400, -400), (400, R), (-400, R)]))
    V = union(V, inter(band, wedge))
    V = inter(V, P([(-400, -400), (400, -400), (400, R + 0.001), (-400, R + 0.001)]))
    # terminal cut through each outer notch
    keep = []
    for side in (-1, 1):
        notch = polar(0, 0, R * K83, 270 + side * 22.5)
        if cut == 'radial':
            d = (notch[0], notch[1])
        else:
            ang = {'h': 0.0, '22': 22.5, '45': 45.0}[cut]
            d = (math.cos(ang * D2R) * -side, -math.sin(ang * D2R))   # direction rising towards the axis
            d = (-side * math.cos(ang * D2R), -math.sin(ang * D2R))
        # half-plane below the cut line through the notch (on the tip side)
        nx, ny = -d[1], d[0]
        if nx * (0 - notch[0]) + ny * (R - notch[1]) < 0: nx, ny = -nx, -ny
        big = 1000
        p0 = (notch[0] - d[0] * big, notch[1] - d[1] * big); p1 = (notch[0] + d[0] * big, notch[1] + d[1] * big)
        keep.append(P([p0, p1, (p1[0] + nx * big, p1[1] + ny * big), (p0[0] + nx * big, p0[1] + ny * big)]))
    side_half = [P([(-400, -400), (0, -400), (0, 400), (-400, 400)]), P([(0, -400), (400, -400), (400, 400), (0, 400)])]
    parts = [inter(inter(V, side_half[i]), keep[i]) for i in range(2)]
    return union(*parts)

files = []
for cut in ('radial', '45', '22', 'h'):
    for t in (8.0, 9.5):
        u, _ = fit(vunit(t, cut), 250, 250, 200, 200)
        f = os.path.join(OUT, f'{cut}_{t}.svg'); open(f, 'w').write(svg(400, 400, [(u, EMERALD)], bg=IVORY, title=f'{cut} {t}')); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopF.png')] + files, check=True)
