"""Round 3 Shirorekha - geometry helpers. All coordinates SVG y-down; a letter's bar top is y=0, baseline y=H."""
import math, re, sys, os
SCRATCH = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
sys.path.insert(0, os.path.join(SCRATCH, 'logo2', 'toolkit'))
import vtype as V
import pathops

HERE = os.path.dirname(os.path.abspath(__file__))
PAL = V.PALETTE
EM, IV, GO, GL, WH = PAL['emerald'], PAL['ivory'], PAL['gold'], PAL['gold_lt'], PAL['white']
KAPPA = 0.5522847498


def path_from(cmds):
    """cmds: list of ('M',x,y) ('L',x,y) ('Q',cx,cy,x,y) ('C',...) ; closes automatically."""
    p = pathops.Path()
    for c in cmds:
        if c[0] == 'M':
            p.moveTo(*c[1:])
        elif c[0] == 'L':
            p.lineTo(*c[1:])
        elif c[0] == 'Q':
            p.quadTo(*c[1:])
        elif c[0] == 'C':
            p.cubicTo(*c[1:])
    p.close()
    return V.union(p)


def poly(pts):
    return path_from([('M',) + tuple(pts[0])] + [('L',) + tuple(q) for q in pts[1:]])


def rect(x0, y0, x1, y1):
    return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def ellipse(cx, cy, rx, ry, k=KAPPA):
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


def U(*ps):
    return V.union(*[p for p in ps if p is not None])


def D(a, b):
    return V.difference(a, b)


def I(a, b):
    return V.intersection(a, b)


def tr(path, s=1.0, dx=0.0, dy=0.0, sy=None):
    return V.transform(path, s, 0, 0, s if sy is None else sy, dx, dy)


def mirror_x(path, axis=0.0):
    return V.transform(path, -1, 0, 0, 1, 2 * axis, 0)


def bbox(path):
    return V.bounds(path)


def line_x(p0, p1, y):
    (x0, y0), (x1, y1) = p0, p1
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def line_y(p0, p1, x):
    (x0, y0), (x1, y1) = p0, p1
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def isect(a0, a1, b0, b1):
    x1, y1 = a0; x2, y2 = a1; x3, y3 = b0; x4, y4 = b1
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def unit_normal_left(p0, p1):
    """Unit normal pointing to screen-left of a chord that travels downward (y-down coords)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    return nx, ny


def ctrl(p0, p1, bulge, frac=0.5):
    """Quadratic control point: chord point at frac, pushed by bulge along the normal (-dy, dx)/L.
    For a chord travelling downward that normal points to screen-left, so +bulge bows the curve left."""
    mx, my = p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac
    nx, ny = unit_normal_left(p0, p1)
    return (mx + nx * bulge * 2, my + ny * bulge * 2)   # *2: a quad's max deviation is half the control offset


def qpt(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])


def qsplit(p0, c, p1, t):
    """Sub-curve [0,t]: returns (control, end)."""
    a = (p0[0] + (c[0] - p0[0]) * t, p0[1] + (c[1] - p0[1]) * t)
    b = (c[0] + (p1[0] - c[0]) * t, c[1] + (p1[1] - c[1]) * t)
    e = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return a, e


def qsplit_hi(p0, c, p1, t):
    """Sub-curve [t,1]: returns (start, control)."""
    b = (c[0] + (p1[0] - c[0]) * t, c[1] + (p1[1] - c[1]) * t)
    a = (p0[0] + (c[0] - p0[0]) * t, p0[1] + (c[1] - p0[1]) * t)
    e = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return e, b


def q_isect_line(p0, c, p1, a, b, n=600):
    """Parameter t where quadratic crosses line a->b (searching from t=1 backwards)."""
    def side(pt):
        return (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
    prev_t, prev_s = 1.0, side(qpt(p0, c, p1, 1.0))
    for i in range(n - 1, -1, -1):
        t = i / n
        s = side(qpt(p0, c, p1, t))
        if (s > 0) != (prev_s > 0):
            lo, hi = t, prev_t
            for _ in range(60):
                mid = (lo + hi) / 2
                if (side(qpt(p0, c, p1, mid)) > 0) == (s > 0):
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev_t, prev_s = t, s
    return None


def q_extreme_x(p0, c, p1):
    """min x on a quadratic."""
    xs = [p0[0], p1[0]]
    den = p0[0] - 2 * c[0] + p1[0]
    if abs(den) > 1e-9:
        t = (p0[0] - c[0]) / den
        if 0 < t < 1:
            xs.append(qpt(p0, c, p1, t)[0])
    return min(xs), max(xs)


def centroid(path):
    from fontTools.pens.statisticsPen import StatisticsPen
    pen = StatisticsPen()
    path.draw(pen)
    return pen.meanX, pen.meanY


def area(path):
    from fontTools.pens.areaPen import AreaPen
    pen = AreaPen()
    path.draw(pen)
    return abs(pen.value)


def rd(path):
    d = V.to_d(path)
    return re.sub(r'-?\d+\.\d+', lambda m: ('%.2f' % float(m.group())).rstrip('0').rstrip('.'), d)


def svg(w, h, layers, bg=None, title='VanIndra Creations'):
    body = ''.join(f'<path fill="{c}" d="{rd(p)}"/>' for p, c in layers if p is not None)
    return V.svg_doc(round(w, 2), round(h, 2), body, bg=bg, title=title)


def write(path, content):
    with open(path, 'w') as f:
        f.write(content)
    return path


def norm(path):
    x0, y0, x1, y1 = bbox(path)
    return tr(path, 1, -x0, -y0)


# ---------------------------------------------------------------- cubic helpers
def cpt(p0, c1, c2, p1, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p1[0],
            u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p1[1])


def csplit(p0, c1, c2, p1, t):
    """De Casteljau. Returns (left=(p0,a,b,m), right=(m,c,d,p1))."""
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a = lerp(p0, c1); bb = lerp(c1, c2); c = lerp(c2, p1)
    d = lerp(a, bb); e = lerp(bb, c)
    m = lerp(d, e)
    return (p0, a, d, m), (m, e, c, p1)


def c_isect_line(p0, c1, c2, p1, a, b, n=800, from_end=True):
    def side(pt):
        return (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
    rng = range(n - 1, -1, -1) if from_end else range(1, n + 1)
    prev_t = 1.0 if from_end else 0.0
    prev_s = side(cpt(p0, c1, c2, p1, prev_t))
    for i in rng:
        t = i / n
        s = side(cpt(p0, c1, c2, p1, t))
        if (s > 0) != (prev_s > 0):
            lo, hi = (t, prev_t) if from_end else (prev_t, t)
            s_lo = side(cpt(p0, c1, c2, p1, lo)) > 0
            for _ in range(60):
                mid = (lo + hi) / 2
                if (side(cpt(p0, c1, c2, p1, mid)) > 0) == s_lo:
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev_t, prev_s = t, s
    return None


def c_x_at_y(p0, c1, c2, p1, y):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if cpt(p0, c1, c2, p1, m)[1] < y:
            lo = m
        else:
            hi = m
    return cpt(p0, c1, c2, p1, (lo + hi) / 2)[0]


def c_extreme_x(p0, c1, c2, p1, n=400):
    xs = [cpt(p0, c1, c2, p1, i / n)[0] for i in range(n + 1)]
    return min(xs), max(xs)


# ---------------------------------------------------------------- the shared leaf
LEAF = dict(t0=4.0, ko1=4.5, ko2=4.0, ki1=-4.0, ki2=-12.0, uo1=0.30, uo2=0.72, ui1=0.30, ui2=0.80)


def leaf_chord(O0, P, t0=4.0, ko1=4.5, ko2=4.0, ki1=-4.0, ki2=-12.0, uo1=0.30, uo2=0.72, ui1=0.30, ui2=0.80):
    """The VanIndra leaf: a stroke from a thin top (width t0, measured horizontally at O0's y) to a point P.
    Control points are given in the chord frame: u along O0->P (0..1), v perpendicular (+ = screen-left / outward).
    Returns (outer_cubic, inner_cubic), both running top -> P."""
    ux, uy = P[0] - O0[0], P[1] - O0[1]
    L = math.hypot(ux, uy)
    ex, ey = ux / L, uy / L                 # along chord
    nx, ny = -ey, ex                        # screen-left normal for a downward chord
    W = lambda u, v: (O0[0] + ex * u * L + nx * v, O0[1] + ey * u * L + ny * v)
    outer = (O0, W(uo1, ko1), W(uo2, ko2), P)
    I0 = (O0[0] + t0, O0[1])
    # inner chord frame starts at I0
    ux2, uy2 = P[0] - I0[0], P[1] - I0[1]
    L2 = math.hypot(ux2, uy2)
    ex2, ey2 = ux2 / L2, uy2 / L2
    nx2, ny2 = -ey2, ex2
    W2 = lambda u, v: (I0[0] + ex2 * u * L2 + nx2 * v, I0[1] + ey2 * u * L2 + ny2 * v)
    inner = (I0, W2(ui1, ki1), W2(ui2, ki2), P)
    return outer, inner
