import os, subprocess, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit, rosette, K83
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop4')

def ros_bold(t_main=13, t_other=7, slit=3.0):
    parts = [unit(t=t_main, k=0, slit=slit)] + [unit(t=t_other, k=k, slit=slit) for k in range(1, 8)]
    return merge(parts)

def ros_wide(t=11, slit=6.0):
    return rosette(t=t, slit=slit)

def ros_double(t=8, g=3, slit=3):
    a = rosette(t=t, slit=slit)
    s = star_pts(0, 0, 100, 8, 3, a0=90)
    inner = diff(P(offset(s, t + g)), P(offset(s, 2 * t + g)))
    cuts = merge([vt.stroke_to_path(P([(0, 0), polar(0, 0, 400, 247.5 + 45 * k), polar(0, 0, 400, 247.5 + 45 * k + .001)]), slit) for k in range(8)])
    return merge([a, diff(inner, cuts)])

def ros_gold_v():
    return None

V = [('eq t10 s3', lambda: rosette(t=10, slit=3)), ('eq t12 s5', lambda: rosette(t=12, slit=5)), ('wide t11 s8', lambda: ros_wide(11, 8)),
     ('bold V', lambda: ros_bold()), ('bold V 2', lambda: ros_bold(14, 5, 4)), ('double', lambda: ros_double())]
files = []
for i, (name, fn) in enumerate(V):
    m, _ = fit(fn(), 270, 270, 200, 200)
    f = os.path.join(OUT, f'r{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, GOLD_LT)], bg=EMERALD, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop4b.png')] + files, check=True)
subprocess.run(['node', RENDER, 'context', os.path.join(OUT, 'ctx_r2.png'), files[1], files[1]], check=True)
