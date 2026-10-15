"""F1 polish: turn sampled pen outlines into true cubic Beziers (judge: 'every Devanagari outline is a sampled
polyline, 414 straight L segments, facets will show in large print'). Philip J. Schneider's least-squares fit
(Graphics Gems, 1990): chord-length parameters, Newton reparameterisation, split at the worst point with a
continuous centre tangent, so the fitted sides are G1-smooth. Used by the contrast pen (C, S, da) and the na drop."""
import math
import pathops


def _sub(a, b): return (a[0] - b[0], a[1] - b[1])
def _add(a, b): return (a[0] + b[0], a[1] + b[1])
def _mul(a, s): return (a[0] * s, a[1] * s)
def _dot(a, b): return a[0] * b[0] + a[1] * b[1]
def _len(a): return math.hypot(a[0], a[1])


def _norm(a):
    L = _len(a) or 1.0
    return (a[0] / L, a[1] / L)


def _bez(c, t):
    u = 1 - t
    return (u ** 3 * c[0][0] + 3 * u * u * t * c[1][0] + 3 * u * t * t * c[2][0] + t ** 3 * c[3][0],
            u ** 3 * c[0][1] + 3 * u * u * t * c[1][1] + 3 * u * t * t * c[2][1] + t ** 3 * c[3][1])


def _bez1(c, t):
    u = 1 - t
    return (3 * (u * u * (c[1][0] - c[0][0]) + 2 * u * t * (c[2][0] - c[1][0]) + t * t * (c[3][0] - c[2][0])),
            3 * (u * u * (c[1][1] - c[0][1]) + 2 * u * t * (c[2][1] - c[1][1]) + t * t * (c[3][1] - c[2][1])))


def _bez2(c, t):
    u = 1 - t
    return (6 * (u * (c[2][0] - 2 * c[1][0] + c[0][0]) + t * (c[3][0] - 2 * c[2][0] + c[1][0])),
            6 * (u * (c[2][1] - 2 * c[1][1] + c[0][1]) + t * (c[3][1] - 2 * c[2][1] + c[1][1])))


def _chord_params(pts):
    u = [0.0]
    for i in range(1, len(pts)):
        u.append(u[-1] + _len(_sub(pts[i], pts[i - 1])))
    T = u[-1] or 1.0
    return [v / T for v in u]


def _generate(pts, u, t1, t2):
    p0, p3 = pts[0], pts[-1]
    C = [[0.0, 0.0], [0.0, 0.0]]
    X = [0.0, 0.0]
    for p, t in zip(pts, u):
        b0, b1, b2, b3 = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        A1, A2 = _mul(t1, b1), _mul(t2, b2)
        C[0][0] += _dot(A1, A1); C[0][1] += _dot(A1, A2); C[1][1] += _dot(A2, A2)
        tmp = _sub(p, _add(_add(_mul(p0, b0 + b1), (0, 0)), _mul(p3, b2 + b3)))
        X[0] += _dot(A1, tmp); X[1] += _dot(A2, tmp)
    C[1][0] = C[0][1]
    det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    seg = _len(_sub(p3, p0))
    if abs(det) > 1e-12:
        a1 = (X[0] * C[1][1] - X[1] * C[0][1]) / det
        a2 = (C[0][0] * X[1] - C[1][0] * X[0]) / det
    else:
        a1 = a2 = seg / 3
    eps = 1e-6 * seg
    if a1 < eps or a2 < eps:
        a1 = a2 = seg / 3
    return (p0, _add(p0, _mul(t1, a1)), _add(p3, _mul(t2, a2)), p3)


def _max_err(pts, c, u):
    mx, idx = 0.0, len(pts) // 2
    for i in range(1, len(pts) - 1):
        d = _len(_sub(_bez(c, u[i]), pts[i])) ** 2
        if d >= mx:
            mx, idx = d, i
    return mx, idx


def _reparam(pts, c, u):
    out = []
    for p, t in zip(pts, u):
        d = _sub(_bez(c, t), p)
        q1, q2 = _bez1(c, t), _bez2(c, t)
        num = _dot(d, q1)
        den = _dot(q1, q1) + _dot(d, q2)
        out.append(t - num / den if abs(den) > 1e-12 else t)
    return out


def _fit(pts, t1, t2, err, depth=0):
    if len(pts) == 2:
        d = _len(_sub(pts[1], pts[0])) / 3
        return [(pts[0], _add(pts[0], _mul(t1, d)), _add(pts[1], _mul(t2, d)), pts[1])]
    u = _chord_params(pts)
    c = _generate(pts, u, t1, t2)
    e, split = _max_err(pts, c, u)
    if e < err:
        return [c]
    if e < err * 16:
        for _ in range(20):
            u = _reparam(pts, c, u)
            c = _generate(pts, u, t1, t2)
            e, split = _max_err(pts, c, u)
            if e < err:
                return [c]
    if depth > 12:
        return [c]
    tc = _norm(_sub(pts[split - 1], pts[split + 1]))
    return (_fit(pts[:split + 1], t1, tc, err, depth + 1) +
            _fit(pts[split:], (-tc[0], -tc[1]), t2, err, depth + 1))


def fit_polyline(pts, tol=0.06):
    """Least-squares cubic fit of an open polyline (sampled from a smooth curve). tol: max deviation (units)."""
    q = [pts[0]]
    for p in pts[1:]:
        if _len(_sub(p, q[-1])) > 1e-6:
            q.append(p)
    if len(q) < 3:
        return [(q[0], q[0], q[-1], q[-1])]
    t1 = _norm(_sub(q[1], q[0]))
    t2 = _norm(_sub(q[-2], q[-1]))
    return _fit(q, t1, t2, tol * tol)


def outline(L, R, tol=0.06):
    """Closed outline from two sampled sides of a stroke (L forward, R forward): fitted L, a straight terminal,
    fitted R reversed, a straight terminal."""
    p = pathops.Path()
    p.moveTo(*L[0])
    for c in fit_polyline(L, tol):
        p.cubicTo(*c[1], *c[2], *c[3])
    p.lineTo(*R[-1])
    for c in fit_polyline(R[::-1], tol):
        p.cubicTo(*c[1], *c[2], *c[3])
    p.close()
    import vtype as V
    return V.union(p)


def closed(pts, tol=0.06):
    """Closed smooth contour from a sampled closed polyline (no corners)."""
    n = len(pts)
    a = pts[: n // 2 + 1]
    b = pts[n // 2:] + [pts[0]]
    p = pathops.Path()
    p.moveTo(*a[0])
    for seg in (a, b):
        cs = fit_polyline(seg, tol)
        for c in cs:
            p.cubicTo(*c[1], *c[2], *c[3])
    p.close()
    import vtype as V
    return V.union(p)
