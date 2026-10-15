"""Geometry helpers for the Shirorekha concept (t5). All coordinates SVG y-down."""
import math, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype as V
import pathops

K = 0.5522847498  # circle kappa

def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return V.union(p)

def rect(x0, y0, x1, y1):
    return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

def ellipse(cx, cy, rx, ry, k=K):
    """Superellipse-ish: k=0.5523 circle; larger k squarer."""
    p = pathops.Path()
    p.moveTo(cx + rx, cy)
    p.cubicTo(cx + rx, cy + ry * k, cx + rx * k, cy + ry, cx, cy + ry)
    p.cubicTo(cx - rx * k, cy + ry, cx - rx, cy + ry * k, cx - rx, cy)
    p.cubicTo(cx - rx, cy - ry * k, cx - rx * k, cy - ry, cx, cy - ry)
    p.cubicTo(cx + rx * k, cy - ry, cx + rx, cy - ry * k, cx + rx, cy)
    p.close()
    return V.union(p)

def circle(cx, cy, r):
    return ellipse(cx, cy, r, r)

def line_x(p0, p1, y):
    (x0, y0), (x1, y1) = p0, p1
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)

def isect(a0, a1, b0, b1):
    x1, y1 = a0; x2, y2 = a1; x3, y3 = b0; x4, y4 = b1
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

def offset(p0, p1, d):
    """Offset the line p0->p1 by d to its right-hand side (in y-down coords: right of travel direction)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    return (p0[0] + nx * d, p0[1] + ny * d), (p1[0] + nx * d, p1[1] + ny * d)

def stroke(p0, p1, w, y0=None, y1=None, align='center'):
    """Straight stroke along centreline (or edge) p0->p1, perpendicular width w, cut by horizontals y0,y1.
    align: 'center' | 'left' (given line is the left edge seen going top->bottom) | 'right'."""
    if align == 'center':
        a = offset(p0, p1, -w / 2); b = offset(p0, p1, w / 2)
    elif align == 'right':
        a = offset(p0, p1, 0); b = offset(p0, p1, w)
    else:
        a = offset(p0, p1, -w); b = offset(p0, p1, 0)
    ya = p0[1] if y0 is None else y0
    yb = p1[1] if y1 is None else y1
    pts = [(line_x(*a, ya), ya), (line_x(*b, ya), ya), (line_x(*b, yb), yb), (line_x(*a, yb), yb)]
    return poly(pts)

def hstroke(x0, x1, y, w):
    return rect(x0, y - w / 2, x1, y + w / 2)

def U(*ps):
    return V.union(*ps)

def D(a, b):
    return V.difference(a, b)

def I(a, b):
    return V.intersection(a, b)

def d(path):
    return V.to_d(path)

def tr(path, s=1.0, dx=0.0, dy=0.0, sy=None):
    return V.transform(path, s, 0, 0, s if sy is None else sy, dx, dy)

def bbox(path):
    return V.bounds(path)

def text(txt, **kw):
    return V.text_path(txt, **kw)

PAL = V.PALETTE
