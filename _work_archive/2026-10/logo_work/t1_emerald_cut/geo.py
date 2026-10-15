"""Geometry helpers for the Emerald Cut concept (straight-edge facet construction)."""
import math
import sys

sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
from vtype import *  # noqa
import pathops

EM = PALETTE['emerald']
IV = PALETTE['ivory']
GO = PALETTE['gold']
GL = PALETTE['gold_lt']
E2 = PALETTE['emerald_2']


def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return union(p)


def polyline(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    return p


def seg(a, b, ext=0.0):
    """Open segment a->b extended by ext at both ends."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    return polyline([(a[0] - ux * ext, a[1] - uy * ext), (b[0] + ux * ext, b[1] + uy * ext)])


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def isect(p1, p2, p3, p4):
    """Intersection of infinite lines p1p2 and p3p4."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        raise ValueError('parallel')
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den)


def signed_area(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return s / 2


def offset_poly(pts, d):
    """Miter-offset a simple polygon inward by d (positive = inward)."""
    n = len(pts)
    sgn = 1 if signed_area(pts) > 0 else -1  # y-down coords: positive area = clockwise visually
    lines = []
    for i in range(n):
        a = pts[i]; b = pts[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        # inward normal
        nx, ny = -dy / L * sgn, dx / L * sgn
        lines.append(((a[0] + nx * d, a[1] + ny * d), (b[0] + nx * d, b[1] + ny * d)))
    out = []
    for i in range(n):
        l0 = lines[i - 1]; l1 = lines[i]
        out.append(isect(l0[0], l0[1], l1[0], l1[1]))
    return out


def scale_about(pts, c, s):
    return [(c[0] + (x - c[0]) * s, c[1] + (y - c[1]) * s) for x, y in pts]


def octagon(W, H, c, x0=0, y0=0, cb=None):
    """Elongated octagon (emerald-cut girdle), clockwise from top-left chamfer start.
    c = top chamfer, cb = bottom chamfer (defaults to c)."""
    cb = c if cb is None else cb
    return [(x0 + c, y0), (x0 + W - c, y0), (x0 + W, y0 + c), (x0 + W, y0 + H - cb),
            (x0 + W - cb, y0 + H), (x0 + cb, y0 + H), (x0, y0 + H - cb), (x0, y0 + c)]


def cut(path, seams, width, cap='butt'):
    """Subtract stroked seam segments from a path."""
    if not seams:
        return path
    s = union(*[stroke_to_path(q, width, cap=cap) for q in seams])
    return difference(path, s)


def fit(path, box, pad=0.0, align='center'):
    """Scale+translate path to fit inside box=(x,y,w,h) preserving aspect."""
    x0, y0, x1, y1 = bounds(path)
    bw, bh = x1 - x0, y1 - y0
    bx, by, w, h = box
    s = min((w - 2 * pad) / bw, (h - 2 * pad) / bh)
    tx = bx + (w - bw * s) / 2 - x0 * s
    ty = by + (h - bh * s) / 2 - y0 * s
    return s, tx, ty


def place(path, s, tx, ty):
    return transform(path, s, 0, 0, s, tx, ty)


def pth(path, fill):
    return f'<path d="{to_d(path)}" fill="{fill}"/>'


def fmt(d, nd=2):
    import re
    return re.sub(r'-?\d+\.\d+', lambda m: (f'{float(m.group()):.{nd}f}').rstrip('0').rstrip('.'), d)


def pth_c(path, fill):
    return f'<path d="{fmt(to_d(path))}" fill="{fill}"/>'
