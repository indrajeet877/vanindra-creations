import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from hookmark import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop1'); os.makedirs(OUT, exist_ok=True)


def cell(name, lay, bg):
    allp = U(*[q for q, _ in lay])
    _, s, tx, ty = fit(allp, (200, 150, 600, 620))
    body = ''.join(pathel(tf(q, s, tx, ty), c) for q, c in lay)
    for size, ox in ((33, 760), (66, 850)):
        _, s2, tx2, ty2 = fit(allp, (ox, 935 - size, size, size))
        body += ''.join(pathel(tf(q, s2, tx2, ty2), c) for q, c in lay)
    return write(os.path.join(OUT, name + '.svg'), 1000, 1000, body, bg=bg)

V_ = [
    ('a_point_p135', layers(p=135), IV),
    ('b_flatfoot_p135', layers(p=135, foot=70), IV),
    ('c_point_p110_light', layers(p=110, g=22), IV),
    ('d_narrow_t045_p125', layers(t=0.45, p=125), IV),
    ('e_point_p160_heavy', layers(p=160, g=30), IV),
    ('f_on_emerald_p135', layers(on='emerald', p=135), EM),
]
print('\n'.join(cell(n, l, b) for n, l, b in V_))
