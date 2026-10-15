"""Round-1 exploration: 9 interlocking V+I constructions (math coords, cap H = 1000)."""
import math
import os
import subprocess
from mono import *  # noqa: F401,F403

OUT = os.path.join(HERE, 'explore')
os.makedirs(OUT, exist_ok=True)
H = 1000


def didone_V(L=440, R=420, thick=190, thin=34, os_=16, serifs=True, sh=22, so=58, si=36, br=26, top=H):
    P = (0, -os_)
    A, B = (-L, top), (R, top)
    A2, B2 = (-L + thick, top), (R - thin, top)
    dA = (P[0] - A[0], P[1] - A[1])
    dB = (P[0] - B[0], P[1] - B[1])
    J = isect(A2, (A2[0] + dA[0], A2[1] + dA[1]), B2, (B2[0] + dB[0], B2[1] + dB[1]))
    parts = [poly([A, A2, J, B2, B, P])]
    geo = dict(P=P, A=A, B=B, A2=A2, B2=B2, J=J)
    if serifs:
        y = top - sh
        parts.append(rect(-L - so, y, -L + thick + si, top))
        parts.append(rect(R - thin - si, y, R + so * 0.8, top))
        for (p1, p2, side) in [(A, P, -1), (A2, J, +1), (B2, J, -1), (B, P, +1)]:
            c = (x_at(p1, p2, y), y)
            parts.append(bracket(c, (side, 0), unit((p2[0] - p1[0], p2[1] - p1[1])), br, br * 1.6))
    return union(*parts), geo


def didone_I(x, y0=0, y1=H, stem=180, sw=96, sh=22, br=26, head=True, foot=True, foot_l=None, foot_r=None,
             head_l=None, head_r=None):
    s2 = stem / 2
    parts = [rect(x - s2, y0, x + s2, y1)]
    if head:
        hl = head_l if head_l is not None else x - s2 - sw
        hr = head_r if head_r is not None else x + s2 + sw
        parts.append(rect(hl, y1 - sh, hr, y1))
        for sx in (-1, 1):
            c = (x + sx * s2, y1 - sh)
            parts.append(bracket(c, (sx, 0), (0, -1), br, br * 1.6))
    if foot:
        fl = foot_l if foot_l is not None else x - s2 - sw
        fr = foot_r if foot_r is not None else x + s2 + sw
        parts.append(rect(fl, y0, fr, y0 + sh))
        for sx in (-1, 1):
            c = (x + sx * s2, y0 + sh)
            parts.append(bracket(c, (sx, 0), (0, 1), br, br * 1.6))
    return union(*parts)


def stroke_quad(p0, p1, w):
    """Straight stroke of perpendicular width w along centreline p0->p1."""
    d = unit((p1[0] - p0[0], p1[1] - p0[1]))
    n = (-d[1] * w / 2, d[0] * w / 2)
    return poly([(p0[0] + n[0], p0[1] + n[1]), (p1[0] + n[0], p1[1] + n[1]),
                 (p1[0] - n[0], p1[1] - n[1]), (p0[0] - n[0], p0[1] - n[1])])


# ---------------- explorations ----------------
def e1_pillar():
    """Tall I pillar threaded over the V's hairline arm."""
    V, g = didone_V()
    d = 165
    I = didone_I(d, -170, H + 170, stem=176)
    stem = rect(d - 88, -400, d + 88, H + 400)
    V = over(stem, V, 30, region=rect(0, 100, 600, 800))
    return union(V, I)


def e2_leaning():
    """V built from two I-strokes leaning on each other, crossing at the foot."""
    c = (0, 110)
    a = math.radians(22)
    L1 = ((-math.tan(a) * (H - c[1]), H), (math.tan(a) * (c[1] + 130), -130))
    L2 = ((math.tan(a) * (H - c[1]), H), (-math.tan(a) * (c[1] + 130), -130))
    s1 = stroke_quad(L1[0], L1[1], 160)
    s2 = stroke_quad(L2[0], L2[1], 160)

    def caps(p0, p1, w, sw=70, sh=22):
        d = unit((p1[0] - p0[0], p1[1] - p0[1]))
        n = (-d[1], d[0])
        out = []
        for p, s in ((p0, 1), (p1, -1)):
            q = [(p[0] + n[0] * (w / 2 + sw), p[1] + n[1] * (w / 2 + sw)), (p[0] - n[0] * (w / 2 + sw), p[1] - n[1] * (w / 2 + sw))]
            q += [(q[1][0] + d[0] * sh * s, q[1][1] + d[1] * sh * s), (q[0][0] + d[0] * sh * s, q[0][1] + d[1] * sh * s)]
            out.append(poly(q))
        return union(*out)
    s1 = union(s1, caps(*L1, 160))
    s2 = union(s2, caps(*L2, 160))
    s2 = over(s1, s2, 28)
    shape = union(s1, s2)
    return intersection(shape, rect(-2000, -2000, 2000, H))


def e3_knot():
    """Crossed V + I: three strands, each over one and under one."""
    c = (0, 170)
    L, R = 430, 410
    tail = -150
    la = ((-L, H), (x_at((-L, H), c, tail), tail))
    ra = ((R, H), (x_at((R, H), c, tail), tail))
    left = poly([la[0], (la[0][0] + 185, H), (la[1][0] + 185, tail), la[1]])
    right = poly([(ra[0][0] - 34, H), ra[0], ra[1], (ra[1][0] - 34, tail)])
    d = 120
    I = didone_I(d, tail, H, stem=150, foot=True, head=True)
    stem = rect(d - 75, -900, d + 75, 1900)
    right = over(left, right, 26)                       # thick over thin at the crossing
    right = over(stem, right, 26, region=rect(-900, c[1] + 40, 900, 900))  # I over thin arm
    I = over(left, I, 26, region=rect(-900, tail + 30, 900, c[1] - 10))     # thick tail over I
    return union(left, right, I)


def e4_rotunit():
    """Point-symmetric tile unit: V | shared pillar | Λ."""
    V, g = didone_V(L=400, R=380, thick=170, thin=30)
    d = 150
    I = didone_I(d, -60, H + 60, stem=160, sw=70)
    stem = rect(d - 80, -400, d + 80, H + 400)
    V = over(stem, V, 26, region=rect(0, 60, 600, 900))
    unitp = union(V, I)
    Lam = rot(V, 180, d, H / 2)
    Lam = over(stem, Lam, 26, region=rect(-900, 100, 900, 940))
    return union(V, Lam, I)


def e5_hidden():
    """Bold geometric V; an I is cut out of its vertex as negative space."""
    L = 440
    P = (0, -20)
    t = 230
    body = poly([(-L, H), (-L + t, H), (0, H - (H + 20) * t / L * 0.92), (L - t, H), (L, H), P])
    g = 46
    slit = rect(-g / 2, -200, g / 2, 360)
    serif = rect(-110, 360 - g * 0.9, 110, 360)
    neg = union(slit, serif)
    return difference(body, neg)


def e6_sharedcap():
    """V and I share one cap hairline; I crosses the hairline arm; V's point passes over the I's foot."""
    V, g = didone_V(L=440, R=400, serifs=False)
    d = 175
    sh = 22
    I = didone_I(d, -150, H, stem=176, head=False, foot_l=-330, foot_r=d + 88 + 96)
    cap = rect(d - 88 - 96, H - sh, 400 + 50, H)
    capl = rect(-440 - 58, H - sh, -440 + 190 + 36, H)
    stem = rect(d - 88, -400, d + 88, H + 400)
    V = over(stem, V, 30, region=rect(0, 100, 600, 900))
    # extend V point down so it crosses the foot serif
    Vext, _ = didone_V(L=440 * 1.22, R=400 * 1.22, top=H * 1.22 - 0.22 * 0, serifs=False)
    Vext = move(Vext, 0, -0.22 * H)
    Vext = intersection(Vext, rect(-900, -400, 900, 200))
    V = union(V, Vext)
    I = over(intersection(V, rect(-900, -400, 900, 0)), I, 26, region=rect(-900, -300, 900, 40))
    return union(V, I, cap, capl)


def e7_engraved():
    """Engraved inline version of the pillar interlace."""
    base = e1_pillar()
    inner = erode(base, 26)
    inner2 = erode(base, 44)
    return difference(base, difference(inner, inner2))


def e8_vic():
    """V + I + C: a Didone C threaded on the pillar, weaving over/under."""
    V, g = didone_V()
    d = 165
    I = didone_I(d, -100, H + 100, stem=168)
    cx, cy, r = d, 430, 300
    outer = circle(cx, cy, r)
    inner = transform(circle(0, 0, 1), r - 150, 0, 0, r - 30, cx + 38, cy)
    ring = difference(outer, inner)
    wedge = poly([(cx, cy), (cx + 900, cy + 640), (cx + 900, cy - 640)])
    C = difference(ring, wedge)
    stem = rect(d - 84, -900, d + 84, 1900)
    V = over(stem, V, 26, region=rect(0, 100, 600, 380))
    C = over(stem, C, 24, region=rect(-900, cy - 80, 900, 1900))   # pillar over C at top
    I = over(C, I, 24, region=rect(-900, -900, 900, cy - 80))      # C over pillar at bottom
    V = over(C, V, 24, region=rect(-900, -900, 900, 900))
    return union(V, I, C)


def e9_geometric():
    """Bold monoline geometric VI with stencil breaks (Fendi-weight)."""
    w = 150
    L = 430
    left = stroke_quad((-L, H + 40), (0, -60), w)
    right = stroke_quad((L, H + 40), (0, -60), w)
    V = intersection(union(left, right), rect(-900, -60, 900, H))
    d = 210
    I = rect(d - w / 2, -60, d + w / 2, H)
    V = over(I, V, 34)
    return union(V, I)


EXPL = [('E1 pillar interlace', e1_pillar), ('E2 leaning pillars', e2_leaning), ('E3 three-strand knot', e3_knot),
        ('E4 rotational unit', e4_rotunit), ('E5 hidden I', e5_hidden), ('E6 shared cap + chain foot', e6_sharedcap),
        ('E7 engraved inline', e7_engraved), ('E8 V+I+C weave', e8_vic), ('E9 geometric stencil', e9_geometric)]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(EXPL):
        p = to_svg_space(fn())
        S = 600
        big, _ = place(p, 110, 90, 380, 380)
        small = []
        for k, sz in enumerate((48, 24, 16)):
            sp, _ = place(p, 150 + k * 90, 505, sz, sz)
            small.append(path_el(sp, EMERALD))
        lab = vtype.text_path(name, family='jost', weight=400, size=22, x=24, y=578)
        body = path_el(big, EMERALD) + ''.join(small) + path_el(lab.path, '#777')
        fn_ = os.path.join(OUT, f'e{i + 1}.svg')
        write_svg(fn_, S, S, body, bg=IVORY)
        files.append(fn_)
    subprocess.run(['node', os.path.join(HERE, '..', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore_r1.png')] + files, check=True)
    print('ok')
