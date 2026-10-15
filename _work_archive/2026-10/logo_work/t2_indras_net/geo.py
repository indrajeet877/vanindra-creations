"""Geometry helpers for the Indra's Net concept: rhombic lattice, threads, jewels.

Lattice convention (SVG y-down):
    P(u, v) = O + u*e1 + v*e2,   e1 = (s*h, h)  (down-right),  e2 = (-s*h, h)  (down-left)
Left arm of the V runs along e1 (fixed v), right arm along e2 (fixed u).
"""
import math
import os
import sys

SCRATCH = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
sys.path.insert(0, os.path.join(SCRATCH, 'logo2', 'toolkit'))
import pathops  # noqa: E402
from vtype import (union, difference, intersection, xor, to_d, transform, bounds,  # noqa: E402,F401
                   svg_doc, text_path, glyph_paths, PALETTE, stroke_to_path)


def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def norm(a):
    L = math.hypot(*a)
    return (a[0] / L, a[1] / L)


def perp(a):
    return (-a[1], a[0])


def seg(p0, p1, w):
    """Butt-capped thick segment as an exact polygon."""
    d = norm(sub(p1, p0))
    n = mul(perp(d), w / 2)
    return poly([add(p0, n), add(p1, n), sub(p1, n), sub(p0, n)])


def halfplane(p, d, big=1e5):
    """Half-plane to the RIGHT of the directed line through p with direction d (screen coords: right of travel)."""
    d = norm(d)
    n = (-d[1], d[0])  # in y-down screen coords this points to the right of travel
    a = sub(p, mul(d, big))
    b = add(p, mul(d, big))
    return poly([a, b, add(b, mul(n, big)), add(a, mul(n, big))])


def line_intersect(p, d, q, e):
    """Intersection of p + t d and q + s e."""
    den = d[0] * e[1] - d[1] * e[0]
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return add(p, mul(d, t))


class Lattice:
    def __init__(self, O, h, s):
        self.O, self.h, self.s = O, h, s
        self.e1 = (s * h, h)
        self.e2 = (-s * h, h)

    def P(self, u, v):
        return (self.O[0] + (u - v) * self.s * self.h, self.O[1] + (u + v) * self.h)

    def cell(self, i, j, inset=0.0):
        """Rhombic cell spanning u in [i,i+1], v in [j,j+1]; inset = perpendicular inset distance."""
        pts = [self.P(i, j), self.P(i + 1, j), self.P(i + 1, j + 1), self.P(i, j + 1)]
        if inset <= 0:
            return poly(pts)
        # inset each edge by moving along the in-pointing normal; compute via offset of edge lines
        c = self.P(i + .5, j + .5)
        lines = []
        for k in range(4):
            a, b = pts[k], pts[(k + 1) % 4]
            d = norm(sub(b, a))
            n = perp(d)
            # make n point inward
            if (c[0] - a[0]) * n[0] + (c[1] - a[1]) * n[1] < 0:
                n = mul(n, -1)
            lines.append((add(a, mul(n, inset)), d))
        out = []
        for k in range(4):
            p, d = lines[k - 1]
            q, e = lines[k]
            out.append(line_intersect(p, d, q, e))
        return poly(out)

    def jewel(self, u, v, r):
        """Lozenge centred on node (u,v), similar to a cell, vertical half-diagonal r."""
        c = self.P(u, v)
        rx = r * self.s
        return poly([(c[0], c[1] - r), (c[0] + rx, c[1]), (c[0], c[1] + r), (c[0] - rx, c[1])])

    def thread_v(self, v, u0, u1, w):
        """Left-arm thread (fixed v) from u0 to u1."""
        return seg(self.P(u0, v), self.P(u1, v), w)

    def thread_u(self, u, v0, v1, w):
        return seg(self.P(u, v0), self.P(u, v1), w)


def write_svg(path, w, h, body, bg=None):
    with open(path, 'w') as f:
        f.write(svg_doc(w, h, body, bg))


def fill(p, color):
    return f'<path d="{to_d(p)}" fill="{color}"/>'


def fit(p, box, pad_frac=0.0, cx=None, cy=None, target=None):
    """Scale+translate path p into a square box of size `box`, so its larger side equals target (default box*(1-2pad))."""
    x0, y0, x1, y1 = bounds(p)
    w, hh = x1 - x0, y1 - y0
    t = target if target else box * (1 - 2 * pad_frac)
    k = t / max(w, hh)
    cx = box / 2 if cx is None else cx
    cy = box / 2 if cy is None else cy
    return transform(p, k, 0, 0, k, cx - (x0 + w / 2) * k, cy - (y0 + hh / 2) * k), k
