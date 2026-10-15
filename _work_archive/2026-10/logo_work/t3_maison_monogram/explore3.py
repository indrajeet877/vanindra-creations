"""Round-3 exploration: constructions obeying the derived rules
(no centred I, nothing crossing the I stem horizontally, interlace only at steep angles)."""
import math
import os
import subprocess
from mono import *  # noqa
from explore import didone_V, didone_I, stroke_quad, H


def r3a(join=True, drop=300, d_off=40, gap=24):
    """Dropped V + tall I: V's hairline top terminal joins the I stem; I's foot serif weaves across the hairline arm."""
    L, R = 440, 420
    V, g = didone_V(L=L, R=R, thick=185, thin=32, serifs=True)
    if join:
        # remove right serif, extend hairline arm into stem
        V, g = didone_V(L=L, R=R, thick=185, thin=32, serifs=True)
    V = move(V, 0, -drop)
    stem = 150
    d = R + stem / 2 + (0 if join else d_off) - 10
    I = didone_I(d, 0, H, stem=stem, sw=80, foot_l=40)
    # foot serif over hairline arm
    foot = rect(40, 0, d, 22)
    V = over(foot, V, gap, region=rect(0, -60, 400, 80))
    V = difference(V, rect(d - stem / 2, -5000, 5000, 5000))
    return union(V, I)


def r3b():
    return r3a(join=False, drop=260, d_off=70)


def r3c():
    """VI ligature, shared cap hairline, foot serif woven under the V point (refined proportions)."""
    L, R = 430, 400
    thick, thin = 178, 30
    V, g = didone_V(L=L, R=R, thick=thick, thin=thin, serifs=False, os_=0)
    drop = 70
    V = move(V, 0, -drop)
    top = H - drop
    sh = 20
    stem = 150
    d = R + stem / 2 + 60
    I = didone_I(d, 0, top, stem=stem, sw=78, head=False, foot_l=-120)
    cap_r = rect(R - thin - 34, top - sh, d + stem / 2 + 78, top)
    cap_l = rect(-L - 54, top - sh, -L + thick + 34, top)
    br = []
    for (p1, p2, side) in [(g['A'], g['P'], -1), (g['A2'], g['J'], +1), (g['B2'], g['J'], -1), (g['B'], g['P'], +1)]:
        p1m, p2m = (p1[0], p1[1] - drop), (p2[0], p2[1] - drop)
        y = top - sh
        c = (x_at(p1m, p2m, y), y)
        br.append(bracket(c, (side, 0), unit((p2m[0] - p1m[0], p2m[1] - p1m[1])), 24, 40))
    for sx in (-1, 1):
        br.append(bracket((d + sx * stem / 2, top - sh), (sx, 0), (0, -1), 24, 40))
    Vb = intersection(V, rect(-2000, -2000, 2000, 60))
    I = over(Vb, I, 24, region=rect(-2000, -300, d - stem / 2 - 3, 60))
    return union(V, I, cap_r, cap_l, *br)


def r3d():
    """Beam: hairline I exactly cap-to-baseline, crossing the thick arm, inverted to white inside it."""
    V, g = didone_V(L=450, R=420, thick=210, thin=32)
    x = -205
    w = 28
    I = didone_I(x, 0, H, stem=w, sw=40, sh=20, br=10)
    I_out = difference(I, dilate(V, 22))
    V2 = difference(V, rect(x - w / 2, -900, x + w / 2, 2900))
    return union(V2, I_out)


def r3e():
    """Shared stem by shear: the V is backslanted until its hairline arm stands vertical — that arm is the I."""
    k = 0.40
    V, g = didone_V(L=400, R=400, thick=60, thin=170, serifs=False, os_=0)
    V = transform(V, 1, 0, -k, 1, 0, 0)  # shear x' = x - k*y
    I = didone_I(0 + 85 - 10, -60, H, stem=170, sw=80, head=True, foot=True)
    return union(V, I)


def r3f():
    """Hidden I: a vertical I-shaped window cut through the V's thick arm."""
    V, g = didone_V(L=460, R=430, thick=230, thin=32)
    # centre of the thick arm at mid height
    yc = 560
    xl = x_at(g['A'], g['P'], yc)
    xr = x_at(g['A2'], g['J'], yc)
    xc = (xl + xr) / 2
    w, hh, sw, sh = 26, 300, 46, 18
    slot = union(rect(xc - w / 2, yc - hh / 2, xc + w / 2, yc + hh / 2),
                 rect(xc - sw, yc + hh / 2 - sh, xc + sw, yc + hh / 2),
                 rect(xc - sw, yc - hh / 2, xc + sw, yc - hh / 2 + sh))
    return difference(V, slot)


def r3g():
    """Split V: thick and hairline arms parted by a vertical I-shaped channel at the vertex."""
    V, g = didone_V(L=450, R=420, thick=200, thin=34)
    w = 30
    ch = rect(-w / 2 + 6, -200, w / 2 + 6, 300)
    cap = rect(-60 + 6, 300 - 22, 60 + 6, 300)
    return difference(V, union(ch, cap))


def r3h():
    """Dropped V + tall I, hairline arm passes BEHIND the stem top-left; foot weaves over."""
    return r3a(join=True, drop=200)


def r3i():
    """Staggered pair, both letters full-weight geometric (Deco), I foot cuts the V's arm."""
    w = 140
    L = 430
    drop = 260
    left = stroke_quad((-L, H + 30 - drop), (0, -70 - drop), w)
    right = stroke_quad((L, H + 30 - drop), (0, -70 - drop), w)
    V = intersection(union(left, right), rect(-900, -drop - 40, 900, H - drop))
    d = L + w / 2 + 40
    I = rect(d - w / 2, 0, d + w / 2, H)
    foot = rect(60, 0, d, 46)
    V = over(foot, V, 30, region=rect(-100, -100, 500, 120))
    return union(V, I, foot)


EXPL = [('a dropped V, joined hairline', r3a), ('b dropped V, free', r3b), ('c ligature shared cap v2', r3c),
        ('d beam cap-to-baseline', r3d), ('e sheared shared stem', r3e), ('f hidden I window', r3f),
        ('g split vertex channel', r3g), ('h dropped V, drop 200', r3h), ('i deco staggered', r3i)]

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
        fn_ = os.path.join(OUT, f'r3_{i + 1}.svg')
        write_svg(fn_, S, S, body, bg=IVORY)
        files.append(fn_)
    subprocess.run(['node', os.path.join(HERE, '..', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore_r3.png')] + files, check=True)
    print('ok')
