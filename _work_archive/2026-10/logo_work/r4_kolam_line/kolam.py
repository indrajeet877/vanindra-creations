"""Kolam line engine: exact arcs around pulli (dots) joined by straight tangents.

A kolam line is modelled as a closed belt around a cyclic list of visits
(center, radius, dir) with dir=+1 counter-clockwise, -1 clockwise (math axes, y up).
Between consecutive visits the belt runs on the common tangent: same dir -> outer
tangent, opposite dir -> crossing tangent (this is where the flat kolam crossing comes from).
Every join is G1 (tangent) by construction.
"""
import math, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype
import pathops

TAU = 2 * math.pi


def tangent(c1, r1, s1, c2, r2, s2):
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    th = math.atan2(dy, dx)
    k = s2 * r2 - s1 * r1
    if abs(k) > d:
        raise ValueError('no tangent')
    phi = th - math.asin(k / d)
    t = (math.cos(phi), math.sin(phi))
    L = (-t[1], t[0])
    p1 = (c1[0] - s1 * r1 * L[0], c1[1] - s1 * r1 * L[1])
    p2 = (c2[0] - s2 * r2 * L[0], c2[1] - s2 * r2 * L[1])
    return p1, p2, phi


def build(visits, loops=None):
    """visits: list of (center, r, dir). loops: optional dict idx->extra full turns.
    Returns list of segments: ('L', p0, p1) and ('A', c, r, a0, span) (span signed)."""
    n = len(visits)
    tans = []
    for i in range(n):
        (c1, r1, s1), (c2, r2, s2) = visits[i], visits[(i + 1) % n]
        tans.append(tangent(c1, r1, s1, c2, r2, s2))
    segs = []
    for i in range(n):
        c, r, s = visits[i]
        arr = tans[i - 1][1]   # arrival point on circle i
        dep = tans[i][0]
        a0 = math.atan2(arr[1] - c[1], arr[0] - c[0])
        a1 = math.atan2(dep[1] - c[1], dep[0] - c[0])
        span = (a1 - a0) % TAU if s > 0 else -((a0 - a1) % TAU)
        if abs(span) > TAU - 1e-7:
            span = 0.0
        if loops and i in loops:
            span += s * TAU * loops[i]
        if r > 0 and abs(span) > 1e-9:
            segs.append(('A', c, r, a0, span))
        p0, p1, _ = tans[i]
        segs.append(('L', p0, p1))
    return segs


def arc_beziers(c, r, a0, span):
    nseg = max(1, int(math.ceil(abs(span) / (math.pi / 4) - 1e-9)))
    out = []
    da = span / nseg
    k = 4 / 3 * math.tan(da / 4)
    for j in range(nseg):
        t0 = a0 + j * da
        t1 = t0 + da
        p0 = (c[0] + r * math.cos(t0), c[1] + r * math.sin(t0))
        p3 = (c[0] + r * math.cos(t1), c[1] + r * math.sin(t1))
        p1 = (p0[0] - k * r * math.sin(t0), p0[1] + k * r * math.cos(t0))
        p2 = (p3[0] + k * r * math.sin(t1), p3[1] - k * r * math.cos(t1))
        out.append((p1, p2, p3))
    return out


def to_pathops(segs, flip=True):
    """Centre-line as a pathops.Path (y flipped to SVG if flip)."""
    f = (lambda p: (p[0], -p[1])) if flip else (lambda p: p)
    P = pathops.Path()
    first = True
    for s in segs:
        if s[0] == 'L':
            p0, p1 = f(s[1]), f(s[2])
            if first:
                P.moveTo(*p0); first = False
            P.lineTo(*p1)
        else:
            _, c, r, a0, span = s
            st = f((c[0] + r * math.cos(a0), c[1] + r * math.sin(a0)))
            if first:
                P.moveTo(*st); first = False
            for p1, p2, p3 in arc_beziers(c, r, a0, span):
                P.cubicTo(*f(p1), *f(p2), *f(p3))
    P.close()
    return P


def outline(segs, w, flip=True):
    return vtype.stroke_to_path(to_pathops(segs, flip), w, cap='round', join='round')


def circle_path(c, r, flip=True):
    cc = (c[0], -c[1]) if flip else c
    P = pathops.Path()
    k = 0.5522847498 * r
    x, y = cc
    P.moveTo(x + r, y)
    P.cubicTo(x + r, y + k, x + k, y + r, x, y + r)
    P.cubicTo(x - k, y + r, x - r, y + k, x - r, y)
    P.cubicTo(x - r, y - k, x - k, y - r, x, y - r)
    P.cubicTo(x + k, y - r, x + r, y - k, x + r, y)
    P.close()
    return P


def dots_path(centers, rd, flip=True):
    return vtype.union(*[circle_path(c, rd, flip) for c in centers])


def fit(path, box, pad=0.12, cx=None):
    """Transform path to fit centred in a box (w,h) with padding fraction."""
    x0, y0, x1, y1 = vtype.bounds(path)
    W, H = box
    s = min(W * (1 - 2 * pad) / (x1 - x0), H * (1 - 2 * pad) / (y1 - y0))
    tx = W / 2 - s * (x0 + x1) / 2
    ty = H / 2 - s * (y0 + y1) / 2
    return s, tx, ty


def tf(path, s, tx, ty):
    return vtype.transform(path, s, 0, 0, s, tx, ty)
