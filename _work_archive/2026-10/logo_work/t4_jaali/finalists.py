import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER
from explore4 import point_v, rosette, star83
from explore6 import jaali_rosette
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
c = {'f1_rosette': rosette(12.0, slit=4.0), 'f2_seed': point_v(10.0), 'f3_jros': jaali_rosette(t=10, g=3.0)}
for k, m in c.items():
    mm, _ = fit(m, 250, 250, 200, 200)
    f = os.path.join(OUT, k + '.svg'); open(f, 'w').write(svg(400, 400, [(mm, GOLD_LT)], bg=EMERALD))
    subprocess.run(['node', RENDER, 'context', os.path.join(OUT, k + '_ctx.png'), f, f], check=True)
