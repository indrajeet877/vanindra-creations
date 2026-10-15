"""वनिंद्रा drawn in the leaf/danda system - final-final pass (TO BE VERIFIED BY THE TEAM / a native type reader).
Changes from r3deva, after the judges' native-reading notes:
- व is the new mark geometry (V silhouette, loop hung from the danda, never from the line).
- न: the left tick is a short teardrop (about a quarter of the letter height), not a long leaf drifting toward त.
- ि: the hook lands on the न's danda; the anusvara sits above that danda (over न), not past it.
- द्र: द is drawn with the contrast pen as one stroke: it leaves the line as a danda-weight stub, turns left into a
  hairline top arm (the entry hook), runs down the heavy left side, round the hairline bottom, and turns up into a
  terminal at the lower right. The rakaar is a caret hung from that terminal: a leaf leg down-left, a hairline down-right.
Glyph order on the line: व | ि | न | ं | द्र | ा"""
from r3geo import *
from r4mark import va_vloop
from r4latin import vstroke_pts, _hseg, _cubic_samples, _u

DEVA = dict(H=100, b=8.8, S=13.0, h=5.0,
            va=dict(b=8.8, S=13.0, jt=20.0, ht=5.0, K=(2.0, 40.0), ks=(32.0, 13.0), P=(31.0, 95.0), Ki=(15.5, 43.0),
                    kis=(25.0, 10.0), yj=0.54, h=8.5),
            gap_va_i=11.0, gap_i_na=12.0, na_w=62.0, na_y=38.0, na_tip=(9.0, 64.0),
            gap_na_da=13.0, da_w=60.0, gap_da_aa=9.0,
            hook_h=40.0, hook_end=0.10, dot_r=6.3, dot_dx=10.0, dot_y=27.0, ovl=4.0, ovr=4.0)


def g_va(p):
    q = dict(p['va']); q.update(ovl=0.0, ovr=0.0)
    g, info = va_vloop(**q)
    x0 = info['xL']
    g = tr(g, 1, -x0, 0)
    return g, q.get('xs', 58.0) + q['S'] - x0, info


def g_na(p, x):
    """Danda at the right; a level hairline leaves it and runs left; at its left end a short teardrop hangs."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['na_w']
    xs = x + W - S
    y0 = p['na_y']
    tipx, tipy = p['na_tip']
    O0 = (x, y0)
    P = (x + tipx, tipy)
    lf = dict(LEAF); lf.update(dict(t0=h * 2.6, ko1=7.0, ko2=6.0, ki1=1.0, ki2=-9.0, uo1=0.30, uo2=0.75))
    outer, inner = leaf_chord(O0, P, **lf)
    yb = y0 + h
    t = c_isect_line(*inner, (x - 50, yb), (x + 200, yb))
    _, Qr = csplit(*inner, t)
    Q = Qr[0]
    (q0, q1, q2, q3) = Qr
    _, c1o, c2o, _ = outer
    left = path_from([('M', *O0), ('L', xs + 1, y0), ('L', xs + 1, yb), ('L', *Q), ('C', *q1, *q2, *P),
                      ('C', *c2o, *c1o, *O0)])
    stem = rect(xs, 0, xs + S, H)
    return U(left, stem), xs, x + W


def g_i_matra(p, x, x_end):
    """Stem, and a hook that grows out of the stem's top, arches right over the next letter and lands on the line at
    x_end, over that letter's danda (thick where it leaves the stem, tapering: a leaf)."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    stem = rect(x, 0, x + S, H)
    top = -p['hook_h']
    span = x_end - x
    E = (x_end, 0.5)
    o0 = (x, 0.0)
    oc1 = (x - 1.0, top * 0.70)
    oc2 = (x + span * 0.18, top * 1.02)
    om = (x + span * 0.42, top * 0.99)
    oc3 = (x + span * 0.70, top * 0.96)
    oc4 = (x_end - span * 0.10, top * 0.50)
    i0 = (x + S, 0.0)
    ic1 = (x + S * 0.92, top * 0.42)
    ic2 = (x + span * 0.22, top * 0.82)
    im = (x + span * 0.44, top * 0.84)
    ic3 = (x + span * 0.68, top * 0.80)
    ic4 = (x_end - span * 0.12, top * 0.40)
    hook = path_from([('M', *o0), ('C', *oc1, *oc2, *om), ('C', *oc3, *oc4, *E),
                      ('C', *ic4, *ic3, *im), ('C', *ic2, *ic1, *i0)])
    return U(stem, hook)


def g_dra(p, x, top=36.0, bot=94.0):
    """द + rakaar, drawn with the contrast pen (see module docstring)."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['da_w']
    xs = x + W * 0.66                       # stub centre
    xl = x + S * 0.55                       # left side centre
    yt = top + h / 2                        # top arm centre
    yb = bot - h / 2
    P0 = (xs, 0.0)
    P1 = (xs, top - 14.0)
    P2 = (x + W * 0.40, yt)
    P3 = (xl, (yt + yb) / 2 + 2.0)
    P4 = (x + W * 0.46, yb)
    P5 = (x + W * 0.80, bot - 20.0)
    segs = [
        _hseg(P0, (0, 1), P1, (0, 1), 4.0, 4.0),
        _hseg(P1, (0, 1), P2, (-1, 0), 9.0, 11.0),
        _hseg(P2, (-1, 0), P3, (0, 1), 13.0, 13.0),
        _hseg(P3, (0, 1), P4, (1, 0), 14.0, 13.0),
        _hseg(P4, (1, 0), P5, _u(0.55, -1.0), 12.0, 8.0),
    ]
    pts = []
    for i, sg in enumerate(segs):
        sm = [q for q, _ in _cubic_samples(sg, 50)]
        pts += sm if i == 0 else sm[1:]
    da = vstroke_pts(pts, S * 1.05, h, smooth=10)
    da = U(da, rect(xs - S * 0.52, 0, xs + S * 0.52, top - 16.0))     # the stub keeps full danda weight to the line
    # rakaar: a caret hung from the terminal (apex just under it)
    ax, ay = P5[0] - 2.0, bot - 6.0
    left_leg = leaf_stroke_simple((ax, ay), (ax - 27.0, H + 23.0), h * 0.9, S * 0.80)
    right_leg = leaf_stroke_simple((ax + 1.0, ay - 2.0), (ax + 17.0, H + 18.0), h * 0.9, h * 1.4)
    return U(da, left_leg, right_leg), x + W


def leaf_stroke_simple(A, B, wa, wb):
    """Straight stroke from A (width wa) to B (width wb), butt ends perpendicular to the stroke."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    return poly([(A[0] + nx * wa / 2, A[1] + ny * wa / 2), (B[0] + nx * wb / 2, B[1] + ny * wb / 2),
                 (B[0] - nx * wb / 2, B[1] - ny * wb / 2), (A[0] - nx * wa / 2, A[1] - ny * wa / 2)])


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
    matra = g_i_matra(p, x_i, na_xs + S * p['hook_end'])
    dot = circle(na_xs + p['dot_dx'], -p['dot_y'], p['dot_r'])
    x_da = na_r + p['gap_na_da']
    dra, da_r = g_dra(p, x_da)
    x_aa = da_r + p['gap_da_aa']
    aa, aa_r = g_aa(p, x_aa)
    body = U(va, matra, na, dot, dra, aa)
    x0 = bbox(va)[0]
    line = rect(x0 - p['ovl'], 0, aa_r + p['ovr'], b)
    return U(body, line), (x0 - p['ovl'], aa_r + p['ovr'])
