"""Round-4: slice interlace vs hidden-I window vs beam, refined."""
import math
import os
import subprocess
from mono import *  # noqa
from explore import didone_V, didone_I, stroke_quad, H


def slice_(L=440, R=470, thick=185, thin=30, d=245, stem=150, top=1140, gap=22, sw=80):
    """Tall I overlapping the V's right half; the hairline arm passes OVER the stem (thin over thick)."""
    V, g = didone_V(L=L, R=R, thick=thick, thin=thin)
    I = didone_I(d, 0, top, stem=stem, sw=sw)
    # hairline arm region (right of the junction)
    P, B, B2, J = g['P'], g['B'], g['B2'], g['J']
    hair = poly([(J[0] - 400, J[1] - 400 * (B[1] - P[1]) / (B[0] - P[0]) * 0), P, B, B2, J])
    hair = intersection(V, poly([P, B, (B2[0], B2[1]), J]))
    I = over(hair, I, gap, region=rect(d - stem, 100, d + stem, top - 60))
    return union(V, I)


def window(L=460, R=430, thick=232, thin=30, yc=540, hh=330, w=None, sw=None, sh=None):
    V, g = didone_V(L=L, R=R, thick=thick, thin=thin)
    w = thin if w is None else w
    sw = 52 if sw is None else sw
    sh = 18 if sh is None else sh
    xl = x_at(g['A'], g['P'], yc)
    xr = x_at(g['A2'], g['J'], yc)
    xc = (xl + xr) / 2
    slot = union(rect(xc - w / 2, yc - hh / 2, xc + w / 2, yc + hh / 2),
                 rect(xc - sw, yc + hh / 2 - sh, xc + sw, yc + hh / 2),
                 rect(xc - sw, yc - hh / 2, xc + sw, yc - hh / 2 + sh))
    return difference(V, slot)


def r4a():
    return slice_()


def r4b():
    return slice_(L=430, R=430, d=200, stem=140, top=1000, sw=70)


def r4c():
    return window()


def r4d():
    return window(thick=250, hh=380, yc=560, sw=44, sh=16, w=24)


def r4e():
    """Window as a true serifed I with brackets."""
    V, g = didone_V(L=460, R=430, thick=240, thin=30)
    yc, hh = 545, 360
    xl = x_at(g['A'], g['P'], yc)
    xr = x_at(g['A2'], g['J'], yc)
    xc = (xl + xr) / 2 + 4
    I = didone_I(xc, yc - hh / 2, yc + hh / 2, stem=30, sw=30, sh=16, br=12)
    return difference(V, I)


def r4f():
    """Beam: hairline I runs through the thick arm, white inside, dark outside; I stops at V's cap + baseline."""
    V, g = didone_V(L=460, R=430, thick=232, thin=30)
    x = -210
    w = 30
    I = didone_I(x, 0, H, stem=w, sw=34, sh=18, br=10)
    I_out = difference(I, dilate(V, 26))
    V2 = difference(V, rect(x - w / 2, -900, x + w / 2, 2900))
    return union(V2, I_out)


def r4g():
    """Window + its echo: the I-window also opens the V's hairline arm's terminal (two I's?)"""
    return window(L=430, R=430, thick=220, yc=600, hh=300)


def r4h():
    """Slice, I to the far right, V's hairline exits through the I's top-left."""
    return slice_(L=440, R=430, d=300, stem=150, top=1000, sw=78)


def r4i():
    """Window version with V slightly condensed (Vogue proportion)."""
    return window(L=380, R=360, thick=210, thin=28, yc=560, hh=330, sw=46)


EXPL = [('a slice tall I', r4a), ('b slice cap-height', r4b), ('c window', r4c), ('d window tall', r4d),
        ('e window serifed', r4e), ('f beam cap/base', r4f), ('g window high', r4g), ('h slice far right', r4h),
        ('i window condensed', r4i)]

if __name__ == '__main__':
    files = []
    OUT = os.path.join(HERE, 'explore')
    for i, (name, fn) in enumerate(EXPL):
        p = to_svg_space(fn())
        S = 600
        big, _ = place(p, 110, 70, 380, 400)
        small = []
        for k, sz in enumerate((48, 24, 16)):
            sp, _ = place(p, 150 + k * 90, 505, sz, sz)
            small.append(path_el(sp, EMERALD))
        lab = vtype.text_path(name, family='jost', weight=400, size=22, x=24, y=578)
        body = path_el(big, EMERALD) + ''.join(small) + path_el(lab.path, '#777')
        fn_ = os.path.join(OUT, f'r4_{i + 1}.svg')
        write_svg(fn_, S, S, body, bg=IVORY)
        files.append(fn_)
    subprocess.run(['node', os.path.join(HERE, '..', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore_r4.png')] + files, check=True)
    print('ok')
