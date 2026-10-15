import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import build as B

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wmtest'); os.makedirs(OUT, exist_ok=True)


def stem_width(family, weight, size):
    g = vt.glyph_paths('I', family=family, weight=weight, size=size)[0]
    x0, y0, x1, y1 = g.bounds
    return x1 - x0, -y0


def brand_V(capH, stem, t=9 / 16, apex_up=False, over=0.0):
    """V (or A without bar if apex_up) on the brand angle, uniform perpendicular stroke ~= stem."""
    a = math.atan(t); w = stem / math.cos(a) * 1.0
    H = capH
    O = V(0, over)
    Lo = V(-t * (H + over), -H); Li = V(-t * (H + over) + w, -H)
    Ro = V(t * (H + over), -H); Ri = V(t * (H + over) - w, -H)
    cr = isect(Li, (t, 1), Ri, (-t, 1))
    p = poly([O, Ro, Ri, cr, Li, Lo])
    if apex_up:
        p = vt.transform(p, 1, 0, 0, -1, 0, -H)
    return p


def word_with_brand_letters(weight=500, size=200.0, tracking=0.13, brand_A=True):
    stem, capH = stem_width('jost', weight, size)
    gl = vt.glyph_paths('VANINDRA', family='jost', weight=weight, size=size)
    paths = []
    x = 0.0
    kern = {'VA': -0.03, 'NI': 0.012, 'IN': 0.012, 'ND': 0.006, 'RA': -0.02, 'AN': 0.0, 'DR': 0.0}
    for i, ch in enumerate('VANINDRA'):
        g = gl[i]
        gx0, gy0, gx1, gy1 = g.bounds
        lsb = gx0 - (sum(q.width for q in gl[:i]))
        if ch == 'V' or (ch == 'A' and brand_A):
            if ch == 'V':
                q = brand_V(capH, stem * 1.08, over=capH * 0.012)
            else:
                q = brand_V(capH, stem * 1.08, apex_up=True, over=capH * 0.012)
                # crossbar
                bx = B.MASTER
                yb = -capH * 0.30
                bar = rect(-capH, yb - stem * 0.80, 2 * capH, stem * 0.80)
                q = U(q, I(bar, poly(vt_hull(q))))
            qb = vt.bounds(q)
            side = stem * 0.35
            q = tf(q, 1, x + side - qb[0], 0)
            paths.append(q)
            x += (qb[2] - qb[0]) + 2 * side
        else:
            q = tf(g.path, 1, x - (sum(t_.width for t_ in gl[:i])), 0)
            paths.append(q)
            x += g.width
        if i < 7:
            x += tracking * size + kern.get('VANINDRA'[i:i + 2], 0.0) * size
    return paths, capH


def vt_hull(p):
    x0, y0, x1, y1 = vt.bounds(p)
    # for an A (apex at top centre): triangle hull
    return [((x0 + x1) / 2, y0), (x1, y1), (x0, y1)]


def lock(name, letters, capH, sub_size=0.36):
    top = U(*letters)
    tb = vt.bounds(top)
    size2 = 200 * sub_size
    base = B.set_word('CREATIONS', 'jost', 400, size2, 0.0)
    nat = vt.bounds(U(*base)); n = 8
    trk = ((tb[2] - tb[0]) - (nat[2] - nat[0])) / n / size2
    sub_ = U(*B.set_word('CREATIONS', 'jost', 400, size2, trk))
    sb = vt.bounds(sub_)
    sub_ = tf(sub_, 1, tb[0] - sb[0], capH * 0.5 - sb[1])
    tk, hk = B.mark_paths()
    mb = vt.bounds(U(tk, hk))
    sb = vt.bounds(sub_)
    s = (sb[3] - tb[1]) / (mb[3] - B.MASTER['over'] - mb[1])
    tkk, hkk = tf(tk, s, 0, 0), tf(hk, s, 0, 0)
    mb = vt.bounds(U(tkk, hkk))
    dx = tb[0] - capH * 0.72 - mb[2]; dy = tb[1] - mb[1]
    items = [(tf(tkk, 1, dx, dy), EM), (tf(hkk, 1, dx, dy), GO), (top, EM), (sub_, GO)]
    ab = vt.bounds(U(*[q for q, _ in items])); pad = capH * 0.9
    items = [(tf(q, 1, pad - ab[0], pad - ab[1]), c) for q, c in items]
    return write(os.path.join(OUT, name + '.svg'), ab[2] - ab[0] + 2 * pad, ab[3] - ab[1] + 2 * pad, ''.join(pathel(q, c) for q, c in items), bg=IV)

files = []
L, capH = word_with_brand_letters(brand_A=False)
files.append(lock('w1_brandV_only', L, capH))
L, capH = word_with_brand_letters(brand_A=True)
files.append(lock('w2_brandV_brandA', L, capH))
plain = B.set_word('VANINDRA', 'jost', 500, 200.0, 0.13, B.KERN)
files.append(lock('w3_plain_jost500', plain, -vt.bounds(U(*plain))[1]))
plain4 = B.set_word('VANINDRA', 'jost', 400, 200.0, 0.15, B.KERN)
files.append(lock('w4_plain_jost400', plain4, -vt.bounds(U(*plain4))[1]))
print('\n'.join(files))
