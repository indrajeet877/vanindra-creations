"""Side-by-side evidence: three directions, large + small, on emerald and ivory."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore4 import point_v, rosette, star83
from explore8 import lace, P_off_path, straight_v
from explore6 import jaali_rosette
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')

def lace_mono(H=100.0, t=28.0, w=2.6, rim=4.0, n=3):
    TH=22.5; S, C = math.sin(TH*D2R), math.cos(TH*D2R)
    region = P(v_pts(H, TH, t))
    dv = t / S
    seeds = []
    rr = (t/2 - rim) * 1.0
    O = (0.0, H - dv/2)
    for side in (-1, 1):
        u = (side*S, -C)
        ang = math.degrees(math.atan2(-u[1], u[0]))
        pitch = 2*rr + w
        for k in range(1, 8):
            c = (O[0]+u[0]*pitch*k, O[1]+u[1]*pitch*k)
            seeds.append(star_pts(c[0], c[1], rr, 8, 3, a0=ang+22.5))
    seeds.append(star_pts(O[0], O[1], rr, 8, 3, a0=90+22.5))
    inner = P_off_path(region, rim)
    grown = merge([P(offset(s, -w/2)) for s in seeds])
    holes = merge([P(offset(s, w/2)) for s in seeds] + [diff(inner, grown)])
    holes = inter(holes, inner)
    top = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])
    return inter(diff(region, holes), top)

cands = {'A_lace': lace_mono(), 'B_rosette': rosette(11.0), 'B2_jrosette': jaali_rosette(), 'C_mitred': point_v(8.0)}
files = []
for k, m in cands.items():
    for bg, fg in ((EMERALD, GOLD_LT), (IVORY, EMERALD)):
        mm, _ = fit(m, 260, 260, 200, 200)
        f = os.path.join(OUT, f'cmp_{k}_{"e" if bg==EMERALD else "i"}.svg')
        open(f, 'w').write(svg(400, 400, [(mm, fg)], bg=bg)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'compare.png')] + files, check=True)
for k in cands:
    subprocess.run(['node', RENDER, 'sizes', os.path.join(OUT, f'sizes_{k}.png'), os.path.join(OUT, f'cmp_{k}_e.svg')], check=True)
