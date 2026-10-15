"""Custom hanging caps for the Shirorekha wordmark. Each glyph: top at y=0 (bar top), baseline y=H.
Returns (path, width). Letters are drawn from x=0."""
import math
from geo import *

class Style:
    def __init__(self, H=100, b=11, S=15, h=3.6, Td=None, o=1.6, k=0.60, mono=False, foot=0.0):
        self.H, self.b, self.S, self.h, self.o, self.k = H, b, S, h, o, k
        self.Td = Td if Td is not None else S * 0.98  # perpendicular width of thick diagonals
        self.mono = mono
        self.foot = foot  # kalam: angled cut depth at stem feet (0 = flat)
        if mono:
            self.h = S; self.Td = S

def _foot(st, x0, x1, path):
    """Kalam cut: slice the foot of a vertical stem with a 45deg-ish chisel (rising to the left)."""
    if st.foot <= 0:
        return path
    H = st.H
    cut = poly([(x0 - 1, H - st.foot - (x1 - x0) * 0), (x0 - 1, H + 5), (x1 + 1, H + 5), (x1 + 1, H + 0.01)])
    # chisel: line from (x0, H - foot) to (x1, H)
    cut = poly([(x0 - 0.01, H - st.foot), (x1 + 0.01, H + 0.0), (x1 + 2, H + 6), (x0 - 2, H + 6)])
    return D(path, cut)

def glyph_V(st, W=None, gap_top=False):
    H, o = st.H, st.o
    W = W or H * 0.80
    vx = W / 2
    top = -2
    # outer edges
    L0, L1 = (0, 0), (vx, H + o)
    R0, R1 = (W, 0), (vx, H + o)
    # inner edges (offset inward by perpendicular widths)
    Li = offset(L0, L1, -st.Td)   # left arm thick; travel top->bottom, right-hand side is -x... compute sign below
    # choose sign so inner edge lies to the right of left outer edge
    a = offset(L0, L1, st.Td); bb = offset(L0, L1, -st.Td)
    Li = a if line_x(*a, 0) > 0 else bb
    a = offset(R0, R1, st.h); bb = offset(R0, R1, -st.h)
    Ri = a if line_x(*a, 0) < W else bb
    iv = isect(*Li, *Ri)
    pts = [(line_x(L0, L1, top), top), (line_x(*Li, top), top), iv, (line_x(*Ri, top), top), (line_x(R0, R1, top), top), (vx, H + o)]
    return poly(pts), W

def glyph_A(st, W=None, apex=None, cross=0.66):
    H = st.H
    W = W or H * 0.80
    apex = apex if apex is not None else st.b * 0.9   # outer width at bar bottom
    top = -2
    yb = st.b
    # outer edges pass through (W/2 - apex/2, yb) and (0, H) / (W, H)
    L0, L1 = (W / 2 - apex / 2, yb), (0, H)
    R0, R1 = (W / 2 + apex / 2, yb), (W, H)
    a = offset(L0, L1, st.h); bb = offset(L0, L1, -st.h)
    Li = a if line_x(*a, H) > 0 else bb       # thin left arm
    a = offset(R0, R1, st.Td); bb = offset(R0, R1, -st.Td)
    Ri = a if line_x(*a, H) < W else bb       # thick right arm
    iv = isect(*Li, *Ri)
    outer = poly([(line_x(L0, L1, top), top), (line_x(R0, R1, top), top), (W, H), (line_x(*Ri, H), H), iv, (line_x(*Li, H), H), (0, H)])
    # crossbar
    yc = H * cross
    hb = st.h if not st.mono else st.S
    cb = rect(line_x(*Li, yc) - 1, yc - hb / 2, line_x(*Ri, yc) + 1, yc + hb / 2)
    cb = I(cb, poly([(line_x(L0, L1, yc - hb), yc - hb), (line_x(R0, R1, yc - hb), yc - hb), (line_x(R0, R1, yc + hb), yc + hb), (line_x(L0, L1, yc + hb), yc + hb)]))
    p = U(outer, cb)
    p = I(p, rect(-5, -5, W + 5, H))
    return p, W

def glyph_N(st, W=None):
    H = st.H
    W = W or H * 0.78
    hs = st.h * 1.6 if not st.mono else st.S   # Didone N verticals: light
    top = -2
    left = rect(0, top, hs, H)
    right = rect(W - hs, top, W, H + st.o)
    # diagonal: horizontal width from perpendicular Td
    ang = math.atan2(W - hs, H)
    Th = st.Td / math.cos(ang) if not st.mono else st.S / math.cos(ang)
    diag = poly([(0, 0), (Th, 0), (W, H + st.o), (W - Th, H + st.o)])
    diag = U(diag, rect(0, top, Th, 0.01))
    p = U(_foot(st, 0, hs, left), right, diag)
    p = I(p, rect(-5, -5, W + 5, H + st.o))
    return p, W

def glyph_I(st):
    return _foot(st, 0, st.S, rect(0, -2, st.S, st.H)), st.S

def _bowl(st, x0, y0, y1, Wb, thick, hair_top, hair_bot, k=None):
    """D-type bowl: straight from x0 then half superellipse. Returns ring (outer - inner)."""
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
    return D(outer, inner), xc

def glyph_D(st, W=None):
    H = st.H
    W = W or H * 0.82
    stem = rect(0, -2, st.S, H)
    ring, _ = _bowl(st, st.S * 0.5, 0, H, W, st.S * 1.06, st.b, st.h)
    return U(_foot(st, 0, st.S, stem), ring), W

def glyph_R(st, W=None, ym=0.56, leg_x=None):
    H = st.H
    W = W or H * 0.78
    stem = rect(0, -2, st.S, H)
    y1 = H * ym
    bw = W * 0.86
    ring, xc = _bowl(st, st.S * 0.5, 0, y1, bw, st.S * 0.98, st.b, st.h)
    # leg: thick straight diagonal from bowl bottom to baseline right
    lx0 = leg_x if leg_x is not None else xc - st.S * 0.15
    top_y = y1 - st.h
    p0, p1 = (lx0, top_y), (W - st.Td * 0.5, H)
    leg = stroke(p0, p1, st.Td if not st.mono else st.S, top_y, H)
    leg = I(leg, rect(-5, top_y, W + 5, H))
    return U(_foot(st, 0, st.S, stem), ring, leg), W

def wordmark(st, word='VANINDRA', track=None, bar=True, overhang=None, gaps=(), widths=None, bar_b=None):
    """Assemble hanging caps on a shirorekha. track: dict of pair spacing (default uniform)."""
    widths = widths or {}
    sp = track if isinstance(track, (int, float)) else st.H * 0.10
    builders = {'V': glyph_V, 'A': glyph_A, 'N': glyph_N, 'I': glyph_I, 'D': glyph_D, 'R': glyph_R}
    x = 0
    parts = []
    spans = []
    prev = None
    # pair adjustments (diagonal pairs sit tighter)
    pair = {('V', 'A'): -0.55, ('A', 'N'): -0.05, ('R', 'A'): -0.45, ('N', 'I'): 0.0, ('I', 'N'): 0.0,
            ('N', 'D'): 0.0, ('D', 'R'): 0.05}
    for ch in word:
        if prev is not None:
            x += sp * (1 + pair.get((prev, ch), 0))
        if ch in widths:
            g, w = builders[ch](st, W=widths[ch]) if ch != 'I' else builders[ch](st)
        else:
            g, w = builders[ch](st)
        parts.append(tr(g, 1, x, 0))
        spans.append((ch, x, x + w))
        x += w
        prev = ch
    total = x
    ov = overhang if overhang is not None else st.H * 0.06
    bb = bar_b if bar_b is not None else st.b
    body = U(*parts)
    if bar:
        b = rect(-ov, 0, total + ov, bb)
        for g0, g1 in gaps:
            b = D(b, rect(g0, -1, g1, bb + 1))
        body = U(body, b)
    return body, total, spans
