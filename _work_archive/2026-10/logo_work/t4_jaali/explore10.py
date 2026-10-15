"""Round 10: monumental jaali V -- few large cells, bold rim; and inlay-channel variant."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore8 import P_off_path, contours, area
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5; S, C = math.sin(TH*D2R), math.cos(TH*D2R)
TOP = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])

def jaali_v(H=100.0, t=28.0, w=2.4, rim=4.0, star_r=None, gap=None, rot=22.5, kind=(8, 3), channel=None, minA=4.0, centre=True):
    region = P(v_pts(H, TH, t))
    dv = t / S
    O = (0.0, H - dv / 2)
    band = t if channel is None else channel
    rr = star_r if star_r else (band / 2 - (rim if channel is None else w))
    g = w if gap is None else gap
    seeds = []
    for side in (-1, 1):
        u = (side * S, -C)
        ang = math.degrees(math.atan2(-u[1], u[0]))
        pitch = 2 * rr + g
        for k in range(1, 9):
            c = (O[0] + u[0] * pitch * k, O[1] + u[1] * pitch * k)
            seeds.append(star_pts(c[0], c[1], rr, kind[0], kind[1], a0=ang + rot))
    if centre:
        seeds.append(star_pts(O[0], O[1], rr, kind[0], kind[1], a0=90 + rot))
    if channel is None:
        inner = P_off_path(region, rim)
    else:
        # a channel of width `channel` centred on each arm's centre line
        inner = diff(P_off_path(region, (t - channel) / 2), P([(-300, -300), (300, -300), (300, rim), (-300, rim)]))
    grown = merge([P(offset(s, -w / 2)) for s in seeds])
    left = [c for c in contours(inter(diff(inner, grown), inner)) if area(c) > minA]
    holes = merge([P(offset(s, w / 2)) for s in seeds] + left)
    holes = inter(holes, inner)
    return inter(diff(region, holes), TOP)

VARS = [('mono 2/arm t30', lambda: jaali_v(t=30, w=2.6, rim=4.5)),
        ('mono khatim', lambda: jaali_v(t=30, w=2.6, rim=4.5, kind=(8, 2), rot=0)),
        ('mono bold webs', lambda: jaali_v(t=32, w=3.6, rim=5.5)),
        ('channel inlay', lambda: jaali_v(t=30, w=1.6, rim=4, channel=14)),
        ('channel inlay khatim', lambda: jaali_v(t=30, w=1.6, rim=4, channel=14, kind=(8, 2), rot=0)),
        ('mono 8/3 point-on', lambda: jaali_v(t=30, w=2.6, rim=4.5, rot=0))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 250, 250, 200, 200)
        for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
            f = os.path.join(OUT, f'm{i+1}{tag}.svg'); open(f, 'w').write(svg(400, 400, [(m, fg)], bg=bg, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r9.png')] + files, check=True)
