"""HOOK + TICK — final build. Produces every deliverable of BRIEF section 6.

Run: logo_venv/bin/python build.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from hookmark import hook_tick

HERE = os.path.dirname(os.path.abspath(__file__))
def P_(n): return os.path.join(HERE, n)

# ---------------------------------------------------------------- master geometry
MASTER = dict(H=1000.0, t=9 / 16, p=125.0, cut=9 / 16, g=24.0, over=30.0)
SMALL = dict(H=1000.0, t=9 / 16, p=178.0, cut=9 / 16, g=70.0, over=0.0)


def mark_paths(spec=MASTER):
    tk, hk, m = hook_tick(**spec)
    return tk, hk


def centroid(path, n=220):
    """Area centroid by scan sampling (good to ~0.2%)."""
    x0, y0, x1, y1 = vt.bounds(path)
    sx = sy = cnt = 0
    for i in range(n):
        y = y0 + (i + 0.5) * (y1 - y0) / n
        for j in range(n):
            x = x0 + (j + 0.5) * (x1 - x0) / n
            if path.contains((x, y)):
                sx += x; sy += y; cnt += 1
    return sx / cnt, sy / cnt


def place_square(paths, size, frac, optical=0.5):
    """Scale union of paths so its larger side = frac*size, centred between bbox centre and area centroid."""
    allp = U(*paths)
    x0, y0, x1, y1 = vt.bounds(allp)
    s = frac * size / max(x1 - x0, y1 - y0)
    cx, cy = centroid(allp)
    bx, by = (x0 + x1) / 2, (y0 + y1) / 2
    ox = bx + (cx - bx) * optical
    oy = by + (cy - by) * optical
    tx = size / 2 - ox * s
    ty = size / 2 - oy * s
    return [tf(q, s, tx, ty) for q in paths]



def set_word(text, family, weight, size, tracking, kern=None):
    # glyph_paths already places each glyph at its shaped (kerned) position; add only the extra space
    gl = vt.glyph_paths(text, family=family, weight=weight, size=size, tracking=0.0)
    out = []
    extra = 0.0
    for i, g in enumerate(gl):
        out.append(tf(g.path, 1, extra, 0))
        if i < len(gl) - 1:
            extra += tracking * size + (kern or {}).get(text[i:i + 2], 0.0) * size
    return out

# ---------------------------------------------------------------- wordmark
# "VANINDRA": Jost 500 for N, I, D, R; the V and both A's are redrawn on the brand angle (t = 9/16),
# with the same perpendicular stroke as Jost's stem, so the mark's diagonal runs through the word.
FS = 200.0            # font size
TRACK = 0.12          # em, applied between every pair
KERN = {'VA': 0.0, 'AN': 0.0, 'NI': 0.010, 'IN': 0.010, 'ND': 0.004, 'DR': -0.004, 'RA': -0.030}
SUB_SIZE = 0.37       # CREATIONS size relative to FS
SUB_TRACK = 0.30      # em


def jost_metrics(weight=500, size=FS):
    g = vt.glyph_paths('I', family='jost', weight=weight, size=size)[0]
    x0, y0, x1, y1 = g.bounds
    return x1 - x0, -y0  # stem, cap height


def brand_vee(capH, stem, apex_up=False, t=9 / 16, over_frac=0.045):
    a = math.atan(t)
    w = stem / math.cos(a)
    over = capH * over_frac
    O = V(0, over)
    Lo = V(-t * (capH + over), -capH); Li = V(-t * (capH + over) + w, -capH)
    Ro = V(t * (capH + over), -capH); Ri = V(t * (capH + over) - w, -capH)
    cr = isect(Li, (t, 1), Ri, (-t, 1))
    p = poly([O, Ro, Ri, cr, Li, Lo])
    if apex_up:
        p = vt.transform(p, 1, 0, 0, -1, 0, -capH)  # apex at top (y = -capH - over), feet on baseline
    return p, w


def brand_A(capH, stem):
    p, w = brand_vee(capH, stem, apex_up=True)
    x0, y0, x1, y1 = vt.bounds(p)
    bar_h = stem * 0.78
    yc = -capH * 0.31
    hull = poly([((x0 + x1) / 2, y0), (x1, y1), (x0, y1)])
    bar = I(rect(x0, yc - bar_h / 2, x1 - x0, bar_h), hull)
    return U(p, bar)


BRAND_KERN = {  # manual kerns (em) for pairs that touch a redrawn V/A (font kerning no longer applies there)
    'AN': 0.0, 'RA': -0.030, 'EA': -0.012, 'AT': -0.045, 'DR': -0.004,
}


def custom_word(text, weight, size, tracking, kern=None, nest_VA=True):
    """Set `text` in Jost `weight`; every V and A is redrawn on the brand angle with Jost's stem."""
    kern = dict(kern or {})
    stem, capH = jost_metrics(weight, size)
    gl = vt.glyph_paths(text, family='jost', weight=weight, size=size)
    gI = vt.glyph_paths('I', family='jost', weight=weight, size=size)[0]
    gN = vt.glyph_paths('N', family='jost', weight=weight, size=size)[0]
    G = (gI.width - gI.bounds[2]) + gN.bounds[0] + tracking * size   # stem-to-stem gap
    t = 9 / 16
    sb = 0.6 * size / 200.0
    out = []
    x = 0.0
    for i, ch in enumerate(text):
        if ch in 'VA':
            q = brand_vee(capH, stem)[0] if ch == 'V' else brand_A(capH, stem)
            qb = vt.bounds(q)
            if nest_VA and i > 0 and text[i - 1] == 'V' and ch == 'A':
                vb = vt.bounds(out[-1])
                v_right_base = vb[2] - t * capH       # V's right outer edge, at the baseline
                q = tf(q, 1, v_right_base + G - qb[0], 0)  # parallel channel, equal in area to a stem gap
            else:
                q = tf(q, 1, x + sb - qb[0], 0)
            out.append(q)
            x = vt.bounds(q)[2] + sb
        else:
            g = gl[i]
            origin = sum(q_.width for q_ in gl[:i])
            out.append(tf(g.path, 1, x - origin, 0))
            x += g.width
        if i < len(text) - 1:
            pair = text[i:i + 2]
            if not (nest_VA and pair == 'VA'):
                x += tracking * size + (kern.get(pair, BRAND_KERN.get(pair, 0.0)) if ('A' in pair or 'V' in pair) else kern.get(pair, 0.0)) * size
    return out, capH, stem


def wordmark_letters():
    return custom_word('VANINDRA', 500, FS, TRACK, KERN)


def wordmark_paths():
    letters, capH, stem = wordmark_letters()
    top = U(*letters)
    tb = vt.bounds(top)
    size2 = FS * SUB_SIZE
    sub_ = U(*custom_word('CREATIONS', 400, size2, SUB_TRACK)[0])
    sb = vt.bounds(sub_)
    gap = capH * 0.52
    # flush left: round C overshoots the V's top-left corner by 1% of its height
    sub_ = tf(sub_, 1, tb[0] - sb[0] - (sb[3] - sb[1]) * 0.01, gap - sb[1])
    return top, sub_, capH


def wordmark_oneline():
    letters, capH, stem = wordmark_letters()
    top = U(*letters)
    tb = vt.bounds(top)
    sub_ = U(*custom_word('CREATIONS', 400, FS, TRACK)[0])
    sb = vt.bounds(sub_)
    sub_ = tf(sub_, 1, tb[2] + FS * 0.30 - sb[0], 0)
    return top, sub_, capH


# ---------------------------------------------------------------- compose helpers
def colours(on):
    return (EM, GO, EM, GO) if on == 'ivory' else (IV, GL, IV, GL)  # tick, hook, word, sub


def body(items, s=1, tx=0, ty=0):
    return ''.join(pathel(tf(q, s, tx, ty), c) for q, c in items)


def save(name, w, h, items, bg=None, title='VanIndra Creations'):
    return write(P_(name), w, h, body(items), bg=bg, title=title)


def lockup_h(on):
    tk, hk = mark_paths()
    top, sub_, capH = wordmark_paths()
    tb = vt.bounds(top); sb = vt.bounds(sub_)
    block_top, block_bot = tb[1], sb[3]
    # mark spans cap-top to CREATIONS baseline (+ its own optical overshoot)
    mk = U(tk, hk); mb = vt.bounds(mk)
    s = (block_bot - block_top) / (mb[3] - MASTER['over'] - mb[1])
    tkk, hkk = tf(tk, s, 0, 0), tf(hk, s, 0, 0)
    mb = vt.bounds(U(tkk, hkk))
    dy = block_top - mb[1]
    tkk, hkk = tf(tkk, 1, -mb[0], dy), tf(hkk, 1, -mb[0], dy)
    mw = mb[2] - mb[0]
    gap = capH * 0.70
    top2 = tf(top, 1, mw + gap - tb[0], 0); sub2 = tf(sub_, 1, mw + gap - tb[0], 0)
    c = colours(on)
    items = [(tkk, c[0]), (hkk, c[1]), (top2, c[2]), (sub2, c[3])]
    ab = vt.bounds(U(*[q for q, _ in items]))
    pad = capH * 0.85
    W = ab[2] - ab[0] + 2 * pad; Hh = ab[3] - ab[1] + 2 * pad
    items = [(tf(q, 1, pad - ab[0], pad - ab[1]), col) for q, col in items]
    return W, Hh, items


def lockup_s(on):
    tk, hk = mark_paths()
    top, sub_, capH = wordmark_paths()
    tb = vt.bounds(top)
    ww = tb[2] - tb[0]
    # CREATIONS centred under VANINDRA in the stacked version
    sb = vt.bounds(sub_)
    sub_ = tf(sub_, 1, tb[0] + ww / 2 - (sb[0] + sb[2]) / 2, 0)
    mk = U(tk, hk); mb = vt.bounds(mk)
    mh = capH * 2.75
    s = mh / (mb[3] - mb[1])
    tkk, hkk = tf(tk, s, 0, 0), tf(hk, s, 0, 0)
    mb = vt.bounds(U(tkk, hkk))
    mw = mb[2] - mb[0]
    gap = capH * 0.95
    mx = tb[0] + ww / 2 - mw / 2 - mb[0]
    my = tb[1] - gap - mb[3]
    tkk, hkk = tf(tkk, 1, mx, my), tf(hkk, 1, mx, my)
    c = colours(on)
    items = [(tkk, c[0]), (hkk, c[1]), (top, c[2]), (sub_, c[3])]
    ab = vt.bounds(U(*[q for q, _ in items]))
    pad = capH * 1.2
    W = ab[2] - ab[0] + 2 * pad; Hh = ab[3] - ab[1] + 2 * pad
    items = [(tf(q, 1, pad - ab[0], pad - ab[1]), col) for q, col in items]
    return W, Hh, items


def lockup_oneline(on):
    tk, hk = mark_paths()
    top, sub_, capH = wordmark_oneline()
    tb = vt.bounds(top)
    mk = U(tk, hk); mb = vt.bounds(mk)
    mh = capH * 1.62
    s = mh / (mb[3] - MASTER['over'] - mb[1])
    tkk, hkk = tf(tk, s, 0, 0), tf(hk, s, 0, 0)
    mb = vt.bounds(U(tkk, hkk))
    over = MASTER['over'] * s
    # optical: centre mark (without overshoot) on the cap height
    cy = -capH / 2
    dy = cy - (mb[1] + (mb[3] - over)) / 2
    dx = tb[0] - capH * 0.62 - mb[2]
    tkk, hkk = tf(tkk, 1, dx, dy), tf(hkk, 1, dx, dy)
    c = colours(on)
    items = [(tkk, c[0]), (hkk, c[1]), (top, c[2]), (sub_, c[3])]
    ab = vt.bounds(U(*[q for q, _ in items]))
    pad = capH * 0.8
    W = ab[2] - ab[0] + 2 * pad; Hh = ab[3] - ab[1] + 2 * pad
    items = [(tf(q, 1, pad - ab[0], pad - ab[1]), col) for q, col in items]
    return W, Hh, items


def mark_transparent(spec, cols, size=1000, frac=0.86):
    tk, hk = mark_paths(spec)
    a, b = place_square([tk, hk], size, frac)
    return [(a, cols[0]), (b, cols[1])]


def build():
    out = []
    # mark (transparent, primary two-tone for light grounds)
    out.append(save('mark.svg', 1000, 1000, mark_transparent(MASTER, (EM, GO))))
    # mark_small: tuned for <=48px; one mid-tone colour (antique gold) legible on ivory AND emerald
    out.append(save('mark_small.svg', 1000, 1000, mark_transparent(SMALL, (GO, GO), frac=0.96)))
    out.append(save('mark_small_on_emerald.svg', 1000, 1000, mark_transparent(SMALL, (IV, GL), frac=0.80), bg=EM))
    out.append(save('mark_small_on_ivory.svg', 1000, 1000, mark_transparent(SMALL, (EM, GO), frac=0.80), bg=IV))
    # squares with backgrounds
    tk, hk = mark_paths()
    a, b = place_square([tk, hk], 1000, 0.60)
    out.append(save('mark_on_ivory.svg', 1000, 1000, [(a, EM), (b, GO)], bg=IV))
    out.append(save('mark_on_emerald.svg', 1000, 1000, [(a, IV), (b, GL)], bg=EM))
    out.append(save('mark_one_colour_gold.svg', 1000, 1000, [(a, GO), (b, GO)], bg=IV))
    out.append(save('mark_one_colour_emerald.svg', 1000, 1000, [(a, EM), (b, EM)], bg=IV))
    out.append(save('mark_one_colour_ivory.svg', 1000, 1000, [(a, IV), (b, IV)], bg=EM))
    # wordmark (transparent)
    top, sub_, capH = wordmark_paths()
    ab = vt.bounds(U(top, sub_)); pad = capH * 0.6
    W = ab[2] - ab[0] + 2 * pad; Hh = ab[3] - ab[1] + 2 * pad
    out.append(save('wordmark.svg', W, Hh, [(tf(top, 1, pad - ab[0], pad - ab[1]), EM), (tf(sub_, 1, pad - ab[0], pad - ab[1]), GO)]))
    # lockups
    for on, bg in (('ivory', IV), ('emerald', EM)):
        W, Hh, items = lockup_h(on)
        out.append(save(f'lockup_horizontal_twoline_on_{on}.svg', W, Hh, items, bg=bg))
        W, Hh, items = lockup_s(on)
        out.append(save(f'lockup_stacked_on_{on}.svg', W, Hh, items, bg=bg))
        W, Hh, items = lockup_oneline(on)
        out.append(save(f'lockup_horizontal_on_{on}.svg', W, Hh, items, bg=bg))
    out.append(construction())
    return out


def construction():
    """Construction sheet: 9:16 frame diagonals, the cut at 9/16, the tick's strokes standing 9 : 16."""
    spec = MASTER
    tk, hk, m = hook_tick(**spec)
    Hm, t, over = spec['H'], spec['t'], spec['over']
    S = 0.62; ox, oy = 700, 860
    T_ = lambda q: tf(q, S, ox, oy)
    LINE = '#9C9483'
    items = []
    def ln(a, b, wdt=2.2, col=LINE):
        pth = pathops.Path(); pth.moveTo(ox + a[0] * S, oy + a[1] * S); pth.lineTo(ox + b[0] * S, oy + b[1] * S)
        items.append((vt.stroke_to_path(pth, wdt), col))
    # the two 9:16 frames whose diagonals carry the arms
    Wf = t * (Hm + over)
    for sx in (-1, 1):
        x0 = 0 if sx > 0 else -Wf
        ln((x0, over), (x0 + Wf, over)); ln((x0 + Wf, over), (x0 + Wf, -Hm)); ln((x0 + Wf, -Hm), (x0, -Hm)); ln((x0, -Hm), (x0, over))
    ln((0, over), (Wf, -Hm), 1.4); ln((0, over), (-Wf, -Hm), 1.4)
    # cut line + baseline + cap line
    yc = -spec['cut'] * Hm
    ln((-Wf - 260, yc), (Wf + 120, yc), 1.6, GO)
    ln((-Wf - 260, 0), (Wf + 120, 0), 1.2); ln((-Wf - 260, -Hm), (Wf + 120, -Hm), 1.2)
    items.append((T_(tk), EM)); items.append((T_(hk), GO))
    def label(txt, x, y, size=30, col='#5E574B', w=400):
        r = vt.text_path(txt, family='jost', weight=w, size=size)
        items.append((tf(r.path, 1, x, y), col))
    label('9 : 16 FRAME', ox - Wf * S - 4, oy - Hm * S - 22, 24)
    label('CAP LINE', ox + (Wf + 140) * S, oy - Hm * S + 9, 22)
    label('THE CUT  9/16 H', ox + (Wf + 140) * S, oy + yc * S + 9, 22, GO, 500)
    label('BASELINE', ox + (Wf + 140) * S, oy + 9, 22)
    label('HOOK', ox + (-Wf - 250) * S, oy + (yc - 180) * S, 26, GO, 500)
    label('TICK  9 : 16', ox + (-Wf - 250) * S, oy + (yc + 200) * S, 26, EM, 500)
    label("Strokes on the diagonals of a 9:16 frame  |  one horizontal cut at 9/16 of the height", 120, 1010, 24)
    label("below the cut the strokes stand 9 : 16 (a tick)  |  above it, the hook", 120, 1050, 24)
    return save("construction.svg", 1400, 1110, items, bg=IV)


if __name__ == '__main__':
    for f in build():
        print(f, os.path.getsize(f))
