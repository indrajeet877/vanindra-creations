"""Loop E: which star gives the most elegant V-unit? {8/3} (45deg), {10/4} (36deg), {12/5} (30deg)."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loopE'); os.makedirs(OUT, exist_ok=True)

def nunit(n, m, R=100.0, t=10.0, k=0, slit=0.0):
    s = star_pts(0, 0, R, n, m, a0=90)
    band = diff(P(s), P(offset(s, t)))
    half = 180.0 / n
    a = 270 + 360.0 / n * k
    wedge = P([(0, 0), polar(0, 0, 4 * R, a - half), polar(0, 0, 4 * R, a + half)])
    u = inter(band, wedge)
    if slit:
        cuts = merge([vt.stroke_to_path(P([(0, 0), polar(0, 0, 4 * R, a + sg * half), polar(0, 0, 4 * R, a + sg * half + 1e-3)]), slit) for sg in (-1, 1)])
        u = diff(u, cuts)
    return u

def nros(n, m, t, slit):
    return merge([nunit(n, m, t=t, k=k, slit=slit) for k in range(n)])

files = []
for n, m, ts in ((8, 3, (7.5, 9.0)), (10, 4, (6.0, 7.5)), (12, 5, (5.0, 6.5))):
    for t in ts:
        u, _ = fit(nunit(n, m, t=t), 250, 250, 200, 200)
        f = os.path.join(OUT, f'u{n}_{t}.svg'); open(f, 'w').write(svg(400, 400, [(u, EMERALD)], bg=IVORY)); files.append(f)
    r = merge([nunit(n, m, t=ts[0], k=k, slit=2.0) for k in range(1, n)])
    v = nunit(n, m, t=ts[0], k=0, slit=2.0)
    allp = merge([r, v]); b = vt.bounds(allp); s = 270 / (b[3] - b[1])
    tf = lambda p: vt.transform(p, s, 0, 0, s, 200 - (b[0] + b[2]) / 2 * s, 200 - (b[1] + b[3]) / 2 * s)
    f = os.path.join(OUT, f'r{n}.svg'); open(f, 'w').write(svg(400, 400, [(tf(r), GOLD_LT), (tf(v), IVORY)], bg=EMERALD)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopE.png')] + files, check=True)
