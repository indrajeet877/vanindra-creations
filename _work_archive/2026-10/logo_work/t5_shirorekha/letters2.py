"""Hanging caps v2 — 'strokes grow from the headline': diagonals start hairline-thin where they leave the
shirorekha and gain weight as they descend (calligraphic wedge / blade); verticals are full-weight dandas.
Top of letters at y=0 (bar top), baseline y=H."""
import math
import pathops
from geo import *
from mono2 import qpt, qsplit, ctrl_left, line_isect_quad

class St:
    def __init__(self, H=100, b=8.6, S=14, h=3.6, t0=3.4, Tf=None, ns=None, o=1.6, k=0.60, bow=4.0):
        self.H, self.b, self.S, self.h, self.t0, self.o, self.k, self.bow = H, b, S, h, t0, o, k, bow
        self.Tf = Tf if Tf is not None else S * 1.18   # horizontal foot width of wedges
        self.ns = ns if ns is not None else S * 0.42   # N verticals

def _wedge(top_l, top_r, bot_l, bot_r, bow=0.0, bow_side='left'):
    """Quadrilateral stroke with optional bowed edge (quadratic) for a fuller belly.
    bow>0 pushes the chosen edge outward from the stroke's centre line."""
    p = pathops.Path()
    p.moveTo(*top_l)
    p.lineTo(*top_r)
    if bow and bow_side == 'right':
        c = ctrl_left(top_r, bot_r, -bow)
        p.quadTo(*c, *bot_r)
    else:
        p.lineTo(*bot_r)
    p.lineTo(*bot_l)
    if bow and bow_side == 'left':
        c = ctrl_left(bot_l, top_l, -bow)  # travelling upward; ctrl_left with negative pushes to the left side of travel
        p.quadTo(*c, *top_l)
    else:
        p.lineTo(*top_l)
    p.close()
    return U(p)

def g_V(st, W=72, swell=-15, bo=4):
    """Blade left arm (thin at the headline, swelling, pointed foot) + hairline right arm."""
    H, o, b = st.H, st.o, st.b
    vx = W / 2
    P = (vx, H + o)
    R0 = (W, 0.0)
    # right arm inner edge (hairline), offset towards the counter
    dx, dy = R0[0] - P[0], R0[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx > 0: nx, ny = -nx, -ny
    Pi, Ri = (P[0] + nx * st.h, P[1] + ny * st.h), (R0[0] + nx * st.h, R0[1] + ny * st.h)
    O0 = (0.0, 0.0)
    co = ctrl_left(O0, P, bo)
    I0 = (st.t0 + b * vx / (H + o), b)
    ci = ctrl_left(I0, P, swell)
    t = line_isect_quad(I0, ci, P, Pi, Ri)
    cq, Q = qsplit(I0, ci, P, t)
    p = pathops.Path()
    p.moveTo(*O0)
    p.quadTo(*co, *P)
    p.lineTo(*R0)
    p.lineTo(line_x(Pi, Ri, 0), 0)
    p.lineTo(*Q)
    p.quadTo(*cq, *I0)
    p.lineTo(I0[0], 0)
    p.close()
    return U(p), W

def g_A(st, W=74, apex=3.0, cross=0.66, swell=4.0):
    H, b = st.H, st.b
    a0, a1 = W / 2 - apex / 2, W / 2 + apex / 2
    # left hairline arm
    L0, L1 = (a0, 0.0), (0.0, H)
    left = poly([L0, (a0 + st.h * 1.08, 0.0), (st.h * 1.08, H), L1])
    # right wedge arm: thin at the headline, thick at the foot
    top_r = (a1, 0.0)
    top_l = (a1 - st.t0 * 1.1, 0.0)
    bot_r = (W, H)
    bot_l = (W - st.Tf, H)
    right = _wedge(top_l, top_r, bot_l, bot_r, bow=swell, bow_side='left')
    # crossbar between arms
    yc = H * cross
    inner_l = line_x((a0 + st.h * 1.08, 0.0), (st.h * 1.08, H), yc)
    inner_r = line_x(top_l, bot_l, yc)
    cb = rect(inner_l - 0.5, yc - st.h / 2, inner_r + 0.5, yc + st.h / 2)
    g = U(left, right, cb)
    return I(g, rect(-2, 0, W + 2, H)), W

def g_N(st, W=70):
    H = st.H
    ns = st.ns
    left = rect(0, 0, ns, H)
    right = rect(W - ns, 0, W, H + st.o)
    diag = poly([(0, 0), (ns + st.t0, 0), (W, H + st.o), (W - st.Tf * 1.04, H + st.o)])
    g = U(left, right, diag)
    return I(g, rect(-2, 0, W + 2, H + st.o)), W

def g_I(st):
    return rect(0, 0, st.S, st.H), st.S

def _bowl(st, x0, y0, y1, Wb, thick, hair_top, hair_bot, k=None):
    k = k or st.k
    ry = (y1 - y0) / 2
    cy = (y0 + y1) / 2
    rx = min(ry, Wb - x0)
    xc = Wb - rx
    outer = U(rect(x0, y0, xc + 0.01, y1), I(ellipse(xc, cy, rx, ry, k), rect(xc, y0 - 1, Wb + 1, y1 + 1)))
    iy0, iy1 = y0 + hair_top, y1 - hair_bot
    iry = (iy1 - iy0) / 2
    icy = (iy0 + iy1) / 2
    irx = rx - thick
    inner = U(rect(x0 - 1, iy0, xc + 0.01, iy1), I(ellipse(xc, icy, irx, iry, k), rect(xc, iy0 - 1, Wb + 1, iy1 + 1)))
    return D(outer, inner), xc, rx

def g_D(st, W=76):
    H = st.H
    stem = rect(0, 0, st.S, H)
    ring, _, _ = _bowl(st, st.S * 0.5, 0, H + st.o * 0.0, W, st.S * 1.10, st.b, st.h)
    return U(stem, ring), W

def g_R(st, W=72, ym=0.54, bw=0.84):
    H = st.H
    stem = rect(0, 0, st.S, H)
    y1 = H * ym
    ring, xc, rx = _bowl(st, st.S * 0.5, 0, y1, W * bw, st.S * 1.02, st.b, st.h)
    # leg wedge: hairline where it leaves the bowl, full weight at the foot
    top_y = y1 - st.h
    lx = xc - st.S * 0.1
    leg = _wedge((lx, top_y), (lx + st.t0 * 1.2, top_y), (W - st.Tf, H), (W, H))
    leg = I(leg, rect(0, top_y, W + 2, H))
    return U(stem, ring, leg), W

BUILD = {'V': g_V, 'A': g_A, 'N': g_N, 'I': g_I, 'D': g_D, 'R': g_R}

def wordmark(st, word='VANINDRA', space=None, ovl=None, ovr=None, bar=True, vgap=False, widths=None):
    """space: dict pair->gap in units (defaults below)."""
    widths = widths or {}
    sp = {('V', 'A'): -6.0, ('A', 'N'): 9.0, ('N', 'I'): 15.0, ('I', 'N'): 15.0, ('N', 'D'): 15.0,
          ('D', 'R'): 13.0, ('R', 'A'): -3.0}
    if space:
        sp.update(space)
    x = 0.0
    parts, spans = [], []
    prev = None
    for ch in word:
        if prev is not None:
            x += sp.get((prev, ch), 12.0)
        f = BUILD[ch]
        g, w = f(st, W=widths[ch]) if ch in widths and ch != 'I' else f(st)
        parts.append(tr(g, 1, x, 0))
        spans.append((ch, x, x + w))
        x += w
        prev = ch
    total = x
    ovl = st.H * 0.10 if ovl is None else ovl
    ovr = st.H * 0.10 if ovr is None else ovr
    body = U(*parts)
    if bar:
        bb = rect(-ovl, 0, total + ovr, st.b)
        if vgap:
            ch, a, c = spans[0]
            bb = D(bb, rect(a + vgap[0], -1, c - vgap[1], st.b + 1))
        body = U(body, bb)
    return body, total, spans

def g_V2(st, W=72, qh=0.70, foot=None):
    """Straight-edged V: left arm is a wedge (hairline at the headline, widening downward) ending in the point;
    right arm hairline. qh = height fraction where the wedge's inner edge meets the hairline's inner edge."""
    H, o, b = st.H, st.o, st.b
    vx = W / 2
    P = (vx, H + o)
    R0 = (W, 0.0)
    dx, dy = R0[0] - P[0], R0[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx > 0: nx, ny = -nx, -ny
    Pi, Ri = (P[0] + nx * st.h, P[1] + ny * st.h), (R0[0] + nx * st.h, R0[1] + ny * st.h)
    yq = H * qh
    Q = (line_x(Pi, Ri, yq), yq)
    I0 = (st.t0 + b * vx / (H + o), b)
    I0 = (I0[0], b)
    # extend inner edge line up to y=0
    x_top = line_x(I0, Q, 0)
    g = poly([(0, 0), (x_top, 0), Q, (line_x(Pi, Ri, 0), 0), R0, P])
    return g, W

def g_V3(st, W=72, swell=-20, bo=3.0, t0=None):
    """Curved-blade V for the wordmark: blade leaves the headline hairline-thin, swells, ends in the point."""
    H, o, b = st.H, st.o, st.b
    t0 = st.t0 if t0 is None else t0
    vx = W / 2
    P = (vx, H + o)
    R0 = (W, 0.0)
    dx, dy = R0[0] - P[0], R0[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx > 0: nx, ny = -nx, -ny
    Pi, Ri = (P[0] + nx * st.h, P[1] + ny * st.h), (R0[0] + nx * st.h, R0[1] + ny * st.h)
    O0 = (0.0, 0.0)
    co = ctrl_left(O0, P, bo)
    I0 = (t0 + b * vx / (H + o), b)
    ci = ctrl_left(I0, P, swell)
    t = line_isect_quad(I0, ci, P, Pi, Ri)
    cq, Q = qsplit(I0, ci, P, t)
    p = pathops.Path()
    p.moveTo(*O0)
    p.quadTo(*co, *P)
    p.lineTo(*R0)
    p.lineTo(line_x(Pi, Ri, 0), 0)
    p.lineTo(*Q)
    p.quadTo(*cq, *I0)
    p.lineTo(I0[0], 0)
    p.close()
    return U(p), W

def g_A3(st, W=74, apex=3.0, cross=0.66, belly=5.0):
    H, b = st.H, st.b
    a0, a1 = W / 2 - apex / 2, W / 2 + apex / 2
    left = poly([(a0, 0.0), (a0 + st.h * 1.08, 0.0), (st.h * 1.08, H), (0.0, H)])
    top_r, top_l = (a1, 0.0), (a1 - st.t0 * 1.1, 0.0)
    bot_r, bot_l = (W, H), (W - st.Tf, H)
    p = pathops.Path()
    p.moveTo(*top_l); p.lineTo(*top_r); p.lineTo(*bot_r); p.lineTo(*bot_l)
    c = ctrl_left(bot_l, top_l, belly)   # travelling up the inner edge; push towards the counter (left of travel = -x... )
    p.quadTo(*c, *top_l); p.close()
    right = U(p)
    yc = H * cross
    inner_l = line_x((a0 + st.h * 1.08, 0.0), (st.h * 1.08, H), yc)
    cb = rect(inner_l - 0.5, yc - st.h / 2, W * 0.75, yc + st.h / 2)
    cb = D(cb, D(rect(0, 0, W, H), U(right, poly([(a0, 0), (a1, 0), (W, H), (0, H)]))))
    g = U(left, right, I(cb, poly([(a0, 0), (a1, 0), (W, H), (0, H)])))
    return I(g, rect(-2, 0, W + 2, H)), W
