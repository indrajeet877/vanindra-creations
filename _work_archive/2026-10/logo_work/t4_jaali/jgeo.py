"""Precise geometry helpers for the Jaali concept (SVG y-down coordinates)."""
import math
import sys

sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import pathops  # noqa: E402
import vtype as vt  # noqa: E402

D2R = math.pi / 180.0
EMERALD, IVORY, GOLD, GOLD_LT, WHITE = '#0B2A20', '#F6F1E7', '#A8843A', '#D2B26A', '#FFFFFF'


def P(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def polar(cx, cy, r, a_deg):
    """a_deg measured counter-clockwise from +x with y UP (math), returned in SVG y-down."""
    a = a_deg * D2R
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def star_pts(cx, cy, R, n=8, m=3, a0=90.0, r=None):
    """Regular star polygon {n/m} outline (2n points). a0 = direction of the first point."""
    if r is None:
        r = R * math.cos(math.pi * m / n) / math.cos(math.pi * (m - 1) / n)
    pts = []
    for k in range(n):
        pts.append(polar(cx, cy, R, a0 + k * 360.0 / n))
        pts.append(polar(cx, cy, r, a0 + (k + 0.5) * 360.0 / n))
    return pts


def ngon_pts(cx, cy, R, n, a0=90.0):
    return [polar(cx, cy, R, a0 + k * 360.0 / n) for k in range(n)]


def signed_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def _isect(p1, d1, p2, d2):
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return (p2[0], p2[1])
    t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
    return (p1[0] + d1[0] * t, p1[1] + d1[1] * t)


def offset(pts, d):
    """Exact parallel offset of a simple polygon. d>0 shrinks (inset), d<0 grows."""
    n = len(pts)
    sgn = 1.0 if signed_area(pts) > 0 else -1.0
    lines = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        # inward normal for positive (y-down => clockwise visually) orientation
        nx, ny = -dy / L * sgn, dx / L * sgn
        lines.append(((a[0] + nx * d, a[1] + ny * d), (dx, dy)))
    out = []
    for i in range(n):
        p1, d1 = lines[i - 1]
        p2, d2 = lines[i]
        out.append(_isect(p1, d1, p2, d2))
    return out


def line_isect(a1, a2, b1, b2):
    return _isect(a1, (a2[0] - a1[0], a2[1] - a1[1]), b1, (b2[0] - b1[0], b2[1] - b1[1]))


def union(*ps):
    return vt.union(*ps)


def diff(a, b):
    return vt.difference(a, b)


def inter(a, b):
    return vt.intersection(a, b)


def bbox(path):
    return vt.bounds(path)


def fit(path, box_w, box_h, cx, cy, optical_dy=0.0):
    """Scale path uniformly to fit inside box (w,h) centred at (cx, cy)."""
    x0, y0, x1, y1 = vt.bounds(path)
    s = min(box_w / (x1 - x0), box_h / (y1 - y0))
    tx = cx - (x0 + x1) / 2 * s
    ty = cy - (y0 + y1) / 2 * s + optical_dy
    return vt.transform(path, s, 0, 0, s, tx, ty), s


def scale_to_height(path, h, x, y):
    x0, y0, x1, y1 = vt.bounds(path)
    s = h / (y1 - y0)
    return vt.transform(path, s, 0, 0, s, x - x0 * s, y - y0 * s), s


def d(path):
    return vt.to_d(path)


def svg(w, h, items, bg=None, title='VanIndra Creations'):
    body = ''.join(f'<path fill="{c}" fill-rule="nonzero" d="{vt.to_d(p)}"/>' for p, c in items)
    return vt.svg_doc(w, h, body, bg=bg, title=title)


def merge(paths):
    """Fast union: concatenate all contours (normalised winding) and simplify once."""
    out = pathops.Path()
    for p in paths:
        q = pathops.Path(p)
        q.simplify(fix_winding=True, clockwise=True)
        out.addPath(q)
    out.simplify(fix_winding=True)
    return out
