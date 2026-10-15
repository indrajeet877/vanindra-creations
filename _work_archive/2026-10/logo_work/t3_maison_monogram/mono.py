"""Geometry helpers for the Maison Monogram (t3). Math coords are y-UP; flip on output."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'toolkit')))
import pathops  # noqa: E402
import vtype  # noqa: E402
from vtype import union, difference, intersection, transform, to_d, bounds, stroke_to_path  # noqa: E402,F401

PAL = vtype.PALETTE
EMERALD, IVORY, GOLD, GOLD_LT, WHITE = PAL['emerald'], PAL['ivory'], PAL['gold'], PAL['gold_lt'], PAL['white']


# ---------- primitives ----------
def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return union(p)


def rect(x0, y0, x1, y1):
    return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def circle(cx, cy, r, n=4):
    k = 0.5522847498 * r
    p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return union(p)


def bracket(c, u, v, ru, rv=None):
    """Concave fillet in the corner c between directions u (along serif) and v (along stem)."""
    rv = ru if rv is None else rv
    a = (c[0] + u[0] * ru, c[1] + u[1] * ru)
    b = (c[0] + v[0] * rv, c[1] + v[1] * rv)
    p = pathops.Path()
    p.moveTo(*a)
    p.quadTo(c[0], c[1], *b)
    p.lineTo(*c)
    p.close()
    return union(p)


def unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def isect(p1, p2, p3, p4):
    """Intersection of infinite lines p1p2 and p3p4."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def x_at(p1, p2, y):
    return p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])


def dilate(p, g):
    if g <= 0:
        return p
    return union(p, stroke_to_path(p, 2 * g, join='miter'))


def erode(p, g):
    big = rect(-1e5, -1e5, 1e5, 1e5)
    inv = difference(big, p)
    return difference(p, dilate(inv, g))


def over(top, under, gap, region=None):
    """Return `under` with a gap cut around `top` (optionally only inside region)."""
    cut = dilate(top, gap)
    if region is not None:
        cut = intersection(cut, region)
    return difference(under, cut)


def rot(p, deg, cx=0, cy=0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return transform(p, c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy)


def move(p, dx, dy):
    return transform(p, 1, 0, 0, 1, dx, dy)


def scale(p, sx, sy=None, cx=0, cy=0):
    sy = sx if sy is None else sy
    return transform(p, sx, 0, 0, sy, cx - sx * cx, cy - sy * cy)


def mirror_x(p, cx=0):
    return transform(p, -1, 0, 0, 1, 2 * cx, 0)


# ---------- SVG output ----------
def to_svg_space(p):
    """Flip math (y-up) to SVG (y-down)."""
    return transform(p, 1, 0, 0, -1, 0, 0)


def place(p, box_x, box_y, box_w, box_h, align='center', optical_dy=0.0):
    """Fit a y-down path into a box, keeping aspect. Returns transformed path."""
    x0, y0, x1, y1 = bounds(p)
    w, h = x1 - x0, y1 - y0
    s = min(box_w / w, box_h / h)
    tx = box_x + (box_w - w * s) / 2 - x0 * s
    ty = box_y + (box_h - h * s) / 2 - y0 * s + optical_dy * box_h
    return transform(p, s, 0, 0, s, tx, ty), s


def path_el(p, fill):
    return f'<path fill="{fill}" d="{to_d(p)}"/>'


def write_svg(fn, w, h, body, bg=None, title='VanIndra Creations'):
    with open(fn, 'w') as f:
        f.write(vtype.svg_doc(w, h, body, bg=bg, title=title))
