"""VanIndra Hinge (final) — the type system. Every glyph is drawn here from cubic beziers and straight segments
(y-up design units, baseline 0). No font outlines are used in any deliverable.

Optical cuts:  DISPLAY (artwork >= 64 px tall)  and  SMALL (headers, Reel tags, anything smaller).
Terminals:     every free stroke end is a straight knife cut (no balls, no beaks). Head serifs are wedges,
               feet are bracketed slabs, capitals carry symmetric slabs.
The hinge:     the n of Van and the I of Indra are one stroke.
               - staircase()  : Van on line 1, Indra on line 2. The n's right leg drops straight into the I;
                                the slab where they meet is the n's foot and the I's head at once.
               - wordmark()   : one line, display only. The I rises behind the n's shoulder.
               - wordmark_text(): one line, small sizes. The ligature is released (n and I separate).
"""
import sys, math
from glyphkit import B, rect, poly, ellipse, U, D, T, vt, pathops, to_svg_d


class P:
    def __init__(s, **kw):
        s.X = 490; s.C = 700; s.A = 724; s.Itop = 724     # x-height, cap, ascender, one-line rising I (= ascender)
        s.S = 82; s.Sc = 90; s.H = 24                      # stems + hairline
        s.Ht = 29; s.Hb = 28; s.o = 11
        s.ft = 20; s.fe = 31; s.fb = 22                    # foot serif
        s.he = 35; s.hd = 30                               # head wedge
        s.ie = 31; s.it = 21                               # capital slab (extension now matches the feet)
        s.cw = 264                                         # n counter
        s.gap = 30                                         # one-line hinge cut (was 16)
        s.tw = 50                                          # knife-cut terminal: stroke thickness at the cut
        s.sh = 0.36                                        # knife-cut shear (tan of the cut angle, ~20 deg)
        s.__dict__.update(kw)


DISPLAY = dict()
SMALL = dict(S=90, Sc=96, H=34, Ht=38, Hb=36, ft=26, fe=30, fb=16, he=34, hd=34, ie=31, it=28, gap=52, cw=256,
             tw=56)


def dilate(path, g):
    q = pathops.Path(path)
    q.stroke(2 * g, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    q.convertConicsToQuads()
    return U(path, U(q))


def fillet(cx, cy, ux, uy, vx, vy, a, b):
    A = (cx + ux * a, cy + uy * a); Bp = (cx + vx * b, cy + vy * b)
    return B().M(*Bp).Q(cx, cy, *A).L(cx, cy).Z().path()


def foot(p, x0, x1, eL=None, eR=None):
    eL = p.fe if eL is None else eL; eR = p.fe if eR is None else eR
    t = p.ft; b = p.fb; parts = [rect(x0 - eL, 0, x1 + eR, t)]
    if eL > 0: parts.append(fillet(x0, t, -1, 0, 0, 1, min(b, eL * 0.8), b * 1.2))
    if eR > 0: parts.append(fillet(x1, t, 1, 0, 0, 1, min(b, eR * 0.8), b * 1.2))
    return U(*parts)


def head_wedge(p, x0, x1, top):
    e = p.he; d = p.hd
    tipT = (x0 - e, top - d + 9); tipB = (x0 - e, top - d - 2)
    b = B().M(*tipB).L(*tipT).L(x1, top + 2).L(x1, top - 120).L(x0, top - 120).L(x0, top - d - 2 - p.fb * 1.4)
    b.Q(x0, top - d - 2, *tipB)
    return b.Z().path()


def cap_slab(p, x0, x1, y, up=True, eL=None, eR=None):
    eL = p.ie if eL is None else eL; eR = p.ie if eR is None else eR
    t = p.it; b = p.fb * 1.05
    if up:
        yb = y - t
        return U(rect(x0 - eL, yb, x1 + eR, y), fillet(x0, yb, -1, 0, 0, -1, min(b, eL * .8), b * 1.25),
                 fillet(x1, yb, 1, 0, 0, -1, min(b, eR * .8), b * 1.25))
    yb = y + t
    return U(rect(x0 - eL, y, x1 + eR, yb), fillet(x0, yb, -1, 0, 0, 1, min(b, eL * .8), b * 1.25),
             fillet(x1, yb, 1, 0, 0, 1, min(b, eR * .8), b * 1.25))


def shared_slab(p, x0, x1, y=0.0):
    """One slab, two serifs: the foot of the n (bracketed upward) and the head of the I (bracketed downward)."""
    e = p.ie; t = p.it; b = p.fb * 1.05
    return U(rect(x0 - e, y, x1 + e, y + t),
             fillet(x0, y + t, -1, 0, 0, 1, min(b, e * .8), b * 1.2), fillet(x1, y + t, 1, 0, 0, 1, min(b, e * .8), b * 1.2),
             fillet(x0, y, -1, 0, 0, -1, min(b, e * .8), b * 1.25), fillet(x1, y, 1, 0, 0, -1, min(b, e * .8), b * 1.25))


def halfplane(P0, P1, side=1, far=4000):
    """polygon covering everything on one side of the line P0->P1 (side=+1: left of the direction, -1: right)."""
    dx, dy = P1[0] - P0[0], P1[1] - P0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    nx, ny = -uy * side, ux * side
    A = (P0[0] - ux * far, P0[1] - uy * far); Bq = (P1[0] + ux * far, P1[1] + uy * far)
    return poly([A, Bq, (Bq[0] + nx * far, Bq[1] + ny * far), (A[0] + nx * far, A[1] + ny * far)])


# ------------------------------------------------------------------ n arch pieces
def arch_outer_to_apex(b, p, xs, w, notch, apex_k=0.44):
    X = p.X; o = p.o; N = (xs, X * notch); ax = xs + w * apex_k
    b.M(xs - 3, N[1] - 40).L(*N)
    b.C(N[0] + w * 0.10, N[1] + (X + o - N[1]) * 0.58, ax - w * 0.27, X + o, ax, X + o)
    return ax


def arch_inner(b, p, xs, xl, w, crotch, yi):
    X = p.X; it = X - p.Ht; ix = xs + w * 0.42
    b.L(xl, yi)
    b.C(xl, yi + (it - yi) * 0.62, ix + (xl - ix) * 0.56, it, ix, it)
    b.C(ix - (ix - xs) * 0.52, it, xs + w * 0.05, X * crotch + (it - X * crotch) * 0.50, xs, X * crotch)
    b.L(xs - 3, X * crotch - 40)
    return b


def n_arch(p, x0, cw, Sr=None):
    S = p.S; X = p.X; o = p.o; Sr = Sr or S
    xs = x0 + S; xl = xs + cw; xr = xl + Sr
    b = B(); ax = arch_outer_to_apex(b, p, xs, cw, 0.80)
    yR = X * 0.64
    b.C(ax + (xr - ax) * 0.60, X + o, xr, yR + (X + o - yR) * 0.60, xr, yR)
    b.L(xr, X * 0.3).L(xl, X * 0.3)
    arch_inner(b, p, xs, xl, cw, 0.64, X * 0.58)
    return b.Z().path(), xs, xl, xr


def n_left(p, x0):
    S = p.S; X = p.X
    return U(rect(x0, 0, x0 + S, X - 60), head_wedge(p, x0, x0 + S, X), foot(p, x0, x0 + S))


def g_n(p, lsb=22, rsb=22):
    x0 = lsb + p.fe
    arch, xs, xl, xr = n_arch(p, x0, p.cw)
    return U(n_left(p, x0), arch, rect(xl, 0, xr, p.X * 0.66), foot(p, xl, xr)), xr + p.fe + rsb


def g_hinge(p, lsb=22, rsb=34, gap=None):
    """ONE-LINE HINGE (display only): a complete n whose right leg is also the stem of a capital I.
    The I rises behind the n's shoulder, separated by a cut that follows the shoulder. -> (n_part, I_part, adv)"""
    S = p.S; X = p.X; gap = p.gap if gap is None else gap
    x0 = lsb + p.fe
    arch, xs, xl, xr = n_arch(p, x0, p.cw)
    leg = U(rect(xl, 0, xr, X * 0.66), cap_slab(p, xl, xr, 0, False))
    n_part = U(n_left(p, x0), arch, leg)
    shoulder = U(arch, rect(xl, X * 0.30, xr, X * 0.66))
    I_full = U(rect(xl, X * 0.3, xr, p.Itop), cap_slab(p, xl, xr, p.Itop, True))
    I_part = D(I_full, dilate(shoulder, gap)) if gap > 0 else D(I_full, n_part)
    return n_part, I_part, xr + p.ie + rsb


def g_hinge_down(p, L, lsb=22, rsb=34):
    """STAIRCASE HINGE: the n's right leg drops straight down into the I of the next line.
    L = baseline-to-baseline distance. -> (n_part above the shared slab, I_part = shared slab + I, adv)"""
    S = p.S; X = p.X; x0 = lsb + p.fe; t = p.it
    arch, xs, xl, xr = n_arch(p, x0, p.cw)
    n_part = U(n_left(p, x0), arch, rect(xl, t, xr, X * 0.66))
    n_part = D(n_part, rect(xl - 300, -3000, xr + 300, t))
    I_part = U(shared_slab(p, xl, xr, 0), rect(xl, -L + t, xr, 0), cap_slab(p, xl, xr, -L, False))
    return n_part, I_part, xr + p.ie + rsb, (xl, xr)


def g_I(p, lsb=20, rsb=20, top=None):
    top = p.A if top is None else top
    x0 = lsb + p.ie; x1 = x0 + p.Sc
    return U(rect(x0, 0, x1, top), cap_slab(p, x0, x1, top, True), cap_slab(p, x0, x1, 0, False)), x1 + p.ie + rsb


# ------------------------------------------------------------------ V (and lowercase v/y body)
def _vee(p, H, W, thick, thin, eo, ei, ro, ri, t, lsb, apex_flat=10):
    o = p.o
    ax = lsb + eo + W / 2; lx0 = ax - W / 2; rx1 = ax + W / 2; apex = (ax, -o)
    thl = math.atan2(H + o, ax - lx0); thr = math.atan2(H + o, rx1 - ax)
    wl = thick / math.sin(thl); wr = thin / math.sin(thr)

    def inter(p1, d1, p2, d2):
        det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])
        tt = ((p2[0] - p1[0]) * (-d2[1]) - (p2[1] - p1[1]) * (-d2[0])) / det
        return (p1[0] + tt * d1[0], p1[1] + tt * d1[1])
    dl = (apex[0] - lx0, apex[1] - H); dr = (apex[0] - rx1, apex[1] - H)
    Ii = inter((lx0 + wl, H), dl, (rx1 - wr, H), dr)
    body = D(poly([(lx0, H), (lx0 + wl, H), Ii, (rx1 - wr, H), (rx1, H), apex]), rect(-500, -300, 3000, -o + apex_flat))
    yb = H - t

    def unit(v):
        L = math.hypot(*v); return (v[0] / L, v[1] / L)
    ul = unit(dl); ur = unit(dr)
    xl_out = lx0 + ul[0] * ((yb - H) / ul[1]); xl_in = xl_out + wl
    xr_out = rx1 + ur[0] * ((yb - H) / ur[1]); xr_in = xr_out - wr
    fb = p.fb * 1.1
    parts = [body, rect(lx0 - eo, yb, lx0 + wl + ei, H), rect(rx1 - wr - ri, yb, rx1 + ro, H),
             fillet(xl_out, yb, -1, 0, ul[0], ul[1], min(fb, eo * .8), fb * 1.4), fillet(xl_in, yb, 1, 0, ul[0], ul[1], min(fb, ei * .8), fb * 1.2),
             fillet(xr_in, yb, -1, 0, ur[0], ur[1], min(fb, ri * .8), fb * 1.2), fillet(xr_out, yb, 1, 0, ur[0], ur[1], min(fb, ro * .8), fb * 1.4)]
    return U(*parts), dict(ax=ax, lx0=lx0, rx1=rx1, wr=wr, dr=dr, apex=apex)


def g_V(p, lsb=8, rsb=0, W=596):
    inner = max(24, p.it * 0.5 + 14)                  # inner serif must outrun the slanted stroke under a thick slab
    g, info = _vee(p, p.C, W, p.Sc * 1.06, p.H * 1.15, 40, inner, 34, inner + 2, p.it, lsb - 4)
    return g, info['rx1'] + 34 + rsb


def g_y(p, lsb=10, rsb=10, W=392):
    """lowercase y: thick left diagonal, hairline right diagonal that runs on below the baseline and ends in a cut."""
    X = p.X; thin = p.H * 1.25
    v, info = _vee(p, X, W, p.S * 1.0, thin, 30, 18, 26, 18, p.ft, lsb)
    rx1, wr, dr = info['rx1'], info['wr'], info['dr']
    L = math.hypot(*dr); ux, uy = dr[0] / L, dr[1] / L
    # tail: continue the hairline's centre line below the baseline, then turn left into a knife-cut terminal
    cx_top = rx1 - wr / 2
    xat = lambda y: cx_top + ux * (y - X) / uy
    depth = 205; w0 = thin * 1.12; w1 = p.tw * 0.92
    y0 = X * 0.30; y1 = -depth * 0.55
    xe = xat(y1) - 70                                       # terminal x (left of the stroke)
    tail = B().M(xat(y0) - w0 / 2, y0).L(xat(y0) + w0 / 2, y0)
    tail.L(xat(y1) + w0 / 2, y1)
    tail.C(xat(y1) + w0 / 2 - 14, -depth * 0.86, xe + 40, -depth, xe, -depth)
    tail.L(xe - w1 * p.sh, -depth + w1)
    tail.C(xe + 22, -depth + w1 - 2, xat(y1) - w0 / 2 - 8, -depth * 0.72, xat(y1) - w0 / 2, y1 + 6)
    tail.L(xat(y0) - w0 / 2, y0)
    return U(v, tail.Z().path()), rx1 + 26 + rsb


# ------------------------------------------------------------------ a (knife-cut terminal)
def g_a(p, lsb=30, rsb=16, w=328):
    S = p.S * 0.97; X = p.X; o = p.o; H = p.H
    la = lsb; sr = la + w; sl = sr - S
    hx = la + (sr - la) * 0.50
    tw = p.tw; iy = X - p.Ht
    To = (la + 6, X * 0.70)                          # outer end of the cut (lower-left)
    Ti = (la + 6 + tw, X * 0.70 + tw * p.sh)         # inner end: the cut rises to the right
    hk = B().M(sr, X * 0.55).L(sr, X * 0.66)
    hk.C(sr, X * 0.66 + (X + o - X * 0.66) * 0.60, hx + (sr - hx) * 0.55, X + o, hx, X + o)
    hk.C(hx - (hx - To[0]) * 0.62, X + o, To[0], To[1] + (X + o - To[1]) * 0.50, To[0], To[1])
    hk.L(*Ti)
    hk.C(Ti[0], Ti[1] + (iy - Ti[1]) * 0.55, hx - (hx - Ti[0]) * 0.45, iy, hx + 4, iy)
    hk.C(hx + (sl - hx) * 0.62, iy, sl, X * 0.74, sl, X * 0.62)
    hk.L(sl, X * 0.55)
    tO = X * 0.585; tI = tO - H * 1.12; bx = la + (sl - la) * 0.50
    bo = B().M(sl + 14, tO)
    bo.C(sl - 50, tO, la, X * 0.47, la, X * 0.27)
    bo.C(la, X * 0.09, la + 48, -o, bx - 6, -o)
    bo.C(bx + 60, -o, sl - 14, X * 0.04, sl + 14, X * 0.14)
    bo.Z()
    li = la + S * 1.04
    ci = B().M(sl, tI)
    ci.C(sl - 46, tI, li, X * 0.45, li, X * 0.29)
    ci.C(li, X * 0.14, li + 26, p.Hb, li + 74, p.Hb)
    ci.C(li + 126, p.Hb, sl, X * 0.12, sl, X * 0.24)
    ci.Z()
    bowl = D(bo.path(), ci.path())
    stem = rect(sl, 0, sr, X * 0.62)
    spur = U(rect(sl, 0, sr + 22, p.ft), fillet(sr, p.ft, 1, 0, 0, 1, 18, p.fb * 1.2))
    return U(hk.Z().path(), bowl, stem, spur), sr + 22 + rsb


# ------------------------------------------------------------------ d / b
def _d_parts(p, lsb, w):
    S = p.S; X = p.X; o = p.o; A = p.A
    ld = lsb; sr = ld + w; sl = sr - S; bx = ld + (sl - ld) * 0.52
    ou = B().M(sl + 12, X * 0.84)
    ou.C(sl - 34, X + o - 4, bx + 60, X + o, bx, X + o)
    ou.C(bx - 82, X + o, ld, X * 0.76, ld, X * 0.475)
    ou.C(ld, X * 0.18, ld + 70, -o, bx, -o)
    ou.C(bx + 70, -o, sl - 20, X * 0.05, sl + 12, X * 0.14)
    ou.Z()
    li = ld + S * 1.06
    ci = B().M(sl, X * 0.80)
    ci.C(sl - 24, X - p.Ht - 2, bx + 56, X - p.Ht, bx + 6, X - p.Ht)
    ci.C(bx - 62, X - p.Ht, li, X * 0.70, li, X * 0.475)
    ci.C(li, X * 0.22, li + 40, p.Hb, bx + 10, p.Hb)
    ci.C(bx + 66, p.Hb, sl - 6, X * 0.12, sl, X * 0.22)
    ci.Z()
    bowl = D(ou.path(), ci.path())
    spur = U(rect(sl, 0, sr + 24, p.ft), fillet(sr, p.ft, 1, 0, 0, 1, 18, p.fb * 1.2))
    return bowl, spur, sl, sr


def g_d(p, lsb=26, rsb=20, w=356):
    bowl, spur, sl, sr = _d_parts(p, lsb, w)
    stem = U(rect(sl, 0, sr, p.A - 60), head_wedge(p, sl, sr, p.A))
    return U(bowl, stem, spur), sr + 24 + rsb


def g_b(p, lsb=20, rsb=26, w=356):
    """b = the d's bowl mirrored onto a left stem with a left-pointing head wedge and a left spur."""
    bowl, spur, sl, sr = _d_parts(p, 0, w)
    m = lambda q: T(q, 0, 0, -1, 1)
    bowl = m(bowl); spur = m(spur)
    x0, x1 = -sr, -sl
    stem = U(rect(x0, 0, x1, p.A - 60), head_wedge(p, x0, x1, p.A))
    g = U(bowl, stem, spur)
    bx0 = vt.bounds(g)[0]
    return T(g, lsb - bx0, 0), (0 - bx0) + lsb + rsb


# ------------------------------------------------------------------ r (knife-cut ear)
def g_r(p, lsb=22, rsb=8):
    S = p.S; X = p.X; o = p.o
    x0 = lsb + p.fe; xs = x0 + S
    ex = xs + 86; tx = xs + 160
    tw = p.tw * 0.86
    To = (tx, X * 0.93)                               # top end of the cut
    Ti = (tx - tw * p.sh, X * 0.93 - tw)              # bottom end: the cut leans right
    e = B().M(xs - 3, X * 0.66).L(xs, X * 0.72)
    e.C(xs + 16, X * 0.72 + (X + o - X * 0.72) * 0.62, ex - 44, X + o, ex, X + o)
    e.C(ex + 40, X + o, tx - 8, X + o - 6, *To)
    e.L(*Ti)
    e.C(Ti[0] - 16, X - p.Ht - 2, ex + 20, X - p.Ht, ex - 6, X - p.Ht)
    e.C(ex - 46, X - p.Ht, xs + 10, X * 0.70, xs, X * 0.58)
    e.L(xs - 3, X * 0.54)
    parts = [rect(x0, 0, xs, X - 60), head_wedge(p, x0, xs, X), foot(p, x0, xs, p.fe, p.fe + 16), e.Z().path()]
    return U(*parts), tx + rsb


# ------------------------------------------------------------------ o / e / C / t / i / s  (for "Creations", "edit by")
def ring(cx, cy, rxo, ryo, rxi, ryi, tilt=-7, ko=0.57, ki=0.555):
    outer = ellipse(cx, cy, rxo, ryo, ko)
    inner = ellipse(0, 0, rxi, ryi, ki)
    a = math.radians(tilt); c, s = math.cos(a), math.sin(a)
    inner = vt.transform(inner, c, s, -s, c, cx, cy)
    return D(outer, inner)


def g_o(p, lsb=26, rsb=26, w=448):
    X = p.X; o = p.o; rx = w / 2; ry = X / 2 + o
    cx = lsb + rx
    return ring(cx, X / 2, rx, ry, rx - p.S * 1.05, ry - p.Ht), lsb + w + rsb


def g_e(p, lsb=26, rsb=18, w=414):
    X = p.X; o = p.o; rx = w / 2; ry = X / 2 + o; cx = lsb + rx; cy = X / 2
    rg = ring(cx, cy, rx, ry, rx - p.S * 1.0, ry - p.Ht * 0.95)
    bar_y0 = X * 0.50; bar_y1 = bar_y0 + p.Ht * 0.92
    cut = poly([(cx + rx * 0.05, bar_y0), (cx + rx + 40, bar_y0), (cx + rx + 40, X * 0.30), (cx + rx * 0.05, X * 0.19)])
    body = D(rg, cut)
    bar = rect(cx - rx + p.S * 0.6, bar_y0, cx + rx - 2, bar_y1)
    return U(body, bar), lsb + w + rsb


def g_C(p, lsb=34, rsb=20, w=584):
    C = p.C; o = p.o; rx = w / 2; ry = C / 2 + o; cx = lsb + rx; cy = C / 2
    rg = ring(cx, cy, rx, ry, rx - p.Sc * 1.08, ry - p.H * 1.3, tilt=-6)
    # opening: two knife cuts leaning right (same shear as every other terminal), plus the mouth
    xt = cx + rx * 0.78; xb = cx + rx * 0.84; k = 70 * p.sh
    cut = D(halfplane((xt - k, cy + C * 0.28), (xt + k * 0.4, cy + ry + 40), side=-1), rect(-4000, -4000, 4000, cy - 2))
    cut2 = D(halfplane((xb - k * 0.4, cy - ry - 40), (xb + k, cy - C * 0.28), side=-1), rect(-4000, cy + 2, 4000, 4000))
    mouth = rect(cx + rx * 0.40, cy - C * 0.215, cx + rx + 400, cy + C * 0.205)
    return D(rg, U(cut, cut2, mouth)), lsb + w + rsb


def g_t(p, lsb=14, rsb=10):
    """t: the stem top is one knife cut (no flag); the bar sits mostly to the right."""
    S = p.S * 0.95; X = p.X; o = p.o
    x0 = lsb + 46; x1 = x0 + S
    stem = B().M(x0, X * 1.05).L(x1, X * 1.05 + S * p.sh * 1.6).L(x1, X * 0.20)
    stem.C(x1, X * 0.09, x1 + 20, X * 0.06, x1 + 46, X * 0.06)
    stem.C(x1 + 76, X * 0.06, x1 + 96, X * 0.12, x1 + 110, X * 0.19)
    stem.L(x1 + 128, X * 0.16)
    stem.C(x1 + 108, X * 0.04, x1 + 70, -o, x1 + 18, -o)
    stem.C(x0 + 16, -o, x0, X * 0.06, x0, X * 0.22)
    stem.Z()
    bar = rect(x0 - 40, X - p.Ht, x1 + 104, X)
    return U(stem.path(), bar), x1 + 128 + rsb


def g_i(p, lsb=22, rsb=22):
    S = p.S; X = p.X; x0 = lsb + p.fe
    dot = ellipse(x0 + S / 2 + 4, X + 150, S * 0.56, S * 0.56)
    return U(rect(x0, 0, x0 + S, X - 60), head_wedge(p, x0, x0 + S, X), foot(p, x0, x0 + S), dot), x0 + S + p.fe + rsb


def expand(segs, wfun, n=48):
    """pointed-pen expansion along cubic spine segments; returns filled path."""
    L = []; R = []
    tot = len(segs)
    for si, (p0, p1, p2, p3) in enumerate(segs):
        for k in range(n + 1):
            if si > 0 and k == 0: continue
            t = k / n; mt = 1 - t
            x = mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0]
            y = mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1]
            dx = 3 * mt * mt * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
            dy = 3 * mt * mt * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
            l = math.hypot(dx, dy) or 1; tx, ty = dx / l, dy / l
            w = wfun((si + t) / tot, tx, ty)
            nx, ny = -ty, tx
            L.append((x + nx * w / 2, y + ny * w / 2)); R.append((x - nx * w / 2, y - ny * w / 2))
    pts = L + R[::-1]
    return poly(pts)


def g_s(p, lsb=26, rsb=20, w=318):
    """s: pen-expanded spine; both ends are knife cuts (lighter than before, no blunt slabs)."""
    X = p.X; o = p.o; S = p.S; H = p.H
    x0 = lsb; x1 = lsb + w
    ht = p.Ht; hb = p.Hb
    yt = X + o - ht / 2; yb = -o + hb / 2
    segs = [
        ((x1 - 30, X * 0.66), (x1 - 26, X * 0.93), (x1 - 90, yt), (x0 + w * 0.50, yt)),
        ((x0 + w * 0.50, yt), (x0 + w * 0.16, yt), (x0 + S * 0.50, X * 0.90), (x0 + S * 0.52, X * 0.72)),
        ((x0 + S * 0.52, X * 0.72), (x0 + S * 0.56, X * 0.50), (x1 - S * 0.56, X * 0.50), (x1 - S * 0.52, X * 0.27)),
        ((x1 - S * 0.52, X * 0.27), (x1 - S * 0.50, X * 0.08), (x0 + w * 0.84, yb), (x0 + w * 0.50, yb)),
        ((x0 + w * 0.50, yb), (x0 + w * 0.20, yb), (x0 + 22, X * 0.10), (x0 + 22, X * 0.34)),
    ]
    te = p.tw * 0.80
    keys = [(0.0, te), (0.10, te * 0.72), (0.20, ht), (0.30, 0.55 * S), (0.42, 0.92 * S), (0.50, 1.0 * S), (0.58, 0.92 * S),
            (0.70, 0.55 * S), (0.80, hb), (0.90, te * 0.72), (1.0, te)]

    def wf(u, tx, ty):
        ks = [keys[0]] + keys + [keys[-1]]
        for i in range(1, len(ks) - 2):
            (u0, w0), (u1, w1), (u2, w2), (u3, w3) = ks[i - 1], ks[i], ks[i + 1], ks[i + 2]
            if u <= u2:
                t = (u - u1) / (u2 - u1) if u2 > u1 else 0
                m1 = (w2 - w0) / 2; m2 = (w3 - w1) / 2
                h00 = 2 * t ** 3 - 3 * t * t + 1; h10 = t ** 3 - 2 * t * t + t; h01 = -2 * t ** 3 + 3 * t * t; h11 = t ** 3 - t * t
                return h00 * w1 + h10 * m1 + h01 * w2 + h11 * m2
        return keys[-1][1]
    body = expand(segs, wf, 60)
    # knife cuts: top terminal (cut rises to the right), bottom terminal (same direction)
    yc1 = X * 0.70; yc2 = X * 0.30
    c1 = halfplane((x1 - 120, yc1 - 120 * p.sh), (x1 + 60, yc1 + 60 * p.sh), side=-1)
    c1 = D(c1, U(rect(-4000, -4000, x1 - 78, 4000), rect(-4000, -4000, 4000, X * 0.58), rect(-4000, X * 0.88, 4000, 4000)))
    c2 = halfplane((x0 - 60, yc2 - 60 * p.sh), (x0 + 120, yc2 + 120 * p.sh), side=1)
    c2 = D(c2, U(rect(x0 + 78, -4000, 4000, 4000), rect(-4000, -4000, 4000, X * 0.12), rect(-4000, X * 0.44, 4000, 4000)))
    return D(body, U(c1, c2)), x1 + rsb


def place(items):
    out = []; x = 0
    for (pth, adv, kern) in items:
        x += kern; out.append(T(pth, x, 0)); x += adv
    return U(*out), x


# ------------------------------------------------------------------ words
KERN = dict(Va=-78, an=0, In=-32, nd=-6, dr=-6, ra=-46)


def wordmark(p):
    """ONE-LINE HINGE (display only). -> dict(ink, I, width): ink = everything except the rising I."""
    V_, vw = g_V(p); a, aw = g_a(p); n, nw = g_n(p); d, dw = g_d(p); r, rw = g_r(p)
    np_, ip_, hw = g_hinge(p)
    items = [(V_, vw, 0), (a, aw, KERN['Va']), (np_, hw, KERN['an']), (n, nw, KERN['In']), (d, dw, KERN['nd']), (r, rw, KERN['dr']), (a, aw, KERN['ra'])]
    ink, width = place(items)
    off = vw + aw + KERN['Va'] + KERN['an']
    return dict(ink=ink, I=T(ip_, off, 0), width=width)


def wordmark_text(p, I_top=None):
    """ONE-LINE TEXT CUT (small sizes): the ligature is released, n and I stand apart, I at ascender height."""
    V_, vw = g_V(p); a, aw = g_a(p); n, nw = g_n(p); d, dw = g_d(p); r, rw = g_r(p)
    Ig, Iw = g_I(p, lsb=4, rsb=0, top=I_top)
    x = 0; ink = []
    for g, adv, k in [(V_, vw, 0), (a, aw, KERN['Va']), (n, nw, 0)]:
        x += k; ink.append(T(g, x, 0)); x += adv
    x += 6; Ip = T(Ig, x, 0); x += Iw + 30
    for g, adv, k in [(n, nw, -6), (d, dw, KERN['nd']), (r, rw, KERN['dr']), (a, aw, KERN['ra'])]:
        x += k; ink.append(T(g, x, 0)); x += adv
    return dict(ink=U(*ink), I=Ip, width=x)


def staircase(p, L=None):
    """THE STAIRCASE: Van on line 1, Indra on line 2, joined by one stroke.
    -> dict(van = V a + the n above the shared slab, I = shared slab + I, indra = n d r a of line 2)"""
    L = (p.A - p.it) if L is None else L               # the I is exactly ascender-tall: A = L + slab
    V_, vw = g_V(p); a, aw = g_a(p); n, nw = g_n(p); d, dw = g_d(p); r, rw = g_r(p)
    hn, hI, hw, (xl, xr) = g_hinge_down(p, L)
    x = 0; van = []
    van.append(T(V_, x, 0)); x += vw + KERN['Va']
    van.append(T(a, x, 0)); x += aw + KERN['an']
    van.append(T(hn, x, 0)); I = T(hI, x, 0); stem = (x + xl, x + xr); x += hw + KERN['In']
    indra = []
    for g, adv, k in [(n, nw, KERN['nd']), (d, dw, KERN['dr']), (r, rw, KERN['ra']), (a, aw, 0)]:
        indra.append(T(g, x, -L)); x += adv + k
    return dict(van=U(*van), I=I, indra=U(*indra), L=L, stem=stem)


CR_KERN = dict(Cr=-30, re=-8, ea=-14, at=-10, ti=-14, io=-12, on=-6, ns=14)


def creations(p, track=0):
    C_, cw_ = g_C(p); r, rw = g_r(p); e, ew = g_e(p); a, aw = g_a(p); t, tw = g_t(p); i, iw = g_i(p); o_, ow = g_o(p); n, nw = g_n(p); s, sw = g_s(p)
    k = CR_KERN
    items = [(C_, cw_, 0), (r, rw, k['Cr'] + track), (e, ew, k['re'] + track), (a, aw, k['ea'] + track), (t, tw, k['at'] + track),
             (i, iw, k['ti'] + track), (o_, ow, k['io'] + track), (n, nw, k['on'] + track), (s, sw, k['ns'] + track)]
    ink, width = place(items)
    return dict(ink=ink, width=width)


def edit_by(p):
    """'edit by' in the same system (for the Reel credit)."""
    e, ew = g_e(p); d, dw = g_d(p); i, iw = g_i(p); t, tw = g_t(p); b, bw = g_b(p); y, yw = g_y(p)
    items = [(e, ew, 0), (d, dw, -10), (i, iw, -14), (t, tw, -12), (b, bw, 150), (y, yw, -20)]
    ink, width = place(items)
    return dict(ink=ink, width=width)


def hinge_mark(p, gap=None):
    np_, ip_, hw = g_hinge(p, gap=gap)
    return dict(n=np_, I=ip_, width=hw)
