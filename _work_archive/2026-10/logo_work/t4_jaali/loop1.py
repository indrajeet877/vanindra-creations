"""Loop 1: silhouette {straight, mitred} x carving {channel, perforation grid, lace, big-star frieze}."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore8 import P_off_path, contours, area
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop1'); os.makedirs(OUT, exist_ok=True)
TH = 22.5; S, C, TN = math.sin(TH*D2R), math.cos(TH*D2R), math.tan(TH*D2R)
K83 = math.cos(math.pi*3/8)/math.cos(math.pi*2/8)

def sil_straight(H=100.0, t=30.0):
    return P(v_pts(H, TH, t)), (0.0, H - t/S/2)

def sil_mitred(R=100.0, t=None):
    # bottom point of an {8/3} star band, scaled so the V is ~100 tall
    t = t or 0.16 * R
    s = star_pts(0, 0, R, 8, 3, a0=90)
    band = diff(P(s), P(offset(s, t)))
    wedge = P([(0, 0), polar(0, 0, 900, 247.5), polar(0, 0, 900, 292.5)])
    return inter(band, wedge), (0.0, R - t/S/2), t

def arm_dirs():
    out = []
    for side in (-1, 1):
        u = (side*S, -C); out.append((u, math.degrees(math.atan2(-u[1], u[0]))))
    return out

def star_chain(O, rr, gap, n=10, rot=22.5, centre=True):
    seeds = []
    for u, ang in arm_dirs():
        pitch = 2*rr + gap
        for k in range(1, n):
            c = (O[0]+u[0]*pitch*k, O[1]+u[1]*pitch*k)
            seeds.append(star_pts(c[0], c[1], rr, 8, 3, a0=ang+rot))
    if centre:
        seeds.append(star_pts(O[0], O[1], rr, 8, 3, a0=90+rot))
    return seeds

def whole_inside(seeds, inner):
    keep = []
    for s in seeds:
        p = P(s)
        if area(diff(p, inner)) < 1e-6:
            keep.append(p)
    return merge(keep) if keep else pathops.Path()

def carve_channel(region, O, t, ch=0.42, w=1.4, top=None):
    rr = t*ch/2
    seeds = star_chain(O, rr, w)
    inner = P_off_path(region, (t - t*ch)/2 - 0.01)
    holes = whole_inside(seeds, P_off_path(region, (t - 2*rr)/2 - 0.2))
    return diff(region, holes)

def carve_perf(region, O, t, pitch=7.0, r=2.6, rim=3.5):
    inner = P_off_path(region, rim)
    seeds = []
    for i in range(-20, 21):
        for j in range(-2, 30):
            seeds.append(star_pts(i*pitch + (j % 2)*pitch/2, O[1] - j*pitch*0.5*1.0, r, 8, 3, a0=90))
    return diff(region, whole_inside(seeds, inner))

def carve_lace(region, O, t, w=2.2, rim=4.4):
    rr = t/2 - rim
    seeds = star_chain(O, rr, w)
    inner = P_off_path(region, rim)
    grown = merge([P(offset(s, -w/2)) for s in seeds])
    left = [c for c in contours(diff(inner, grown)) if area(c) > 3.0]
    holes = inter(merge([P(offset(s, w/2)) for s in seeds] + left), inner)
    return diff(region, holes)

def carve_bigstars(region, O, t, rim=4.6, gap=3.0):
    rr = t/2 - rim
    seeds = star_chain(O, rr, gap)
    inner = P_off_path(region, rim*0.6)
    return diff(region, whole_inside([s for s in seeds], inner))

TOPCUT = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])
rows = []
reg_s, O_s = sil_straight()
reg_m, O_m, t_m = sil_mitred()
cands = [('S_channel', carve_channel(reg_s, O_s, 30.0)), ('S_perf', carve_perf(reg_s, O_s, 30.0)),
         ('S_lace', carve_lace(reg_s, O_s, 30.0)), ('S_bigstars', carve_bigstars(reg_s, O_s, 30.0)),
         ('M_channel', carve_channel(reg_m, O_m, t_m)), ('M_perf', carve_perf(reg_m, O_m, t_m, pitch=5.6, r=2.0, rim=2.8)),
         ('M_lace', carve_lace(reg_m, O_m, t_m, w=1.6, rim=3.2)), ('M_bigstars', carve_bigstars(reg_m, O_m, t_m, rim=3.4, gap=2.2))]
files = []
for name, m in cands:
    m = inter(m, TOPCUT) if name.startswith('S') else m
    mm, _ = fit(m, 250, 250, 200, 200)
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        f = os.path.join(OUT, f'{name}_{tag}.svg'); open(f, 'w').write(svg(400, 400, [(mm, fg)], bg=bg, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop1.png')] + files, check=True)
print('ok')
