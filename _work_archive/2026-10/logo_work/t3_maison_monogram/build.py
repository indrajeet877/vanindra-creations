"""VanIndra Creations — t3 Maison Monogram: 'The Threaded VI'.

Construction (math coords, y-up, cap height H = 1000, baseline 0):
  * A Didone V: thick left arm, hairline right arm, hairline serifs with small brackets, vertex overshoot.
  * A small-capital I (~0.82 H) is threaded through the V's hairline arm: the hairline passes OVER the I's
    stem (two hairline gaps cut the stem), the I's head sits inside the V's counter, its foot stands outside.
  * The I is placed analytically inside the slanted channel between the V's point (foot clearance) and the
    hairline (head clearance), so both clearances are identical and perpendicular to the hairline.
"""
import json
import math
import os
import subprocess
import sys

from mono import *  # noqa

H = 1000.0
TK = os.path.join(HERE, '..', 'toolkit', 'render.js')
OUT = HERE


# ----------------------------------------------------------------------------------------------
# Letter construction
# ----------------------------------------------------------------------------------------------
def v_letter(L, R, thick, thin, os_, sh, so_l, si_l, si_r, so_r, br_u, br_v, top=H, serifs=True):
    P = (0.0, -os_)
    A, B = (-L, top), (R, top)
    A2, B2 = (-L + thick, top), (R - thin, top)
    dA = (P[0] - A[0], P[1] - A[1])
    dB = (P[0] - B[0], P[1] - B[1])
    J = isect(A2, (A2[0] + dA[0], A2[1] + dA[1]), B2, (B2[0] + dB[0], B2[1] + dB[1]))
    parts = [poly([A, A2, J, B2, B, P])]
    if serifs:
        y = top - sh
        parts.append(rect(-L - so_l, y, -L + thick + si_l, top))
        parts.append(rect(R - thin - si_r, y, R + so_r, top))
        for (p1, p2, side) in [(A, P, -1), (A2, J, +1), (B2, J, -1), (B, P, +1)]:
            c = (x_at(p1, p2, y), y)
            parts.append(bracket(c, (side, 0), unit((p2[0] - p1[0], p2[1] - p1[1])), br_u, br_v))
    hair = poly([P, B, B2, J])
    return union(*parts), dict(P=P, A=A, B=B, A2=A2, B2=B2, J=J, hair=hair)


def i_letter(x, y0, y1, stem, sw, sh, br_u, br_v):
    s2 = stem / 2
    parts = [rect(x - s2, y0, x + s2, y1), rect(x - s2 - sw, y1 - sh, x + s2 + sw, y1), rect(x - s2 - sw, y0, x + s2 + sw, y0 + sh)]
    for sx in (-1, 1):
        parts.append(bracket((x + sx * s2, y1 - sh), (sx, 0), (0, -1), br_u, br_v))
        parts.append(bracket((x + sx * s2, y0 + sh), (sx, 0), (0, 1), br_u, br_v))
    return union(*parts)


MASTER = dict(
    L=520, R=520,          # outer half-widths of the V at cap height
    thick=186, thin=31,    # horizontal widths of thick arm / hairline
    os_=16,                # vertex overshoot
    sh=23,                 # serif thickness (horizontal hairlines a touch thinner than the diagonal hairline)
    so_l=58, si_l=36, si_r=36, so_r=50,
    br_u=24, br_v=40,
    stem=150, isw=56, ish=23, ibr_u=22, ibr_v=36,
    clear_b=58,            # perpendicular clearance: I foot-serif corner <-> V point (outer edge)
    clear_t=44,            # perpendicular clearance: I head-serif corner <-> hairline (inner edge)
    gap=18,                # perpendicular gap either side of the hairline where it passes over the stem
)

SMALL = dict(MASTER, L=575, R=575, thick=262, thin=74, sh=54, so_l=40, si_l=22, si_r=22, so_r=34, br_u=0.001, br_v=0.001,
             stem=178, isw=30, ish=54, ibr_u=0.001, ibr_v=0.001, clear_b=56, clear_t=50, gap=52, os_=22)


def monogram(p=MASTER, report=False):
    V, g = v_letter(p['L'], p['R'], p['thick'], p['thin'], p['os_'], p['sh'], p['so_l'], p['si_l'], p['si_r'],
                    p['so_r'], p['br_u'], p['br_v'])
    R, os_, t = p['R'], p['os_'], p['thin']
    ca = math.cos(math.atan(R / (H + os_)))
    xo = lambda y: R * (y + os_) / (H + os_)  # noqa: E731  outer edge of the hairline
    mb, mt = p['clear_b'] / ca, p['clear_t'] / ca
    half = p['stem'] / 2 + p['isw']
    # foot: I foot-serif's top-left corner clears the V's outer right edge by clear_b (perpendicular)
    d = xo(p['ish']) + mb + half
    # head: I head-serif's bottom-right corner clears the hairline's inner edge by clear_t
    itop = (d + half + mt + t) * (H + os_) / R - os_ + p['ish']
    I = i_letter(d, 0, itop, p['stem'], p['isw'], p['ish'], p['ibr_u'], p['ibr_v'])
    hair = intersection(V, g['hair'])
    I = over(hair, I, p['gap'])
    shape = union(V, I)
    if report:
        s_l, s_r = d - p['stem'] / 2, d + p['stem'] / 2
        y_in = s_l * (H + os_) / R - os_
        y_out = (s_r + t) * (H + os_) / R - os_
        print(f'  I centre x={d:.1f}  I height={itop:.1f}  crossing y {y_in:.0f}..{y_out:.0f}  J={g["J"][0]:.0f},{g["J"][1]:.0f}')
    return shape, dict(d=d, itop=itop, g=g)


# ----------------------------------------------------------------------------------------------
# Wordmark
# ----------------------------------------------------------------------------------------------
BOD = vtype.bodoni_variable()


def word_glyphs(text, size, wght=500, opsz=96, tracking=0.0, kern=None, custom=True):
    """Bodoni Moda (opsz 96) set in y-down space with custom V and I drawn from the monogram system."""
    gl = vtype.glyph_paths(text, file=BOD, variations={'opsz': opsz, 'wght': wght}, size=size, tracking=tracking)
    cap = 0.75 * size
    stem = 0.149 * cap * (1 + (wght - 500) / 1000 * 1.1)
    out = []
    x = 0.0
    for i, ch in enumerate(text):
        g = gl[i]
        k = (kern or {}).get(i, 0.0) * size
        x += k
        b = g.bounds
        if custom and ch in 'VI':
            # build in math coords at cap=1000, scale to cap, flip to y-down
            s = cap / H
            if ch == 'V':
                shape, _ = v_letter(470, 470, stem / s / math.cos(math.atan(470 / 1016)) * 1.02, 0.30 * stem / s * 0.9 + 6,
                                    16, 24, 54, 34, 34, 46, 22, 36)
            else:
                shape = i_letter(0, 0, H, stem / s, 64, 24, 22, 36)
            sb = bounds(shape)
            shape = transform(shape, s, 0, 0, -s, 0, 0)
            sbb = bounds(shape)
            # keep original sidebearings: left edge at glyph's left bound
            lsb = b[0] - 0  # glyph left bound relative to its origin x (glyph already positioned)
            gx0 = b[0]
            p = move(shape, gx0 - sbb[0], 0)
            width_new = sbb[2] - sbb[0]
            width_old = b[2] - b[0]
            dx_after = width_new - width_old
            p = move(p, x, 0)
            out.append(p)
            x += dx_after
        else:
            out.append(move(g.path, x, 0))
    return union(*out)


WM_OPSZ, WM_WGHT = 11, 500
WM_KERN = {1: -0.050, 2: -0.006, 3: 0.010, 4: 0.006, 5: -0.008, 6: -0.002, 7: -0.028}
WM_TRACK = -0.012


def wordmark_paths(style='mixed', size=1000):
    if style == 'mixed':
        # kerning in em, applied BEFORE glyph i (optical spacing, judged at 1200 px and at 40 px)
        w = word_glyphs('VanIndra', size, wght=WM_WGHT, opsz=WM_OPSZ, tracking=WM_TRACK, kern=WM_KERN, custom=False)
    else:
        kern = {1: -0.060, 2: 0.0, 3: 0.006, 4: 0.006, 5: -0.004, 6: -0.006, 7: -0.030}
        w = word_glyphs('VANINDRA', size, wght=WM_WGHT, opsz=WM_OPSZ, tracking=0.03, kern=kern, custom=False)
    return w


SUB_TRACK = 0.30


def sub_line(text, size, tracking=None):
    """CREATIONS in Jost 400, fixed optical tracking."""
    t = vtype.text_path(text, family='jost', weight=400, size=size, tracking=SUB_TRACK if tracking is None else tracking)
    return t.path


def word_block(style='mixed', size=1000, sub_ratio=0.275, gap_ratio=0.27, align='left'):
    w = wordmark_paths(style, size)
    wb = bounds(w)
    w = move(w, -wb[0], 0)
    wb = bounds(w)
    width = wb[2] - wb[0]
    sub_size = size * sub_ratio
    s = sub_line('CREATIONS', sub_size)
    sb = bounds(s)
    cap = 0.75 * size
    y_sub = gap_ratio * size + (sb[3] - sb[1])
    if align == 'left':
        s = move(s, -sb[0], y_sub - sb[3])
    else:
        s = move(s, -sb[0] + (width - (sb[2] - sb[0])) / 2, y_sub - sb[3])
    return w, s


# ----------------------------------------------------------------------------------------------
# Assembly helpers (y-down)
# ----------------------------------------------------------------------------------------------
def mark_svgspace(p=MASTER):
    m, info = monogram(p)
    return to_svg_space(m), info


def fit(path, x, y, w, h):
    return place(path, x, y, w, h)


def optical_center_square(path, S, frac=0.60, dy=-0.012):
    """Place mark in a square, height = frac*S, nudged up slightly (optical centre)."""
    b = bounds(path)
    h = b[3] - b[1]
    w = b[2] - b[0]
    s = frac * S / max(h, w * 0.92)
    tx = S / 2 - (b[0] + w / 2) * s
    ty = S / 2 - (b[1] + h / 2) * s + dy * S
    return transform(path, s, 0, 0, s, tx, ty)


def write(name, w, h, body, bg=None):
    fn = os.path.join(OUT, name)
    write_svg(fn, w, h, body, bg=bg)
    return fn


def build(style='mixed', variant='master'):
    mk, info = mark_svgspace(MASTER)
    mk_small, _ = mark_svgspace(SMALL)
    files = {}

    # --- mark.svg (transparent, emerald) with clear space = 1/6 of mark height
    b = bounds(mk)
    mw, mh = b[2] - b[0], b[3] - b[1]
    pad = mh / 6
    m1 = move(mk, -b[0] + pad, -b[1] + pad)
    files['mark'] = write('mark.svg', mw + 2 * pad, mh + 2 * pad, path_el(m1, EMERALD))

    # --- mark_small.svg (square, transparent, antique gold: reads on ivory AND emerald)
    S = 64
    ms = optical_center_square(mk_small, S, frac=0.86, dy=-0.005)
    files['mark_small'] = write('mark_small.svg', S, S, path_el(ms, GOLD))

    # --- squares
    S = 1000
    sq = optical_center_square(mk, S, frac=0.56)
    files['mark_on_ivory'] = write('mark_on_ivory.svg', S, S, path_el(sq, EMERALD), bg=IVORY)
    files['mark_on_emerald'] = write('mark_on_emerald.svg', S, S, path_el(sq, GOLD_LT), bg=EMERALD)
    files['mark_one_colour_gold'] = write('mark_one_colour_gold.svg', S, S, path_el(sq, GOLD))

    # --- wordmark.svg
    w, s = word_block(style)
    wb = bounds(union(w, s))
    pad = 120
    w1 = move(w, -wb[0] + pad, -wb[1] + pad)
    s1 = move(s, -wb[0] + pad, -wb[1] + pad)
    files['wordmark'] = write('wordmark.svg', wb[2] - wb[0] + 2 * pad, wb[3] - wb[1] + 2 * pad,
                              path_el(w1, EMERALD) + path_el(s1, GOLD))

    # --- horizontal lockup: mark height = text block height (cap top -> CREATIONS baseline)
    def horizontal(bg, c_mark, c_word, c_sub):
        wbk = bounds(union(w, s))
        block_h = wbk[3] - wbk[1]
        mb = bounds(mk)
        sc = block_h * 1.16 / (mb[3] - mb[1])
        m2 = transform(mk, sc, 0, 0, sc, 0, 0)
        mb2 = bounds(m2)
        gapx = (mb2[2] - mb2[0]) * 0.40
        # vertical: centre the text block on the mark's optical centre
        mcy = (mb2[1] + mb2[3]) / 2
        tcy = (wbk[1] + wbk[3]) / 2
        m2 = move(m2, -mb2[0], -mcy)
        tx = (mb2[2] - mb2[0]) + gapx - wbk[0]
        w2 = move(w, tx, -tcy)
        s2 = move(s, tx, -tcy)
        allb = bounds(union(m2, w2, s2))
        padx = (mb2[3] - mb2[1]) * 0.22
        W = allb[2] - allb[0] + 2 * padx
        Hh = allb[3] - allb[1] + 2 * padx
        ox, oy = -allb[0] + padx, -allb[1] + padx
        body = path_el(move(m2, ox, oy), c_mark) + path_el(move(w2, ox, oy), c_word) + path_el(move(s2, ox, oy), c_sub)
        return W, Hh, body

    W, Hh, body = horizontal(IVORY, EMERALD, EMERALD, GOLD)
    files['lockup_horizontal_on_ivory'] = write('lockup_horizontal_on_ivory.svg', W, Hh, body, bg=IVORY)
    W, Hh, body = horizontal(EMERALD, GOLD_LT, IVORY, GOLD_LT)
    files['lockup_horizontal_on_emerald'] = write('lockup_horizontal_on_emerald.svg', W, Hh, body, bg=EMERALD)
    W, Hh, body = horizontal(None, GOLD, GOLD, GOLD)
    files['lockup_horizontal_gold'] = write('lockup_horizontal_one_colour_gold.svg', W, Hh, body)

    # --- stacked lockup
    def stacked(c_mark, c_word, c_sub):
        wc, sc_ = word_block(style, align='center')
        wbk = bounds(union(wc, sc_))
        tw = wbk[2] - wbk[0]
        mb = bounds(mk)
        sc = tw * 0.44 / (mb[2] - mb[0])
        m2 = transform(mk, sc, 0, 0, sc, 0, 0)
        mb2 = bounds(m2)
        m2 = move(m2, -(mb2[0] + mb2[2]) / 2, -mb2[3])
        gapy = (mb2[3] - mb2[1]) * 0.30
        cx = (wbk[0] + wbk[2]) / 2
        wc = move(wc, -cx, gapy - wbk[1])
        sc_ = move(sc_, -cx, gapy - wbk[1])
        allb = bounds(union(m2, wc, sc_))
        side = max(allb[2] - allb[0], allb[3] - allb[1]) * 1.32
        ox = side / 2 - (allb[0] + allb[2]) / 2
        oy = side / 2 - (allb[1] + allb[3]) / 2
        body = path_el(move(m2, ox, oy), c_mark) + path_el(move(wc, ox, oy), c_word) + path_el(move(sc_, ox, oy), c_sub)
        return side, side, body

    W, Hh, body = stacked(EMERALD, EMERALD, GOLD)
    files['lockup_stacked_on_ivory'] = write('lockup_stacked_on_ivory.svg', W, Hh, body, bg=IVORY)
    W, Hh, body = stacked(GOLD_LT, IVORY, GOLD_LT)
    files['lockup_stacked_on_emerald'] = write('lockup_stacked_on_emerald.svg', W, Hh, body, bg=EMERALD)

    # --- monogram canvas (bonus): half-drop lattice, alternate units rotated 180 degrees
    PW, PH = 1200, 800
    unit = optical_center_square(mk, 100, frac=0.54)
    ub = bounds(unit)
    cells = []
    step_x, step_y = 150, 128
    for j in range(-1, int(PH / step_y) + 2):
        for i in range(-1, int(PW / step_x) + 2):
            x = i * step_x + (step_x / 2 if j % 2 else 0)
            y = j * step_y
            u = unit
            cells.append(move(u, x - 50 + step_x / 2, y - 50 + step_y / 2))
    pat = union(*cells)
    pat = intersection(pat, rect(0, 0, PW, PH))
    files['pattern'] = write('pattern_canvas.svg', PW, PH, path_el(pat, GOLD_LT), bg=EMERALD)
    return files


def render(files):
    order = ['mark', 'mark_small', 'wordmark', 'mark_on_ivory', 'mark_on_emerald', 'mark_one_colour_gold',
             'lockup_horizontal_on_ivory', 'lockup_horizontal_on_emerald', 'lockup_stacked_on_ivory',
             'lockup_stacked_on_emerald', 'pattern']
    subprocess.run(['node', TK, 'sheet', os.path.join(OUT, 'sheet.png')] + [files[k] for k in order], check=True)
    subprocess.run(['node', TK, 'sizes', os.path.join(OUT, 'sizes.png'), files['mark_small']], check=True)
    subprocess.run(['node', TK, 'context', os.path.join(OUT, 'context.png'), files['mark_on_emerald'],
                    files['lockup_horizontal_gold']], check=True)
    subprocess.run(['node', TK, 'png', files['mark_on_ivory'], os.path.join(OUT, 'mark_large.png'), '900'], check=True)


if __name__ == '__main__':
    style = sys.argv[1] if len(sys.argv) > 1 else 'mixed'
    print('master:')
    monogram(MASTER, report=True)
    print('small:')
    monogram(SMALL, report=True)
    f = build(style)
    if '--norender' not in sys.argv:
        render(f)
    for k, v in f.items():
        print(k, os.path.getsize(v) // 1024, 'KB')
