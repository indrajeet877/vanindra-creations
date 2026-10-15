"""वनिंद्रा drawn in the leaf/danda system (TO BE VERIFIED BY THE TEAM / native readers).
Same body as the Latin capitals: line top y=0, baseline y=H. Matras rise above y=0, the rakaar descends below H.
Glyph order on the line: व | ि (stem left of न, hook arching over न) | न | ं | द्र | ा
Stroke logic (same as the Latin): verticals are dandas (S), horizontals and joins are hairlines (h), every
curved or diagonal stroke is a leaf that is thin where it hangs and gains weight as it falls."""
from r3geo import *
from r3mark import leaf_bowl, MARK, va_cloop

DEVA = dict(H=100, b=8.8, S=13.0, h=5.0,
            va=dict(xs=58.0, jt=20.0, ht=4.5, o1=(-8.0, -3.0), o2=(-12.0, 0.5), i1=(0.0, 0.0), i2=(18.0, 0.5),
                    P=(28.0, 92.0), yj=0.56, h=8.0),
            gap_va_i=11.0, gap_i_na=12.0, na_w=66.0, na_y=34.0, na_tip=(10.0, 70.0),
            gap_na_da=12.0, da_w=70.0, gap_da_aa=10.0,
            hook_h=40.0, dot_r=6.5, dot_dx=10.0, ovl=4.0, ovr=4.0, va_gap=0.0)


def g_va(p):
    """The same leaf-loop va as the mark (loop hangs from the danda; counter is a V)."""
    q = dict(p['va']); q.update(b=p['b'], S=p['S'], ovl=0.0, ovr=0.0)
    g, info = va_cloop(**q)
    x0 = info['xL']
    g = tr(g, 1, -x0, 0)
    return g, q['xs'] + p['S'] - x0, info


def g_na(p, x):
    """Danda at the right; a level hairline leaves it at na_y and runs left; at its left end a leaf hangs down
    and ends in a point (the font anatomy: the left element hangs from the danda, not from the line)."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['na_w']
    xs = x + W - S
    y0 = p['na_y']                       # top of the level stroke
    tipx, tipy = p['na_tip']
    O0 = (x, y0)
    P = (x + tipx, tipy)
    lf = dict(LEAF); lf.update(dict(t0=h * 2.4, ko1=6.0, ko2=5.5, ki1=-1.0, ki2=-11.0))
    outer, inner = leaf_chord(O0, P, **lf)
    yb = y0 + h                          # bottom of the level stroke
    t = c_isect_line(*inner, (x - 50, yb), (x + 200, yb))
    (a0, a1, a2, Q), _ = csplit(*inner, t)
    _, Qr = csplit(*inner, t)
    # inner edge from Q down to P (the part below the level stroke)
    (q0, q1, q2, q3) = Qr
    _, c1o, c2o, _ = outer
    left = path_from([('M', *O0), ('L', xs + 1, y0), ('L', xs + 1, yb), ('L', *Q), ('C', *q1, *q2, *P),
                      ('C', *c2o, *c1o, *O0)])
    stem = rect(xs, 0, xs + S, H)
    return U(left, stem), xs, x + W


def g_i_matra(p, x, x_end):
    """Stem x..x+S, and a hook that grows out of the stem's top, arches right over the next letter and lands as a
    point on the line at x_end (thick where it leaves the stem, tapering: a leaf)."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    stem = rect(x, 0, x + S, H)
    top = -p['hook_h']
    span = x_end - x
    E = (x_end, 0.5)                                    # lands on the line
    o0 = (x, 0.0)
    oc1 = (x - 1.0, top * 0.70)
    oc2 = (x + span * 0.18, top * 1.02)
    om = (x + span * 0.42, top * 0.99)                  # crest (outer)
    oc3 = (x + span * 0.72, top * 0.96)
    oc4 = (x_end - span * 0.06, top * 0.45)
    i0 = (x + S, 0.0)
    ic1 = (x + S * 0.92, top * 0.42)
    ic2 = (x + span * 0.22, top * 0.82)
    im = (x + span * 0.44, top * 0.84)                  # crest (inner)
    ic3 = (x + span * 0.70, top * 0.80)
    ic4 = (x_end - span * 0.08, top * 0.36)
    hook = path_from([('M', *o0), ('C', *oc1, *oc2, *om), ('C', *oc3, *oc4, *E),
                      ('C', *ic4, *ic3, *im), ('C', *ic2, *ic1, *i0)])
    return U(stem, hook)


def g_dra(p, x, top=34.0, bot=92.0, stub_x=0.66, lo_cut=46.0):
    """द + rakaar. A danda-stub hangs from the line on the right and flows into the upper arm of a C-shaped bowl
    (thick on the left, hairline top and bottom, open on the right). Two strokes leave the foot of the bowl:
    द's tail (down-right) and the rakaar (down-left), crossing below the baseline."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['da_w']
    rx, ry = W * 0.46, (bot - top) / 2
    cx, cy = x + rx, (top + bot) / 2
    k = 0.60
    outer = ellipse(cx, cy, rx, ry, k)
    inner = ellipse(cx + S * 0.45, cy + 0.6, rx - S * 0.95, ry - h * 1.15, k)
    ring = D(outer, inner)
    sx1 = x + W * stub_x
    sx0 = sx1 - S * 0.92
    ring = D(ring, rect(sx1, -10, x + W + 60, cy))                        # upper arm ends flush with the stub
    R = 400
    pts = [(cx, cy)] + [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in (-1, 15, 30, lo_cut)]
    ring = D(ring, poly(pts))                                              # lower arm ends at ~lo_cut degrees
    stub = D(rect(sx0, 0, sx1, top + h * 1.15 + 4), inner)
    bowl = U(ring, stub)
    fx, fy = cx + 4.0, bot - h * 1.1
    tail = poly([(fx - 4.0, fy - 2.0), (fx + 2.0, fy - 2.0), (fx + 25.0, H + 18.0), (fx + 12.0, H + 18.0)])
    rak = poly([(fx - 3.0, fy - 1.0), (fx + 3.0, fy + 1.5), (fx - 21.0, H + 24.0), (fx - 33.0, H + 19.5)])
    # keep the legs out of the bowl's counter
    tail, rak = D(tail, inner), D(rak, inner)
    return U(bowl, tail, rak), x + W


def g_aa(p, x):
    return rect(x, 0, x + p['S'], p['H']), x + p['S']


def devanagari_word(**kw):
    p = dict(DEVA)
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(p.get(k), dict):
            q = dict(p[k]); q.update(v); p[k] = q
        else:
            p[k] = v
    H, S, b = p['H'], p['S'], p['b']
    va, xr, _ = g_va(p)
    x_i = xr + p['gap_va_i']
    x_na = x_i + S + p['gap_i_na']
    na, na_xs, na_r = g_na(p, x_na)
    matra = g_i_matra(p, x_i, na_xs + S * 0.5)
    dot = circle(na_xs + S * 0.5 + p['dot_dx'], -p['hook_h'] * 0.42, p['dot_r'])
    x_da = na_r + p['gap_na_da']
    dra, da_r = g_dra(p, x_da)
    x_aa = da_r + p['gap_da_aa']
    aa, aa_r = g_aa(p, x_aa)
    body = U(va, matra, na, dot, dra, aa)
    x0 = bbox(va)[0]
    line = rect(x0 - p['ovl'], 0, aa_r + p['ovr'], b)
    return U(body, line), (x0 - p['ovl'], aa_r + p['ovr'])
