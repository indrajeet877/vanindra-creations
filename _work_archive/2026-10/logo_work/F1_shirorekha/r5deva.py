"""वनिंद्रा, F1 polish (TO BE VERIFIED BY THE TEAM / a native type reader before any public use).
Judges' notes and what changed from r4deva:
- every outline is now true cubic Beziers (fitted pen, r5pen), no sampled polylines;
- व is the new mark geometry (lighter loop, danda heaviest);
- न: the left element is a drop that grows out of the end of the joining stroke and falls below it, with its tail
  pointing down-right (as in Martel / Noto / Tiro), not a detached teardrop tucked under the bar;
- ि: the hook keeps a real width all the way to the line and lands over the centre of न's danda;
- द्र: the rakaar is a short caret hung from the end of द's tail (apex at the tail, legs about 10 units below the
  baseline, left leg a small leaf, right leg a hairline). It no longer crosses the bowl into an X / λ and is no longer
  the heaviest, lowest shape in the word.
Glyph order on the line: व | ि | न | ं | द्र | ा"""
from r3geo import *
from r4mark import va_vloop
from r4latin import _hseg, _cubic_samples, _u
from r5pen import vstroke_pts
from r5fit import fit_polyline

DEVA5 = dict(H=100, b=8.8, S=13.0, h=5.0,
             va=dict(b=8.8, S=13.0, jt=20.0, ht=5.0, K=(0.5, 43.0), ks=(40.0, 17.0), Ki=(11.0, 46.5), kis=(35.0, 15.0),
                     karm=(15.0, 0.8), kiarm=(15.0, -1.0), P=(30.0, 96.0), yj=0.54, h=8.5),
             gap_va_i=11.0, gap_i_na=12.0, na_w=60.0, na_y=40.0, na_bar=6.0,
             gap_na_da=12.0, da_w=58.0, gap_da_aa=10.0,
             hook_h=40.0, hook_w=5.5, dot_r=6.3, dot_dx=12.0, dot_y=26.0, ovl=4.0, ovr=4.0,
             rak_l=(-15.0, 11.0), rak_r=(8.0, 9.0))


def g_va(p):
    q = dict(p['va']); q.update(ovl=0.0, ovr=0.0)
    g, info = va_vloop(**q)
    x0 = info['xL']
    g = tr(g, 1, -x0, 0)
    return g, q.get('xs', 58.0) + q['S'] - x0, info


def g_na(p, x):
    """Danda at the right; the joining stroke leaves it at y0 and runs left; at its left end it turns down into a
    drop whose tail points down-right."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['na_w']
    xs = x + W - S
    y0 = p['na_y']
    bh = p['na_bar']
    # the drop: leaves the end of the joining stroke through a narrow neck and falls into a weighted foot whose
    # tail turns right (leaf logic: light where it leaves the stroke, full weight at the foot)
    x1 = x + 14.0
    if p.get('na_style', 'foot') == 'crescent':
        drop = path_from([('M', x1 + 4.0, y0),
                          ('C', x + 6.0, y0, x - 0.5, y0 + 3.0, x - 0.5, y0 + 12.0),
                          ('C', x - 0.5, y0 + 22.0, x + 5.0, y0 + 30.0, x + 15.0, y0 + 33.0),
                          ('C', x + 12.0, y0 + 27.0, x + 11.0, y0 + 20.0, x + 13.0, y0 + bh + 3.0),
                          ('C', x + 13.6, y0 + bh + 0.8, x1 - 1.0, y0 + bh, x1, y0 + bh),
                          ('L', x1 + 4.0, y0 + bh)])
    else:
        drop = path_from([('M', x1 + 4.0, y0),
                          ('C', x + 6.0, y0, x + 1.5, y0 + 3.0, x + 1.5, y0 + 11.0),
                          ('C', x + 1.5, y0 + 18.0, x - 1.5, y0 + 22.0, x - 1.5, y0 + 28.0),
                          ('C', x - 1.5, y0 + 33.5, x + 4.0, y0 + 36.5, x + 10.0, y0 + 35.0),
                          ('C', x + 13.0, y0 + 34.2, x + 15.0, y0 + 32.5, x + 16.0, y0 + 30.5),
                          ('C', x + 12.0, y0 + 30.0, x + 8.5, y0 + 25.0, x + 8.5, y0 + 17.0),
                          ('C', x + 8.5, y0 + bh + 2.5, x + 10.0, y0 + bh, x1, y0 + bh),
                          ('L', x1 + 4.0, y0 + bh)])
    bar = rect(x1, y0, xs + 1, y0 + bh)
    stem = rect(xs, 0, xs + S, H)
    return U(drop, bar, stem), xs, x + W


def g_i_matra(p, x, x_end):
    """Stem, and a hook that grows out of the stem's top, arches right and lands on the line over the centre of the
    next letter's danda, keeping a real width (hook_w) where it lands."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    stem = rect(x, 0, x + S, H)
    top = -p['hook_h']
    span = x_end - x
    hw = p['hook_w'] / 2
    Eo, Ei = (x_end + hw, 0.5), (x_end - hw, 0.5)
    o0 = (x, 0.0)
    oc1 = (x - 1.0, top * 0.70)
    oc2 = (x + span * 0.18, top * 1.02)
    om = (x + span * 0.42, top * 0.99)
    oc3 = (x + span * 0.72, top * 0.96)
    oc4 = (x_end + hw - span * 0.04, top * 0.48)
    i0 = (x + S, 0.0)
    ic1 = (x + S * 0.92, top * 0.42)
    ic2 = (x + span * 0.22, top * 0.82)
    im = (x + span * 0.44, top * 0.83)
    ic3 = (x + span * 0.66, top * 0.80)
    ic4 = (x_end - hw - span * 0.06, top * 0.42)
    hook = path_from([('M', *o0), ('C', *oc1, *oc2, *om), ('C', *oc3, *oc4, *Eo), ('L', *Ei),
                      ('C', *ic4, *ic3, *im), ('C', *ic2, *ic1, *i0)])
    return U(stem, hook)


def leaf_leg(A, B, wa, wb):
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    return poly([(A[0] + nx * wa / 2, A[1] + ny * wa / 2), (B[0] + nx * wb / 2, B[1] + ny * wb / 2),
                 (B[0] - nx * wb / 2, B[1] - ny * wb / 2), (A[0] - nx * wa / 2, A[1] - ny * wa / 2)])


def g_dra(p, x, top=36.0, bot=92.0):
    """द with the contrast pen: leaves the line as a danda-weight stub, turns left into a hairline top arm (entry
    hook), runs down the heavy left side, round the hairline bottom and out into a short tail at the lower right.
    The rakaar is a small caret hung from the end of that tail."""
    H, S, b, h = p['H'], p['S'], p['b'], p['h']
    W = p['da_w']
    xs = x + W * 0.68
    xl = x + S * 0.55
    yt = top + h / 2
    yb = bot - h / 2
    P0 = (xs, 0.0)
    P1 = (xs, top - 14.0)
    P2 = (x + W * 0.40, yt)
    P3 = (xl, (yt + yb) / 2 + 2.0)
    P4 = (x + W * 0.46, yb)
    P5 = (x + W * 0.78, bot - 9.0)                      # tail end
    segs = [
        _hseg(P0, (0, 1), P1, (0, 1), 4.0, 4.0),
        _hseg(P1, (0, 1), P2, (-1, 0), 9.0, 11.0),
        _hseg(P2, (-1, 0), P3, (0, 1), 13.0, 13.0),
        _hseg(P3, (0, 1), P4, (1, 0), 14.0, 12.0),
        _hseg(P4, (1, 0), P5, _u(1.0, -0.55), 10.0, 6.0),
    ]
    pts = []
    for i, sg in enumerate(segs):
        sm = [q for q, _ in _cubic_samples(sg, 50)]
        pts += sm if i == 0 else sm[1:]
    da = vstroke_pts(pts, S * 1.05, h, smooth=10, taper=(None, h * 1.25), tz=0.06)
    da = U(da, rect(xs - S * 0.52, 0, xs + S * 0.52, top - 16.0))
    # rakaar: apex at the tail end, two short legs
    A = (P5[0] - 1.0, P5[1] + 1.5)
    lx, ly = p['rak_l']
    rx, ry = p['rak_r']
    left_leg = leaf_leg(A, (A[0] + lx, H + ly), h * 1.0, S * 0.62)
    right_leg = leaf_leg((A[0] + 0.8, A[1]), (A[0] + rx, H + ry), h * 1.0, h * 1.2)
    knot = circle(A[0] + 0.3, A[1] + 0.6, h * 0.62)
    return U(da, left_leg, right_leg, knot), x + W


def g_aa(p, x):
    return rect(x, 0, x + p['S'], p['H']), x + p['S']


def devanagari_word(**kw):
    p = dict(DEVA5)
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
    dot = circle(na_xs + S + p['dot_dx'], -p['dot_y'], p['dot_r'])
    x_da = na_r + p['gap_na_da']
    dra, da_r = g_dra(p, x_da)
    x_aa = da_r + p['gap_da_aa']
    aa, aa_r = g_aa(p, x_aa)
    body = U(va, matra, na, dot, dra, aa)
    x0 = bbox(va)[0]
    line = rect(x0 - p['ovl'], 0, aa_r + p['ovr'], b)
    return U(body, line), (x0 - p['ovl'], aa_r + p['ovr'])
