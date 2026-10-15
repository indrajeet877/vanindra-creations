"""Round-2 exploration: better-balanced V+I constructions."""
import math
import os
import subprocess
import sys
from mono import *  # noqa
from explore import didone_V, didone_I, stroke_quad, H

OUT = os.path.join(HERE, 'explore')


def cipher(L=470, R=450, thick=180, thin=32, d=230, stem=150, drop=170, rise=0, sw=84, gap=26, foot_l=-150):
    """V lowered by `drop`; I stands right, stem crosses thin arm (I over); V point passes over I's foot serif."""
    V, g = didone_V(L=L, R=R, thick=thick, thin=thin)
    V = move(V, 0, -drop)
    I = didone_I(d, 0, H + rise, stem=stem, sw=sw, foot_l=foot_l)
    stemr = rect(d - stem / 2, -900, d + stem / 2, 2900)
    V = over(stemr, V, gap, region=rect(d - 400, 0 + 60, d + 400, H))       # I over V's thin arm
    I = over(intersection(V, rect(-2000, -2000, 2000, 120)), I, gap, region=rect(-2000, -200, d - stem / 2 - 2, 80))
    return union(V, I)


def r2a():
    return cipher()


def r2b():
    return cipher(L=520, R=500, d=190, stem=140, drop=120, rise=120, foot_l=-180)


def r2c():
    """Ligature: I right of V, cap hairline shared, foot serif woven under V point."""
    L, R = 450, 410
    V, g = didone_V(L=L, R=R, serifs=False)
    drop = 90
    V = move(V, 0, -drop)
    sh = 22
    d = R + 110
    stem = 150
    I = didone_I(d, 0, H - drop, stem=stem, sw=80, head=False, foot_l=-160)
    cap = rect(R - 32 - 36, H - drop - sh, d + stem / 2 + 80, H - drop)
    capl = rect(-L - 58, H - drop - sh, -L + 180 + 36, H - drop)
    I = over(intersection(V, rect(-2000, -2000, 2000, 120)), I, 26, region=rect(-2000, -300, d - 80, 80))
    br = [bracket((d - stem / 2, H - drop - sh), (-1, 0), (0, -1), 26, 42), bracket((d + stem / 2, H - drop - sh), (1, 0), (0, -1), 26, 42)]
    return union(V, I, cap, capl, *br)


def r2d():
    """Beam: hairline tall I pierces the thick arm; inverts to a white line inside the arm."""
    V, g = didone_V(L=450, R=420, thick=200, thin=32)
    x = -235
    w = 30
    I = didone_I(x, -230, H + 230, stem=w, sw=46, sh=20, br=10)
    inside = intersection(I, V)
    V = difference(V, dilate(inside, 0))
    out = difference(I, dilate(g_V := V, 0))
    beam_in = intersection(rect(x - w / 2, -900, x + w / 2, 2900), didone_V(L=450, R=420, thick=200, thin=32)[0])
    V2 = didone_V(L=450, R=420, thick=200, thin=32)[0]
    I_out = difference(I, V2)
    V2 = difference(V2, rect(x - w / 2, -900, x + w / 2, 2900))
    return union(V2, I_out)


def r2e():
    """Two leaning pillars (each an I) form a split V, Roman-inscription serifs."""
    a = math.radians(22)
    gap = 36
    parts = []
    for s, w in ((-1, 176), (1, 40)):
        top = (s * (math.tan(a) * (H + 10) + gap / 2), H)
        bot = (s * gap / 2, -10)
        # quad with outer edge through top->bot
        if s < 0:
            q = poly([top, (top[0] + w, H), (bot[0] + w * 0.0 + 0, bot[1] + w / math.tan(a) * 0.0), bot])
            # inner edge parallel
            inner_top = (top[0] + w, H)
            inner_bot = (bot[0], bot[1] + w / math.tan(a))
            q = poly([top, inner_top, inner_bot, bot])
        else:
            inner_top = (top[0] - w, H)
            inner_bot = (bot[0], bot[1] + w / math.tan(a))
            q = poly([inner_top, top, bot, inner_bot])
        parts.append(q)
        y = H - 22
        x0, x1 = sorted([top[0], inner_top[0]])
        parts.append(rect(x0 - 60, y, x1 + 60, H))
    return intersection(union(*parts), rect(-2000, -10, 2000, H))


def r2f():
    """Interlocked chevrons V and Λ (chain link), thick/thin, alternating over/under."""
    V, g = didone_V(L=420, R=420, thick=170, thin=34, serifs=False)
    Lam = rot(V, 180, 0, H / 2)
    Lam = move(Lam, 0, -360)
    V = move(V, 0, 0)
    left = rect(-2000, -2000, 0, 3000)
    right = rect(0, -2000, 2000, 3000)
    Lam_c = over(V, Lam, 24, region=left)
    V_c = over(Lam, V, 24, region=right)
    return union(V_c, Lam_c)


def r2g():
    """Reverse spine: the V's right arm is a heavy italic I (horizontal serifs), left arm a hairline."""
    V, g = didone_V(L=430, R=450, thick=32, thin=190, serifs=True)
    # extend into a foot serif under the point
    foot = rect(-80, -16, 220, 6)
    return union(V, foot)


def r2h():
    """Typographic reference: Bodoni Moda V + I overlapped with interlace."""
    f = vtype.bodoni_variable()
    Vg = vtype.text_path('V', file=f, variations={'opsz': 96, 'wght': 500}, size=1400)
    Ig = vtype.text_path('I', file=f, variations={'opsz': 96, 'wght': 500}, size=1400)
    V = transform(Vg.path, 1, 0, 0, -1, 0, 0)
    I = transform(Ig.path, 1, 0, 0, -1, 0, 0)
    vb = bounds(V)
    ib = bounds(I)
    I = move(I, vb[2] - (ib[2] - ib[0]) * 1.35 - ib[0], 0)
    stem = intersection(I, rect(-5000, 60, 5000, 900))
    V = over(stem, V, 24)
    return union(V, I)


def r2i():
    """Cipher with a narrower, taller (Vogue-condensed) V and a taller pillar."""
    return cipher(L=360, R=340, thick=160, thin=28, d=175, stem=130, drop=60, rise=200, sw=70, foot_l=-120)


EXPL = [('A cipher (staggered)', r2a), ('B cipher wide + tall I', r2b), ('C ligature shared cap', r2c),
        ('D beam / figure-ground', r2d), ('E split pillars', r2e), ('F interlocked chevrons', r2f),
        ('G reverse spine', r2g), ('H Bodoni reference', r2h), ('I condensed cipher', r2i)]

if __name__ == '__main__':
    files = []
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
        fn_ = os.path.join(OUT, f'r2_{i + 1}.svg')
        write_svg(fn_, S, S, body, bg=IVORY)
        files.append(fn_)
    subprocess.run(['node', os.path.join(HERE, '..', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore_r2.png')] + files, check=True)
    print('ok')
