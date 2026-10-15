import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from mark import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine'); os.makedirs(OUT, exist_ok=True)


def cell(name, lay, bg=IV, minis=True):
    allp = U(*[p for p, _ in lay])
    _, s, tx, ty = fit(allp, (200, 160, 600, 640))
    body = ''.join(pathel(tf(p, s, tx, ty), c) for p, c in lay)
    for size, ox in ((33, 790), (66, 860)):
        _, s2, tx2, ty2 = fit(allp, (ox, 930 - size, size, size))
        body += ''.join(pathel(tf(p, s2, tx2, ty2), c) for p, c in lay)
    return write(os.path.join(OUT, name + '.svg'), 1000, 1000, body, bg=bg)

V_ = [
    ('R1_base_Tw124_tw40_g12', layers(Tw=124, tw=40, g=12)),
    ('R2_heavier_Tw144_tw48_g14_h0p5', layers(Tw=144, tw=48, g=14, hr=0.5)),
    ('R3_lighter_hold_tw30', layers(Tw=130, tw=30, g=11)),
    ('R4_tip_on_baseline_s', layers(Tw=124, tw=40, g=12, s=-(40 + 12 / COS))),
    ('R5_hold_overshoot', layers(Tw=124, tw=40, g=12, foot_drop=40)),
    ('R6_two_tone_on_emerald', layers(col_hook=GL, col_hold=IV, Tw=124, tw=40, g=12)),
]
files = []
for n, lay in V_:
    files.append(cell(n, lay, bg=EM if 'emerald' in n else IV))
print('\n'.join(files))
