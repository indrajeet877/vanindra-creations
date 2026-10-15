"""Round 13: interlocking jaali stars -- does a V appear in their overlaps / negative space?"""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER
from explore4 import star83
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')

def two(d, op='xor', kind=(8, 3), rot=90):
    A = P(star_pts(-d, 0, 100, kind[0], kind[1], a0=rot)); B = P(star_pts(d, 0, 100, kind[0], kind[1], a0=rot))
    return {'xor': vt.xor(A, B), 'int': inter(A, B), 'union': union(A, B)}[op]

def three(d, h, op='xor'):
    A = P(star83(-d, -h, 100)); B = P(star83(d, -h, 100)); Cc = P(star83(0, h, 100))
    if op == 'xor':
        return vt.xor(vt.xor(A, B), Cc)
    return union(A, B, Cc)

def band_two(d, t=12):
    out = []
    for cx in (-d, d):
        s = star83(cx, 0, 100)
        out.append(diff(P(s), P(offset(s, t))))
    return vt.xor(out[0], out[1])

VARS = [('xor d=20', lambda: two(20)), ('xor d=38', lambda: two(38)), ('xor d=54', lambda: two(54)),
        ('int d=38', lambda: two(38, 'int')), ('xor khatim d=35', lambda: two(35, kind=(8, 2))), ('three xor', lambda: three(38, 22)),
        ('bands xor d=38', lambda: band_two(38)), ('bands xor d=54', lambda: band_two(54)), ('xor 8/3 rot d=40', lambda: two(40, rot=112.5))]
if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m, _ = fit(fn(), 260, 260, 200, 200)
        f = os.path.join(OUT, f'i{i+1}.svg'); open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name)); files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r12.png')] + files, check=True)
