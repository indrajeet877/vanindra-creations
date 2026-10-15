"""Round 3 final-final additions to the drawn alphabet.
- vstroke: a variable-width pen. Width follows the same contrast rule as the capitals: a stroke is full weight
  where it travels vertically (a danda) and hairline where it travels horizontally (the line). Used for C and S,
  so their stress matches the D/R/O superellipse bowls and the S has no construction seams.
- CREATIONS letters rebuilt: A, R, N use the VANINDRA constructors (leaf diagonals); C, O, S have real contrast."""
from r3geo import *
from r3latin import St, BUILD, wordmark, g_A, g_N, g_R, g_I, g_E, g_T, g_O, _ring


def _cubic_samples(seg, n):
    p0, c1, c2, p1 = seg
    out = []
    for i in range(n + 1):
        t = i / n
        pt = cpt(p0, c1, c2, p1, t)
        u = 1 - t
        dx = 3 * u * u * (c1[0] - p0[0]) + 6 * u * t * (c2[0] - c1[0]) + 3 * t * t * (p1[0] - c2[0])
        dy = 3 * u * u * (c1[1] - p0[1]) + 6 * u * t * (c2[1] - c1[1]) + 3 * t * t * (p1[1] - c2[1])
        L = math.hypot(dx, dy) or 1.0
        out.append((pt, (dx / L, dy / L)))
    return out


def vstroke(segs, S, h, n=48, p=1.35, taper0=None, taper1=None):
    """segs: list of cubics (p0,c1,c2,p1) joined end to start. Width = h + (S-h)*|ty|^p.
    taper0/taper1: width at the start/end terminals (None = natural)."""
    samples = []
    for k, sg in enumerate(segs):
        s = _cubic_samples(sg, n)
        samples += s if k == 0 else s[1:]
    N = len(samples)
    L, R = [], []
    for i, (pt, (tx, ty)) in enumerate(samples):
        w = h + (S - h) * abs(ty) ** p
        f = i / (N - 1)
        if taper0 is not None and f < 0.12:
            w = taper0 + (w - taper0) * (f / 0.12) ** 0.8
        if taper1 is not None and f > 0.88:
            w = taper1 + (w - taper1) * ((1 - f) / 0.12) ** 0.8
        nx, ny = -ty, tx
        L.append((pt[0] + nx * w / 2, pt[1] + ny * w / 2))
        R.append((pt[0] - nx * w / 2, pt[1] - ny * w / 2))
    return poly(L + R[::-1])


def vstroke_pts(pts, S, h, p=1.35, taper=(None, None), tz=0.16, tpow=0.9, smooth=0):
    """Variable-width pen along a sampled centreline (numeric tangents). smooth = half-window (samples) of a moving
    average on the width, so the weight flows along the stroke without lumps."""
    N = len(pts)
    L, R = [], []
    tang, ws = [], []
    for i in range(N):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, N - 1)]
        tx, ty = _u(b[0] - a[0], b[1] - a[1])
        tang.append((tx, ty))
        ws.append(h + (S - h) * abs(ty) ** p)
    if smooth:
        ws = [sum(ws[max(0, i - smooth):i + smooth + 1]) / len(ws[max(0, i - smooth):i + smooth + 1]) for i in range(N)]
    for i in range(N):
        tx, ty = tang[i]
        w = ws[i]
        f = i / (N - 1)
        if taper[0] is not None and f < tz:
            w = taper[0] + (w - taper[0]) * (f / tz) ** tpow
        if taper[1] is not None and f > 1 - tz:
            w = taper[1] + (w - taper[1]) * ((1 - f) / tz) ** tpow
        nx, ny = -ty, tx
        L.append((pts[i][0] + nx * w / 2, pts[i][1] + ny * w / 2))
        R.append((pts[i][0] - nx * w / 2, pts[i][1] - ny * w / 2))
    return poly(L + R[::-1])


def sarc(cx, cy, rx, ry, a0, a1, n=80, e=2.0 / 2.2):
    """Superellipse arc (exponent 2.5 ~ the k=0.60 bowls), angles in degrees, y-down (−90 = top)."""
    out = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        c, s_ = math.cos(t), math.sin(t)
        out.append((cx + rx * math.copysign(abs(c) ** e, c), cy + ry * math.copysign(abs(s_) ** e, s_)))
    return out


def _hseg(a, ta, b, tb, ka, kb):
    """cubic from a (unit tangent ta) to b (unit tangent tb), handle lengths ka, kb."""
    return (a, (a[0] + ta[0] * ka, a[1] + ta[1] * ka), (b[0] - tb[0] * kb, b[1] - tb[1] * kb), b)


def _u(dx, dy):
    L = math.hypot(dx, dy)
    return (dx / L, dy / L)


def g_S2(st, W=54, a=40.0, tip=0.55):
    """S: two superellipse arcs joined by the spine, drawn with the same pen as C (hairline top/bottom, weight on the
    sides and spine), terminals tapering like the leaf. One continuous centreline, so no seams or spurs."""
    H, S, h, o = st.H, st.S, st.h, st.o
    Sw = S * 0.98
    ym = H * 0.50
    rxu, ryu = W * 0.47 - Sw / 2, (ym + h * 0.15 + o * 0.5) / 2 - h / 2
    cxu, cyu = W * 0.49, (-o * 0.5 + ym + h * 0.15) / 2
    rxl, ryl = W * 0.50 - Sw / 2, (H + o * 0.5 - ym + h * 0.15) / 2 - h / 2
    cxl, cyl = W * 0.51, (ym - h * 0.15 + H + o * 0.5) / 2
    up = sarc(cxu, cyu, rxu, ryu, -a, -270 + 18, n=110)           # top-right terminal -> top -> left -> into spine
    lo = sarc(cxl, cyl, rxl, ryl, -90 + 18, 180 - a, n=110)       # out of spine -> right -> bottom -> bottom-left terminal
    # spine: a straight-ish bridge between the two arcs (cubic through the centre)
    a0, a1 = up[-1], lo[0]
    ta = _u(up[-1][0] - up[-2][0], up[-1][1] - up[-2][1])
    tb = _u(lo[1][0] - lo[0][0], lo[1][1] - lo[0][1])
    d = math.hypot(a1[0] - a0[0], a1[1] - a0[1])
    seg = _cubic_samples((a0, (a0[0] + ta[0] * d * 0.38, a0[1] + ta[1] * d * 0.38),
                          (a1[0] - tb[0] * d * 0.38, a1[1] - tb[1] * d * 0.38), a1), 40)
    pts = up + [q for q, _ in seg[1:-1]] + lo
    g = vstroke_pts(pts, Sw, h, taper=(h * tip, h * tip), tz=0.08)
    return I(g, rect(-3, -o - 1, W + 6, H + o + 1)), W


def g_C2(st, W=64, a=44.0, tip=0.55):
    """C: one superellipse stroke from top-right round the left to bottom-right; full weight on the left (vertical
    travel), hairline top and bottom, and both terminals taper like the leaf (thin, pointed)."""
    H, S, h, o = st.H, st.S, st.h, st.o
    Sw = S * 1.04
    rx, ry = W * 0.52 - Sw / 2, (H + o) / 2 - h / 2
    cx, cy = Sw / 2 + rx - 0.4, H / 2
    pts = sarc(cx, cy, rx, ry, -a, -360 + a, n=160)
    g = vstroke_pts(pts, Sw, h, taper=(h * tip, h * tip), tz=0.10)
    return I(g, rect(-3, -o - 1, W + 6, H + o + 1)), W


def g_C3(st, W=64, a=42.0):
    """C: the O ring opened by a radial wedge, so each terminal is cut towards the centre (an angled face that tapers
    with the ring, like the leaf), never a flat vertical cut."""
    H, o = st.H, st.o
    Wr = W * 1.10
    ring_o, ring_i, (cx, cy, rx, ry) = _ring(st, 0, Wr, -o * 0.6, H + o * 0.6, st.S * 1.04, st.h, st.h)
    ring = D(ring_o, ring_i)
    R = 400
    t0, t1 = math.radians(-a), math.radians(a)
    wedge = poly([(cx, cy), (cx + R * math.cos(t0), cy + R * math.sin(t0)), (cx + R, cy), (cx + R * math.cos(t1), cy + R * math.sin(t1))])
    g = D(ring, wedge)
    x1 = bbox(g)[2]
    return g, x1


def g_S3(st, W=50, sw=0.94, ym=0.49, te=(0.30, 0.22), tb=(0.30, 0.79), spine=(0.86, 0.50), k=0.56, smooth=14):
    """S: one continuous centreline (six G1 cubics) drawn with the contrast pen: hairline where it runs along the line
    and the baseline, full weight down the sides and the spine. Terminals end square to the stroke (angled faces)."""
    H, S, h, o = st.H, st.S, st.h, st.o
    Sw = S * sw
    yt, yb = h / 2 - o * 0.5, H - h / 2 + o * 0.5
    xl, xr = Sw / 2, W - Sw / 2
    yc = H * ym
    P0 = (W - 4.0, H * te[1]); t0 = _u(-te[0], -1.0)
    P1 = (W * 0.52, yt);       t1 = (-1.0, 0.0)
    P2 = (xl, (yt + yc) / 2 + 1.0); t2 = (0.0, 1.0)
    P3 = (W * 0.5, yc);        t3 = _u(*spine)
    P4 = (xr, (yc + yb) / 2 - 1.0); t4 = (0.0, 1.0)
    P5 = (W * 0.48, yb);       t5 = (-1.0, 0.0)
    P6 = (3.0, H * tb[1]);     t6 = _u(-tb[0], -1.0)
    def seg(a, ta, b, tbn):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        return _hseg(a, ta, b, tbn, d * k * 0.75, d * k * 0.75)
    segs = [seg(P0, t0, P1, t1), seg(P1, t1, P2, t2), seg(P2, t2, P3, t3), seg(P3, t3, P4, t4), seg(P4, t4, P5, t5),
            seg(P5, t5, P6, t6)]
    pts = []
    for i, sg in enumerate(segs):
        sm = [q for q, _ in _cubic_samples(sg, 60)]
        pts += sm if i == 0 else sm[1:]
    g = vstroke_pts(pts, Sw, h, smooth=smooth)
    return I(g, rect(-3, -o - 1, W + 3, H + o + 1)), W


def g_O2(st, W=78):
    H = st.H
    o, i, _ = _ring(st, 0, W, -st.o * 0.6, H + st.o * 0.6, st.S * 1.04, st.h, st.h)
    return D(o, i), W




def word(st, text, space, ovl=0.0, ovr=0.0, bar=False, build=None, widths=None, grid=None):
    """Like r3latin.wordmark but with a selectable glyph table (no line). grid: snap every letter origin to a multiple
    of `grid` units (pixel-fitting for a fixed size: grid = 100 / cap_px)."""
    build = build or CRE_BUILD
    x, prev, parts, spans = 0.0, None, [], []
    snap = (lambda v: round(v / grid) * grid) if grid else (lambda v: v)
    for ch in text:
        if ch == ' ':
            x += space.get(' ', 34.0)
            prev = None
            continue
        if prev is not None:
            x += space.get((prev, ch), 12.0)
        f = build[ch]
        g, w = f(st, W=widths[ch]) if widths and ch in widths else f(st)
        x = snap(x)
        parts.append(tr(g, 1, x, 0))
        spans.append((ch, x, x + w))
        x += w
        prev = ch
    return U(*parts), x, spans


CRE_BUILD = dict(BUILD)
CRE_BUILD.update({'S': lambda st, W=None: g_S3(st, smooth=22, k=0.5), 'C': g_C3, 'O': g_O2})
VAN_BUILD = dict(BUILD)
