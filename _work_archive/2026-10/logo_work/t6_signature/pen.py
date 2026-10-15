"""Pointed-pen calligraphy engine (pure Python + skia-pathops).

Design space: upright, y-UP, baseline y=0, x-height X=100.
A stroke is a list of nodes  N(x, y, ang, p=1, k=0.55)
  ang : tangent direction in degrees (upright space; 0=right, 90=up, -90=down)
  p   : pressure multiplier at the node (0 = force hairline, 1 = full shade allowed)
  k   : tension of the segment that LEAVES this node (0.552 = elliptical quadrant)
Each segment is a cubic whose handles run along the node tangents to the point where
the two tangent lines meet ("control triangle") scaled by the tension -> curves are
computed from the grid, never hand-wobbled.
After construction the skeleton is sheared to one fixed slant, so every stem and
oval axis shares the same angle (consistent pen logic).
Width model (pointed pen): shade only when the pen moves DOWN the slant axis.
  w = hair + (shade - hair) * smoothstep(d0, 1, downness) * p
The outline is the exact envelope of the moving circular nib (radius w/2, including
dr/ds), curve-fitted to clean cubics (Schneider), then unioned with pathops.
"""
import math
import sys

import pathops

sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype  # noqa: E402


class N:
    __slots__ = ('x', 'y', 'ang', 'p', 'k')

    def __init__(self, x, y, ang, p=1.0, k=0.55):
        self.x, self.y, self.ang, self.p, self.k = float(x), float(y), float(ang), float(p), float(k)

    def moved(self, dx=0, dy=0):
        return N(self.x + dx, self.y + dy, self.ang, self.p, self.k)


# ---------------------------------------------------------------- geometry

def seg_ctrl(a, b):
    """Control points for node a -> node b using the tangent-intersection rule."""
    d0 = (math.cos(math.radians(a.ang)), math.sin(math.radians(a.ang)))
    d1 = (math.cos(math.radians(b.ang)), math.sin(math.radians(b.ang)))
    dx, dy = b.x - a.x, b.y - a.y
    chord = math.hypot(dx, dy)
    det = d0[0] * (-d1[1]) - d0[1] * (-d1[0])  # solve a + s d0 = b - u d1
    proj = abs(dx * d0[0] + dy * d0[1])
    par = max(proj, 0.35 * chord) * a.k * 0.95   # parallel / S-curve fallback
    h0 = h1 = par
    if abs(det) > 1e-6:
        s = (dx * (-d1[1]) - dy * (-d1[0])) / det
        u = (d0[0] * dy - d0[1] * dx) / det
        if s > 1e-6 and u > 1e-6 and s < 3 * chord and u < 3 * chord:
            h0, h1 = a.k * s, a.k * u
    return ((a.x, a.y), (a.x + h0 * d0[0], a.y + h0 * d0[1]),
            (b.x - h1 * d1[0], b.y - h1 * d1[1]), (b.x, b.y))


def bez(c, t):
    mt = 1 - t
    a, b, cc, d = mt * mt * mt, 3 * mt * mt * t, 3 * mt * t * t, t * t * t
    return (a * c[0][0] + b * c[1][0] + cc * c[2][0] + d * c[3][0],
            a * c[0][1] + b * c[1][1] + cc * c[2][1] + d * c[3][1])


def dbez(c, t):
    mt = 1 - t
    a, b, cc = 3 * mt * mt, 6 * mt * t, 3 * t * t
    return (a * (c[1][0] - c[0][0]) + b * (c[2][0] - c[1][0]) + cc * (c[3][0] - c[2][0]),
            a * (c[1][1] - c[0][1]) + b * (c[2][1] - c[1][1]) + cc * (c[3][1] - c[2][1]))


def smoothstep(e0, e1, x):
    if e1 == e0:
        return 1.0 if x >= e1 else 0.0
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


class Pen:
    def __init__(self, slant=14.0, hair=5.0, shade=17.0, d0=0.30, gamma=1.0, mode='pointed', nib_angle=35.0,
                 step=0.6):
        self.slant, self.hair, self.shade, self.d0, self.gamma = slant, hair, shade, d0, gamma
        self.mode, self.nib_angle, self.step = mode, nib_angle, step
        self.t = math.tan(math.radians(slant))

    def width(self, ux, uy, p):
        n = math.hypot(ux, uy) or 1.0
        ux, uy = ux / n, uy / n
        if self.mode == 'mono':
            return self.hair
        if self.mode == 'broad':
            th = math.radians(self.nib_angle)
            f = abs(ux * math.sin(th) - uy * math.cos(th))
            return self.hair + (self.shade - self.hair) * f * p
        down = max(0.0, -uy)
        f = smoothstep(self.d0, 1.0, down) ** self.gamma
        return self.hair + (self.shade - self.hair) * f * p

    def sample(self, nodes):
        """Return list of (X, Y, w) in final (sheared) y-up space."""
        if hasattr(nodes, 'segs'):
            return self.sample_segs(nodes.segs)
        out = []
        for i in range(len(nodes) - 1):
            a, b = nodes[i], nodes[i + 1]
            c = seg_ctrl(a, b)
            L = sum(math.hypot(bez(c, (j + 1) / 16)[0] - bez(c, j / 16)[0], bez(c, (j + 1) / 16)[1] - bez(c, j / 16)[1])
                    for j in range(16))
            n = max(8, int(L / self.step))
            for j in range(0 if i == 0 else 1, n + 1):
                t = j / n
                x, y = bez(c, t)
                ux, uy = dbez(c, t)
                if abs(ux) + abs(uy) < 1e-9:
                    ux, uy = math.cos(math.radians(a.ang if t < .5 else b.ang)), math.sin(math.radians(a.ang if t < .5 else b.ang))
                pp = a.p + (b.p - a.p) * (t * t * (3 - 2 * t))
                w = self.width(ux, uy, pp)
                out.append((x + y * self.t, y, w))
        return out


    def sample_segs(self, segs):
        out = []
        for i, seg in enumerate(segs):
            P0, C1, C2, P3, p0, p1 = seg[:6]
            ease = seg[6] if len(seg) > 6 else None
            c = (P0, C1, C2, P3)
            L = sum(math.hypot(bez(c, (j + 1) / 16)[0] - bez(c, j / 16)[0], bez(c, (j + 1) / 16)[1] - bez(c, j / 16)[1])
                    for j in range(16))
            n = max(6, int(L / self.step))
            for j in range(0 if i == 0 else 1, n + 1):
                t = j / n
                x, y = bez(c, t)
                ux, uy = dbez(c, t)
                if abs(ux) + abs(uy) < 1e-9:
                    ux, uy = dbez(c, min(1, max(0, t + (1e-3 if t < .5 else -1e-3))))
                if ease is None:
                    e = t * t * (3 - 2 * t)
                elif ease == 'linear':
                    e = t
                elif ease == 'ramp':           # C1: soft start, straight middle, soft finish
                    e = ease_ramp(t)
                elif ease == 'taper':          # C1 at start (soft shoulder), then straight wedge to the tip
                    e = ease_taper(t)
                elif ease == 'taper_soft':
                    e = ease_taper(t, 0.6)
                elif ease == 'ogive_out':      # zero slope at start, closes like a pointed arch
                    e = 1 - math.sqrt(max(0.0, 1 - t * t))
                elif ease == 'ogive_in':       # opens like a pointed arch, zero slope at end
                    e = math.sqrt(max(0.0, 1 - (1 - t) * (1 - t)))
                else:  # numeric exponent: e = t**ease  (ease>1: slow start, convex taper)
                    e = t ** ease
                pp = p0 + (p1 - p0) * e
                out.append((x + y * self.t, y, self.width(ux, uy, pp)))
        return out


def ease_ramp(t, a=0.28):
    vmax = 1.0 / (1 - a)
    if t < a:
        return 0.5 * vmax * t * t / a
    if t <= 1 - a:
        return 0.5 * vmax * a + vmax * (t - a)
    u = 1 - t
    return 1 - 0.5 * vmax * u * u / a


def ease_taper(t, a=0.32):
    vmax = 1.0 / (1 - a / 2)
    if t < a:
        return 0.5 * vmax * t * t / a
    return 0.5 * vmax * a + vmax * (t - a)


# ---------------------------------------------------------------- Schneider curve fitting

def _sub(a, b): return (a[0] - b[0], a[1] - b[1])
def _add(a, b): return (a[0] + b[0], a[1] + b[1])
def _mul(a, s): return (a[0] * s, a[1] * s)
def _dot(a, b): return a[0] * b[0] + a[1] * b[1]


def _norm(a):
    l = math.hypot(*a)
    return (a[0] / l, a[1] / l) if l > 1e-12 else (0.0, 0.0)


def _gen(pts, u, t1, t2):
    p0, p3 = pts[0], pts[-1]
    C = [[0.0, 0.0], [0.0, 0.0]]
    X = [0.0, 0.0]
    for i, ui in enumerate(u):
        mt = 1 - ui
        A1 = _mul(t1, 3 * mt * mt * ui)
        A2 = _mul(t2, 3 * mt * ui * ui)
        C[0][0] += _dot(A1, A1); C[0][1] += _dot(A1, A2); C[1][1] += _dot(A2, A2)
        b0 = mt ** 3 + 3 * mt * mt * ui
        b1 = 3 * mt * ui * ui + ui ** 3
        tmp = _sub(pts[i], _add(_mul(p0, b0), _mul(p3, b1)))
        X[0] += _dot(A1, tmp); X[1] += _dot(A2, tmp)
    C[1][0] = C[0][1]
    det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    seg = math.hypot(*_sub(p3, p0))
    eps = 1e-6 * seg
    if abs(det) > 1e-12:
        al = (X[0] * C[1][1] - X[1] * C[0][1]) / det
        ar = (C[0][0] * X[1] - C[1][0] * X[0]) / det
    else:
        al = ar = seg / 3
    if al < eps or ar < eps:
        al = ar = seg / 3
    return (p0, _add(p0, _mul(t1, al)), _add(p3, _mul(t2, ar)), p3)


def _maxerr(pts, c, u):
    m, idx = 0.0, len(pts) // 2
    for i in range(1, len(pts) - 1):
        q = bez(c, u[i])
        d = (q[0] - pts[i][0]) ** 2 + (q[1] - pts[i][1]) ** 2
        if d >= m:
            m, idx = d, i
    return m, idx


def _newton(c, p, u):
    q = bez(c, u)
    d1 = dbez(c, u)
    # second derivative
    mt = 1 - u
    d2 = (6 * mt * (c[2][0] - 2 * c[1][0] + c[0][0]) + 6 * u * (c[3][0] - 2 * c[2][0] + c[1][0]),
          6 * mt * (c[2][1] - 2 * c[1][1] + c[0][1]) + 6 * u * (c[3][1] - 2 * c[2][1] + c[1][1]))
    num = (q[0] - p[0]) * d1[0] + (q[1] - p[1]) * d1[1]
    den = d1[0] ** 2 + d1[1] ** 2 + (q[0] - p[0]) * d2[0] + (q[1] - p[1]) * d2[1]
    if abs(den) < 1e-12:
        return u
    return min(1.0, max(0.0, u - num / den))


def _chord(pts):
    u = [0.0]
    for i in range(1, len(pts)):
        u.append(u[-1] + math.hypot(*_sub(pts[i], pts[i - 1])))
    L = u[-1] or 1.0
    return [x / L for x in u]


def fit(pts, tol=0.04):
    if len(pts) < 2:
        return []
    k = min(3, len(pts) - 1)
    t1 = _norm(_sub(pts[k], pts[0]))
    t2 = _norm(_sub(pts[-1 - k], pts[-1]))
    return _fit(pts, t1, t2, tol * tol)


def _fit(pts, t1, t2, err):
    if len(pts) == 2:
        d = math.hypot(*_sub(pts[1], pts[0])) / 3
        return [(pts[0], _add(pts[0], _mul(t1, d)), _add(pts[1], _mul(t2, d)), pts[1])]
    u = _chord(pts)
    c = _gen(pts, u, t1, t2)
    m, split = _maxerr(pts, c, u)
    if m < err:
        return [c]
    if m < err * 16:
        for _ in range(12):
            u = [_newton(c, pts[i], u[i]) for i in range(len(pts))]
            c = _gen(pts, u, t1, t2)
            m, split = _maxerr(pts, c, u)
            if m < err:
                return [c]
    split = max(1, min(len(pts) - 2, split))
    lo, hi = max(0, split - 2), min(len(pts) - 1, split + 2)
    tc = _norm(_sub(pts[lo], pts[hi]))
    if tc == (0.0, 0.0):
        tc = _norm(_sub(pts[split - 1], pts[split + 1]))
    return _fit(pts[:split + 1], t1, tc, err) + _fit(pts[split:], (-tc[0], -tc[1]), t2, err)


# ---------------------------------------------------------------- outline

def circle_path(cx, cy, r, path=None):
    k = 0.5522847498 * r
    p = path if path is not None else pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def stroke_outline(samples, tol=0.04, caps=True):
    n = len(samples)
    P = [(s[0], s[1]) for s in samples]
    R = [s[2] / 2 for s in samples]
    S = [0.0]
    for i in range(1, n):
        S.append(S[-1] + math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]))
    left, right = [], []
    for i in range(n):
        i0, i1 = max(0, i - 1), min(n - 1, i + 1)
        T = _norm(_sub(P[i1], P[i0]))
        ds = S[i1] - S[i0]
        rp = (R[i1] - R[i0]) / ds if ds > 1e-9 else 0.0
        rp = max(-0.9, min(0.9, rp))
        Nn = (-T[1], T[0])
        q = math.sqrt(1 - rp * rp)
        base = _add(P[i], _mul(T, -R[i] * rp))
        left.append(_add(base, _mul(Nn, R[i] * q)))
        right.append(_add(base, _mul(Nn, -R[i] * q)))
    L = fit(left, tol)
    Rr = fit(right[::-1], tol)
    path = pathops.Path()
    path.moveTo(*L[0][0])
    for c in L:
        path.cubicTo(*c[1], *c[2], *c[3])
    path.lineTo(*Rr[0][0])
    for c in Rr:
        path.cubicTo(*c[1], *c[2], *c[3])
    path.close()
    # resolve self overlaps inside the ribbon
    path = pathops.op(path, path, pathops.PathOp.UNION)
    if caps:
        cap = pathops.Path()
        circle_path(P[0][0], P[0][1], R[0], cap)
        circle_path(P[-1][0], P[-1][1], R[-1], cap)
        cap = pathops.op(cap, cap, pathops.PathOp.UNION)
        path = pathops.op(path, cap, pathops.PathOp.UNION)
    return path


class St(list):
    """A stroke: list of nodes + options (ball0/ball1 = terminal ball radius at start/end, pen override)."""

    def __init__(self, nodes, ball0=0.0, ball1=0.0, pen=None, scale=1.0):
        super().__init__(nodes)
        self.ball0, self.ball1, self.pen, self.scale = ball0, ball1, pen, scale


def _bulb(smp, r, at_start=True, k=2.4):
    """Blend a round drop of radius r into the stroke end: w = sqrt(w^2 + bump^2), bump -> 0 smoothly."""
    if not r:
        return smp
    seq = smp if at_start else smp[::-1]
    L = k * r
    out, s = [], 0.0
    for i, (x, y, w) in enumerate(seq):
        if i:
            s += math.hypot(x - seq[i - 1][0], y - seq[i - 1][1])
        if s < L:
            u = s / L
            bump = 2 * r * (1 - u * u) ** 1.5
            w = math.sqrt(w * w + bump * bump)
        out.append((x, y, w))
    return out if at_start else out[::-1]


def render(strokes, pen, tol=0.04, hair_boost=0.0):
    """strokes: list of node lists / St / SB. Returns pathops.Path in y-UP space."""
    acc = None
    for s in strokes:
        pn = getattr(s, 'pen', None) or pen
        smp = pn.sample(s)
        if hair_boost:
            smp = [(x, y, w + hair_boost) for x, y, w in smp]
        smp = _bulb(smp, getattr(s, 'ball0', 0.0), True)
        smp = _bulb(smp, getattr(s, 'ball1', 0.0), False)
        o = stroke_outline(smp, tol)
        acc = o if acc is None else pathops.op(acc, o, pathops.PathOp.UNION)
    return acc


def skeleton_d(strokes, pen):
    """Skeleton polylines (y-up) for debugging overlays."""
    out = []
    for s in strokes:
        if isinstance(s, tuple):
            s = s[0]
        smp = pen.sample(s)
        out.append('M' + ' L'.join(f'{x:.1f},{-y:.1f}' for x, y, _ in smp[::3]))
    return ' '.join(out)


def flip(path, s=1.0, tx=0.0, ty=0.0):
    """y-up design space -> SVG y-down, scaled by s then translated."""
    return vtype.transform(path, s, 0, 0, -s, tx, ty)


def d_of(path, nd=2):
    d = vtype.to_d(path)
    import re
    return re.sub(r'-?\d+\.\d+', lambda m: f'{float(m.group()):.{nd}f}'.rstrip('0').rstrip('.'), d)
