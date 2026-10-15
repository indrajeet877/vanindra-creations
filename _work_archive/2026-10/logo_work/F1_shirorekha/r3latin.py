"""VANINDRA capitals drawn in the leaf/danda system. Every vertical is a danda (stem), every diagonal is a leaf:
it leaves the headline hairline-thin and gains weight as it falls. Letter tops sit at y=0 (top of the line), baseline y=H.
`top` = thickness of a bowl's own top stroke (hidden under the line when bar=True)."""
from r3geo import *


class St:
    def __init__(self, H=100, b=8.8, S=13.0, h=5.0, ns=8.0, t0=3.8, Tf=14.0, o=1.6, k=0.60, lb=3.0,
                 top=None, bar=True, cross=0.64, trap=2.2, aw=1.0, vleaf=None):
        self.H, self.b, self.S, self.h, self.ns, self.t0, self.Tf, self.o, self.k, self.lb = H, b, S, h, ns, t0, Tf, o, k, lb
        self.bar = bar
        self.top = top if top is not None else (b if bar else h * 1.05)
        self.cross, self.trap, self.aw = cross, trap, aw
        self.vleaf = vleaf or dict(t0=t0, ko1=3.0, ko2=2.5, ki1=-2.0, ki2=-9.0)


def leaf_stroke(tl, tr_, bl, br, bow_outer, bow_inner, outer='left'):
    """Quadrilateral stroke from a narrow top (tl..tr_) to a wide bottom (bl..br). Its outer edge bows outward by
    bow_outer and the inner edge bows the same way by bow_inner (a leaf: curved, swelling)."""
    if outer == 'left':
        co = ctrl(tl, bl, bow_outer)           # +bulge = screen-left for a downward chord
        ci = ctrl(tr_, br, bow_inner)
        return path_from([('M', *tl), ('L', *tr_), ('Q', *ci, *br), ('L', *bl), ('Q', *co, *tl)])
    else:
        co = ctrl(tr_, br, -bow_outer)
        ci = ctrl(tl, bl, -bow_inner)
        return path_from([('M', *tl), ('L', *tr_), ('Q', *co, *br), ('L', *bl), ('Q', *ci, *tl)])


def hair_from(P, T, h, side):
    """Hairline from P to T (perpendicular width h), the given line is the OUTER edge; side='left' puts the body on
    the screen-left of travel P->T."""
    dx, dy = T[0] - P[0], T[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = (dy / L, -dx / L) if side == 'left' else (-dy / L, dx / L)
    return (P[0] + nx * h, P[1] + ny * h), (T[0] + nx * h, T[1] + ny * h)


def g_V(st, W=70, leaf=None):
    """Leaf left arm (thin at the line, swelling, pointed) + hairline right arm. Same leaf as the mark's bowl."""
    H, o = st.H, st.o
    P = (W / 2, H + o)
    lf = dict(LEAF); lf.update(st.vleaf if leaf is None else leaf)
    outer, inner = leaf_chord((0.0, 0.0), P, **lf)
    R0 = (W, 0.0)
    Pi, Ri = hair_from(P, R0, st.h, 'left')
    t = c_isect_line(*inner, Pi, Ri)
    (a0, a1, a2, Q), _ = csplit(*inner, t)
    O0, c1o, c2o, _ = outer
    shape = path_from([('M', *O0), ('C', *c1o, *c2o, *P), ('L', *R0), ('L', line_x(Pi, Ri, 0), 0.0), ('L', *Q),
                       ('C', *a2, *a1, *a0)])
    return I(shape, rect(-5, 0, W + 5, H + o + 1)), W


def g_A(st, W=72, apex=None):
    H = st.H
    apex = st.t0 + st.h * 0.6 if apex is None else apex
    a0, a1 = W / 2 - apex / 2, W / 2 + apex / 2
    hw = st.h * 1.06 * st.aw
    left = poly([(a0, 0.0), (a0 + hw, 0.0), (hw, H), (0.0, H)])
    right = leaf_stroke((a1 - st.t0, 0.0), (a1, 0.0), (W - st.Tf, H), (W, H), st.lb, st.lb * 0.35, outer='right')
    yc = H * st.cross
    il = line_x((a0 + hw, 0.0), (hw, H), yc)
    ir = line_x((a1 - st.t0, 0.0), (W - st.Tf, H), yc) + 1.0
    cb = rect(il - 0.5, yc - st.h * 0.5, ir, yc + st.h * 0.5)
    g = U(left, right, cb)
    return I(g, rect(-2, 0, W + 2, H)), W


def g_N(st, W=68):
    H, ns = st.H, st.ns
    left = rect(0, 0, ns, H)
    right = rect(W - ns, 0, W, H)
    tl, tr_ = (0.0, 0.0), (ns + st.t0, 0.0)
    bl, br = (W - st.Tf, H), (W, H)
    diag = poly([tl, tr_, br, bl])
    g = U(left, right, diag)
    if st.trap:
        # ink trap: deepen the acute right-hand counter where the diagonal meets the right stem
        y_meet = line_y(tr_, br, W - ns)   # where the diagonal's upper edge meets the stem's inner edge
        tw = st.trap
        g = D(g, poly([(W - ns - 0.02, y_meet - 18), (W - ns - 0.02, y_meet + tw * 2.2), (W - ns - tw, y_meet - 6)]))
    return I(g, rect(-2, 0, W + 2, H)), W


def g_I(st, W=None):
    return rect(0, 0, st.S, st.H), st.S


def _bowl(st, x0, y0, y1, Wb, thick, top, bot, k=None):
    k = k or st.k
    ry = (y1 - y0) / 2
    cy = (y0 + y1) / 2
    rx = min(ry, Wb - x0)
    xc = Wb - rx
    outer = U(rect(x0, y0, xc + 0.01, y1), I(ellipse(xc, cy, rx, ry, k), rect(xc, y0 - 1, Wb + 1, y1 + 1)))
    iy0, iy1 = y0 + top, y1 - bot
    iry = (iy1 - iy0) / 2
    icy = (iy0 + iy1) / 2
    irx = rx - thick
    inner = U(rect(x0 - 1, iy0, xc + 0.01, iy1), I(ellipse(xc, icy, irx, iry, k), rect(xc, iy0 - 1, Wb + 1, iy1 + 1)))
    return D(outer, inner), xc, rx


def g_D(st, W=74):
    H = st.H
    stem = rect(0, 0, st.S, H)
    ring, _, _ = _bowl(st, st.S * 0.5, 0, H, W, st.S * 1.08, st.top, st.h)
    return U(stem, ring), W


def g_R(st, W=70, ym=0.55, bw=0.84):
    H = st.H
    stem = rect(0, 0, st.S, H)
    y1 = H * ym
    ring, xc, rx = _bowl(st, st.S * 0.5, 0, y1, W * bw, st.S * 1.0, st.top, st.h)
    top_y = y1 - st.h
    lx = xc - st.S * 0.15
    leg = leaf_stroke((lx, top_y), (lx + st.t0 * 1.15, top_y), (W - st.Tf, H), (W, H), st.lb, st.lb * 0.35, outer='right')
    leg = I(leg, rect(0, top_y, W + 3, H))
    return U(stem, ring, leg), W


BUILD = {'V': g_V, 'A': g_A, 'N': g_N, 'I': g_I, 'D': g_D, 'R': g_R}
SPACE = {('V', 'A'): -7.0, ('A', 'N'): 9.0, ('N', 'I'): 20.0, ('I', 'N'): 20.0, ('N', 'D'): 17.0,
         ('D', 'R'): 14.0, ('R', 'A'): 4.0}


def wordmark(st, word='VANINDRA', space=None, ovl=4.0, ovr=4.0, bar=None, widths=None, bar_span=None):
    """Returns (path, total_width, spans). bar_span: None = full line, ('V',) = only over the V, 'none' = no line."""
    sp = dict(SPACE)
    if space:
        sp.update(space)
    widths = widths or {}
    x, prev = 0.0, None
    parts, spans = [], []
    for ch in word:
        if ch == ' ':
            x += sp.get(' ', 34.0)
            prev = None
            continue
        if prev is not None:
            x += sp.get((prev, ch), 12.0)
        f = BUILD[ch]
        g, w = f(st, W=widths[ch]) if ch in widths else f(st)
        parts.append(tr(g, 1, x, 0))
        spans.append((ch, x, x + w))
        x += w
        prev = ch
    total = x
    body = U(*parts)
    use_bar = st.bar if bar is None else bar
    if use_bar and bar_span != 'none':
        if bar_span is None:
            bb = rect(-ovl, 0, total + ovr, st.b)
        else:
            ch, a, c = spans[0]
            bb = rect(a - ovl, 0, c + ovr, st.b)
        body = U(body, bb)
    return body, total, spans


# ------------------------------------------------------------------ extra letters for CREATIONS (same system)
def _ring(st, x0, W, y0, y1, thick, top, bot, k=None, shift=0.0):
    k = k or st.k
    cx, cy = x0 + W / 2, (y0 + y1) / 2
    rx, ry = W / 2, (y1 - y0) / 2
    outer = ellipse(cx, cy, rx, ry, k)
    inner = ellipse(cx + shift, cy + (top - bot) / 2, rx - thick, ry - (top + bot) / 2, k)
    return outer, inner, (cx, cy, rx, ry)


def g_O(st, W=80):
    H = st.H
    o, i, _ = _ring(st, 0, W, -st.o * 0.6, H + st.o * 0.6, st.S * 1.0, st.top, st.h)
    return I(D(o, i), rect(-2, 0, W + 2, H + st.o)), W


def g_C(st, W=70, open_=0.60):
    H = st.H
    o, i, (cx, cy, rx, ry) = _ring(st, 0, W * 1.08, -st.o * 0.6, H + st.o * 0.6, st.S * 1.0, st.top, st.h)
    ring = D(o, i)
    xcut = cx + rx * open_
    ring = D(ring, rect(xcut, st.top + 0.01 + H * 0.12, W * 1.2, H - st.h - H * 0.10))
    ring = I(ring, rect(-2, 0, xcut, H + st.o))
    return ring, xcut


def g_E(st, W=56, mid=0.50, arm=0.86):
    H = st.H
    stem = rect(0, 0, st.S, H)
    top = rect(0, 0, W, max(st.top, st.h))
    mid_ = rect(0, H * mid - st.h / 2, W * arm, H * mid + st.h / 2)
    bot = rect(0, H - st.h, W, H)
    return U(stem, top, mid_, bot), W


def g_T(st, W=62, tbar=None):
    H = st.H
    tb = tbar if tbar is not None else max(st.top, st.h) * 1.0
    cx = W / 2
    return U(rect(0, 0, W, tb), rect(cx - st.S / 2, 0, cx + st.S / 2, H)), W


def g_S(st, W=60):
    """Two stacked superellipse rings (upper open lower-right, lower open upper-left), stress on the outer sides."""
    H = st.H
    ym = H * 0.52
    th = st.h * 1.05
    # upper ring: from 0 to ym+th/2
    o1, i1, (cx1, cy1, rx1, ry1) = _ring(st, W * 0.03, W * 0.94, 0, ym + th / 2, st.S * 0.92, st.top, th, shift=st.S * 0.10)
    up = D(o1, i1)
    up = D(up, rect(cx1, cy1 - 1, W + 5, ym + th))                        # remove lower-right quadrant
    up = D(up, rect(cx1 + rx1 * 0.62, st.top + H * 0.10, W + 5, cy1))     # open the upper-right (terminal)
    o2, i2, (cx2, cy2, rx2, ry2) = _ring(st, 0, W, ym - th / 2, H + st.o * 0.5, st.S * 0.98, th, st.h, shift=-st.S * 0.10)
    lo = D(o2, i2)
    lo = D(lo, rect(-5, ym - th, cx2, cy2 + 1))                            # remove upper-left quadrant
    lo = D(lo, rect(-5, cy2, cx2 - rx2 * 0.62, H - st.h - H * 0.08))      # open the lower-left (terminal)
    g = U(up, lo)
    return I(g, rect(-2, 0, W + 2, H + st.o)), W


BUILD.update({'O': g_O, 'C': g_C, 'E': g_E, 'T': g_T, 'S': g_S})


def g_B(st, W=62, ym=0.47):
    H = st.H
    stem = rect(0, 0, st.S, H)
    up, _, _ = _bowl(st, st.S * 0.5, 0, H * ym + st.h * 0.5, W * 0.90, st.S * 0.95, st.top, st.h)
    lo, _, _ = _bowl(st, st.S * 0.5, H * ym - st.h * 0.5, H, W, st.S * 1.0, st.h, st.h)
    return U(stem, up, lo), W


def g_Y(st, W=66, yj=0.54):
    """Leaf left arm and hairline right arm meet at yj; a danda drops from the join."""
    H = st.H
    cx = W / 2
    yjoin = H * yj
    left = leaf_stroke((0.0, 0.0), (st.t0, 0.0), (cx - st.S / 2, yjoin + 2), (cx + st.S / 2, yjoin + 2), st.lb, st.lb * 0.3, outer='left')
    hw = st.h * 1.05
    right = poly([(W - hw, 0.0), (W, 0.0), (cx + st.S / 2, yjoin), (cx + st.S / 2 - hw * 1.2, yjoin)])
    stem = rect(cx - st.S / 2, yjoin - 2, cx + st.S / 2, H)
    return I(U(left, right, stem), rect(-2, 0, W + 2, H)), W


BUILD.update({'B': g_B, 'Y': g_Y})
