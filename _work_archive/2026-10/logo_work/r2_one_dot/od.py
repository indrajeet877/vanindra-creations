"""One Dot: a parametric bilingual (Latin lowercase + Devanagari) lettering engine.

All glyphs are built in a y-UP design space (baseline y=0, Latin x-height y=X,
Devanagari headline top y=H) from a handful of primitives (stems, squircle rings,
asymmetric arches, straight wedges, one circle) and boolean-unioned with
skia-pathops.  `place()` scales + flips to SVG y-down at output.

System rules shared by both scripts:
  * verticals = S (stem / danda), horizontals = T (thin), rounds = S * Rk
  * tops are flat and sit on one line (Latin x-height = an implied headline;
    Devanagari = the drawn shirorekha); bottoms are round (bowls hang)
  * one arch: it leaves a stem with a square shoulder and lands with a round one
    (Latin n / r; the Devanagari i-matra and the na shoulder are the same arch)
  * one bowl: Latin a / d and Devanagari va share it
  * diagonals: down-right strokes heavy, down-left strokes light (Latin v; ra legs)
  * exactly one circle: the dot (Latin i tittle / Devanagari anusvara), same
    diameter and same gap above the line in both scripts.
"""
import math
import sys

sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import pathops  # noqa: E402
from vtype import union, difference, intersection, to_d, transform, bounds, svg_doc, PALETTE  # noqa: E402,F401

KC = 0.5523  # circle handle factor

# ----------------------------------------------------------------- primitives

def rect(x0, y0, x1, y1):
    p = pathops.Path()
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p


def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return union(p)


def squircle(x0, y0, x1, y1, k=0.62, ktl=None, ktr=None, kbl=None, kbr=None):
    """Closed rounded box from 4 cubic quadrants. k: handle factor (0.5523 = ellipse,
    -> 1 = square). Per-corner override. y-up."""
    ktl = k if ktl is None else ktl
    ktr = k if ktr is None else ktr
    kbl = k if kbl is None else kbl
    kbr = k if kbr is None else kbr
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2, (y1 - y0) / 2
    p = pathops.Path()
    p.moveTo(cx + a, cy)
    p.cubicTo(cx + a, cy - kbr * b, cx + kbr * a, cy - b, cx, cy - b)
    p.cubicTo(cx - kbl * a, cy - b, cx - a, cy - kbl * b, cx - a, cy)
    p.cubicTo(cx - a, cy + ktl * b, cx - ktl * a, cy + b, cx, cy + b)
    p.cubicTo(cx + ktr * a, cy + b, cx + a, cy + ktr * b, cx + a, cy)
    p.close()
    return union(p)


def circle(cx, cy, r):
    return squircle(cx - r, cy - r, cx + r, cy + r, k=KC)


def clip(p, x0=-1e5, y0=-1e5, x1=1e5, y1=1e5):
    return intersection(p, rect(x0, y0, x1, y1))


def cut(p, x0=-1e5, y0=-1e5, x1=1e5, y1=1e5):
    return difference(p, rect(x0, y0, x1, y1))


def shift(p, dx, dy=0.0):
    return transform(p, 1, 0, 0, 1, dx, dy)


def place(p, s, dx, dy):
    """scale a y-up path by s, flip to SVG y-down, translate."""
    return transform(p, s, 0, 0, -s, dx, dy)


def stroke_line(x0, y0, x1, y1, w0, w1=None):
    """Straight stroke whose HORIZONTAL width is w0 at (x0,y0) and w1 at (x1,y1); ends cut level."""
    w1 = w0 if w1 is None else w1
    return poly([(x0 - w0 / 2, y0), (x0 + w0 / 2, y0), (x1 + w1 / 2, y1), (x1 - w1 / 2, y1)])


def arch_region(x0, xa, x1, top, base, kL, kR, ext=0.0):
    """Region under an asymmetric arch: left foot (x0,base) -> apex (xa,top) -> right foot (x1,base)."""
    p = pathops.Path()
    h = top - base
    p.moveTo(x0, base - ext)
    p.lineTo(x0, base)
    if kL >= 0.97:
        p.lineTo(x0, top)
        p.lineTo(xa, top)
    else:
        p.cubicTo(x0, base + kL * h, xa - kL * (xa - x0), top, xa, top)
    if kR >= 0.97:
        p.lineTo(x1, top)
        p.lineTo(x1, base)
    else:
        p.cubicTo(xa + kR * (x1 - xa), top, x1, base + kR * h, x1, base)
    p.lineTo(x1, base - ext)
    p.close()
    return union(p)


def arch2(x0, x1, top, base, SL, SR, T, apex=0.5, kL=0.8, kR=0.8, kinL=None, kinR=None, drop=40.0):
    """Arch band from x0..x1 (outer), top at `top`, legs down to `base`.
    SL/SR: left/right leg thickness (horizontal), T: thickness at the apex."""
    kinL = kL if kinL is None else kinL
    kinR = kR if kinR is None else kinR
    xa = x0 + apex * (x1 - x0)
    ix0, ix1 = x0 + SL, x1 - SR
    xai = ix0 + apex * (ix1 - ix0)
    outer = arch_region(x0, xa, x1, top, base, kL, kR, ext=60)
    inner = arch_region(ix0, xai, ix1, top - T, base, kinL, kinR, ext=80)
    return clip(difference(outer, inner), y0=base - drop)


# ----------------------------------------------------------------- parameters

class P:
    """Design parameters (units: Latin x-height X = 500)."""

    def __init__(self, **kw):
        self.X = 500.0
        self.S = 90.0          # stem
        self.T = 56.0          # thin (horizontal)
        self.Rk = 1.05         # round side weight factor
        self.ktop = 0.80       # flat tops (outer)
        self.kbot = 0.58       # round bottoms (outer)
        self.kin_top = 0.80
        self.kin_bot = 0.60
        self.o = 9.0           # overshoot for round bottoms
        self.nW = 390.0        # n outer width
        self.aW = 400.0        # a bowl+stem width
        self.vW = 390.0
        self.rW = 245.0
        self.asc = 730.0       # d ascender height
        self.spring = 0.40     # where the arch meets the right leg (x X)
        self.apex = 0.55       # arch apex position
        self.kAL = 0.97        # arch outer left (square shoulder)
        self.kAR = 0.80        # arch outer right
        self.kAiL = 0.92       # arch inner left
        self.kAiR = 0.78       # arch inner right
        self.dotD = 104.0      # dot diameter
        self.dotGap = 62.0     # gap between line and dot
        self.dot_shape = 'circle'
        self.vflat = 34.0      # flat at v vertex
        self.vthin = None      # thin diagonal width (horizontal), default T*1.25
        self.vthick = None     # thick diagonal width (horizontal), default S*1.12
        self.sb = 48.0         # sidebearing straight
        self.sbr = 30.0        # sidebearing round
        self.sbd = 8.0         # sidebearing diagonal
        self.sbf = 4.0         # sidebearing flag (r)
        self.term_angle = 0.0  # stem foot cut angle (deg) 0 = flat
        self.kern = {}
        self.a_story = 1
        self.bowl_ktr = None   # a/d/va bowl outer top-right k (None = ktop)
        self.oW = 420.0
        self.space = 230.0
        self.cW = 420.0
        self.c_top_cut = 120.0
        self.c_bot_cut = 105.0
        self.e_bar = 0.50
        self.tW = 250.0
        self.t_h = 1.22
        self.sW = 340.0
        self.s_spine = 0.86
        # Devanagari
        self.H = 600.0         # headline top
        self.Th = 60.0         # headline thickness
        self.hl_over = 34.0    # headline overhang left
        self.hl_over_r = 14.0  # headline overhang right
        self.dS = None         # danda stem (default S)
        self.dgap = None       # anusvara gap (default dotGap)
        self.vaW = 390.0
        self.va_top = 0.72
        self.naW = 370.0
        self.na_gap = 1.0
        self.na_top = 0.64
        self.na_leg = 0.30
        self.na_legw = 0.90
        self.kam_lead = 0.10   # how far the i-matra arch starts left of its stem (x S)
        self.kam_end = 0.35    # where the arch ends over the na danda (x S)
        self.kam_rise = 210.0
        self.kam_apex = 0.34
        self.kam_stop = 0.26   # right end height above headline (x rise)
        self.bindu_x = 1.10    # anusvara centre over na danda (x S from danda left)
        self.daW = 350.0
        self.da_bot = 0.08
        self.da_top = 0.66
        self.ra_apex = 0.52
        self.ra_len = 0.27
        self.ra_l = 0.06
        self.ra_r = 1.00
        self.dra_gap = 1.0
        self.aa_gap = 1.25
        self.va_gap = 1.0
        self.hgap = 60.0
        for k, v in kw.items():
            if not hasattr(self, k):
                raise AttributeError(k)
            setattr(self, k, v)
        self._defaults()

    def _defaults(self):
        if self.vthin is None:
            self.vthin = self.T * 1.25
        if self.vthick is None:
            self.vthick = self.S * 1.12
        if self.dS is None:
            self.dS = self.S
        if self.dgap is None:
            self.dgap = self.dotGap

    def copy(self, **kw):
        q = P.__new__(P)
        q.__dict__.update(self.__dict__)
        for k, v in kw.items():
            if not hasattr(q, k):
                raise AttributeError(k)
            setattr(q, k, v)
        return q


# ----------------------------------------------------------------- shared constructions

def foot(p, x0, x1, P_):
    """Optional angled foot cut on a stem spanning x0..x1 (kalam cut)."""
    if not P_.term_angle:
        return p
    h = math.tan(math.radians(P_.term_angle)) * (x1 - x0)
    tri = poly([(x0 - 1, -1), (x0 - 1, h), (x1 + 1, -1)])
    return difference(p, tri)


def the_arch(P_, x0, x1, top, base, SL=None, SR=None, T=None, apex=None, square=True):
    SL = P_.S if SL is None else SL
    SR = P_.S * P_.Rk if SR is None else SR
    T = P_.T if T is None else T
    apex = P_.apex if apex is None else apex
    kL = P_.kAL if square else P_.kAR
    kiL = P_.kAiL if square else P_.kAiR
    return arch2(x0, x1, top, base, SL, SR, T, apex=apex, kL=kL, kR=P_.kAR, kinL=kiL, kinR=P_.kAiR)


def bowl(P_, x0, x1, y0, y1, S_l=None, S_r=None, Ttop=None, Tbot=None, ktr=None):
    """Closed bowl ring (flat top, round bottom)."""
    S_l = P_.S * P_.Rk if S_l is None else S_l
    S_r = P_.S * P_.Rk if S_r is None else S_r
    Ttop = P_.T if Ttop is None else Ttop
    Tbot = P_.T * 1.12 if Tbot is None else Tbot
    ktr = P_.ktop if ktr is None else ktr
    outer = squircle(x0, y0, x1, y1, ktl=P_.ktop, ktr=ktr, kbl=P_.kbot, kbr=P_.kbot)
    inner = squircle(x0 + S_l, y0 + Tbot, x1 - S_r, y1 - Ttop,
                     ktl=P_.kin_top, ktr=P_.kin_top, kbl=P_.kin_bot, kbr=P_.kin_bot)
    return difference(outer, inner)


def dot(P_, cx, cy, scale=1.0):
    r = P_.dotD / 2 * scale
    if P_.dot_shape == 'square':
        return rect(cx - r * 0.89, cy - r * 0.89, cx + r * 0.89, cy + r * 0.89)
    return circle(cx, cy, r)


# ----------------------------------------------------------------- Latin lowercase
# each returns dict(path, w, l, r, dot=(cx,cy) or None)

def g_n(P_):
    S, X, W = P_.S, P_.X, P_.nW
    base = X * P_.spring
    st = foot(rect(0, 0, S, X), 0, S, P_)
    a = the_arch(P_, 0, W, X, base)
    rs = foot(rect(W - S * P_.Rk, 0, W, base), W - S * P_.Rk, W, P_)
    return dict(path=union(st, a, rs), w=W, l='s', r='s')


def g_i(P_):
    S, X = P_.S, P_.X
    st = foot(rect(0, 0, S, X), 0, S, P_)
    cx, cy = S / 2, X + P_.dotGap + P_.dotD / 2
    return dict(path=st, w=S, l='s', r='s', dot=(cx, cy))


def g_r(P_):
    S, X, W = P_.S, P_.X, P_.rW
    base = X * P_.spring
    st = foot(rect(0, 0, S, X), 0, S, P_)
    a = clip(the_arch(P_, 0, P_.nW, X, base), x1=W)
    return dict(path=union(st, a), w=W, l='s', r='flag')


def g_a(P_, asc=None):
    """single-storey a: bowl + right stem with flat top (the same bowl as Devanagari va)."""
    S, X, W = P_.S, P_.X, P_.aW
    stx0 = W - S
    b = bowl(P_, 0, W - S * 0.30, -P_.o, X, S_r=S * 0.75, ktr=P_.bowl_ktr)
    st = foot(rect(stx0, 0, W, asc or X), stx0, W, P_)
    return dict(path=union(b, st), w=W, l='r', r='s')


def g_d(P_):
    return g_a(P_, asc=P_.asc)


def g_v(P_):
    S, X, W = P_.S, P_.X, P_.vW
    f = P_.vflat
    cx = W / 2
    tL, tR = P_.vthick, P_.vthin
    # outer edges: (0,X)->(cx-f/2,0) and (W,X)->(cx+f/2,0); inner edges parallel
    def lerp(a, b, t):
        return a + (b - a) * t
    # inner-left line: (tL, X) + t*((cx-f/2) - 0, -X)
    # inner-right line: (W-tR, X) + u*((cx+f/2) - W, -X)
    # intersection: same y => t == u ; x: tL + t*(cx-f/2) = W - tR + t*(cx+f/2-W)
    t = (W - tR - tL) / ((cx - f / 2) - (cx + f / 2 - W))
    crotch = (tL + t * (cx - f / 2), X - t * X)
    pts = [(0, X), (tL, X), crotch, (W - tR, X), (W, X), (cx + f / 2, 0), (cx - f / 2, 0)]
    return dict(path=poly(pts), w=W, l='d', r='d')


def _o_ring(P_, W):
    S, X = P_.S, P_.X
    return bowl(P_, 0, W, -P_.o, X, S_l=S * P_.Rk, S_r=S * P_.Rk)


def g_o(P_):
    W = P_.oW
    return dict(path=_o_ring(P_, W), w=W, l='r', r='r')


def g_c(P_):
    W, X = P_.oW, P_.X
    p = _o_ring(P_, W)
    p = cut(p, x0=W - P_.c_top_cut, y0=X * 0.45)
    p = cut(p, x0=W - P_.c_bot_cut, y1=X * 0.45)
    b = bounds(p)
    return dict(path=p, w=b[2], l='r', r='flag')


def g_e(P_):
    W, X, S, T = P_.oW, P_.X, P_.S, P_.T
    p = _o_ring(P_, W)
    yb = X * P_.e_bar
    p = cut(p, x0=W * 0.5, y0=P_.T * 1.12 + 1, y1=yb - T * 1.05)   # open lower right
    p = cut(p, x0=W - P_.c_bot_cut, y1=yb - T * 1.05)              # bottom terminal, vertical cut
    bar = rect(S * 0.5, yb - T * 1.05, W - S * 0.5, yb)
    return dict(path=union(p, bar), w=W, l='r', r='r')


def g_t(P_):
    S, X, T = P_.S, P_.X, P_.T
    W = P_.tW
    sx = W * 0.32
    st = rect(sx, 0, sx + S, X * P_.t_h)
    bar = rect(0, X - T * 1.1, W, X)
    return dict(path=union(st, bar), w=W, l='flag', r='flag')


def g_s(P_):
    S, X, T = P_.S, P_.X, P_.T
    W = P_.sW
    Sm = S * P_.s_spine
    ym = X * 0.53
    Rs = S * 0.98
    up_o = squircle(0, ym - Sm / 2, W, X, ktl=P_.ktop, ktr=P_.ktop, kbl=P_.kbot, kbr=P_.kbot)
    up_i = squircle(Rs, ym + Sm / 2, W - Rs, X - T, ktl=P_.kin_top, ktr=P_.kin_top, kbl=P_.kin_bot, kbr=P_.kin_bot)
    up = difference(up_o, up_i)
    up = cut(up, x0=W * 0.5, y1=X - T - 1)            # remove right side below top band
    up = cut(up, x0=W - P_.c_top_cut * 0.9, y0=ym)      # top terminal cut
    lo_o = squircle(0, -P_.o, W, ym + Sm / 2, ktl=P_.ktop, ktr=P_.ktop, kbl=P_.kbot, kbr=P_.kbot)
    lo_i = squircle(Rs, P_.T * 1.12, W - Rs, ym - Sm / 2, ktl=P_.kin_top, ktr=P_.kin_top, kbl=P_.kin_bot, kbr=P_.kin_bot)
    lo = difference(lo_o, lo_i)
    lo = cut(lo, x1=W * 0.5, y0=P_.T * 1.12 + 1)       # remove left side above bottom band
    lo = cut(lo, x1=P_.c_bot_cut * 0.9, y1=ym)          # bottom terminal cut
    return dict(path=union(up, lo), w=W, l='flag', r='flag')


def g_b(P_):
    """b = the d bowl mirrored onto a left ascender stem."""
    S, X, W = P_.S, P_.X, P_.aW
    x0 = S * 0.30
    outer = squircle(x0, -P_.o, W, X, ktl=0.99, ktr=P_.ktop, kbl=P_.kbot, kbr=P_.kbot)
    inner = squircle(x0 + S * 0.75, -P_.o + P_.T * 1.12, W - S * P_.Rk, X - P_.T,
                     ktl=P_.kin_top, ktr=P_.kin_top, kbl=P_.kin_bot, kbr=P_.kin_bot)
    st = rect(0, 0, S, P_.asc)
    return dict(path=union(difference(outer, inner), st), w=W, l='s', r='r')


def g_y(P_):
    S, X, W = P_.S, P_.X, P_.vW
    f = P_.vflat
    cx = W / 2
    tL, tR = P_.vthick, P_.vthin * 1.1
    desc = X * 0.42
    # right stroke runs on below the baseline (the descender), left stroke lands on it at the baseline
    sx = ((cx + f / 2) - W) / X  # dx per unit y going down
    xr_out = lambda y: W + sx * (X - y)
    right = poly([(W - tR, X), (W, X), (xr_out(-desc), -desc), (xr_out(-desc) - tR, -desc)])
    t = (W - tR - tL) / ((cx - f / 2) - (cx + f / 2 - W))
    left = poly([(0, X), (tL, X), (tL + t * (cx - f / 2), X - t * X), (cx + f / 2 - tR * 0.2, 0), (cx - f / 2, 0)])
    left = clip(left, y0=0)
    return dict(path=union(left, right), w=W, l='d', r='d')


LATIN = {'n': g_n, 'i': g_i, 'r': g_r, 'a': g_a, 'd': g_d, 'v': g_v, 'o': g_o, 'c': g_c, 'e': g_e, 't': g_t, 's': g_s, 'b': g_b, 'y': g_y}


def sb_for(kind, P_):
    return {'s': P_.sb, 'r': P_.sbr, 'd': P_.sbd, 'flag': P_.sbf}[kind]


def set_word(word, P_, kern=None, glyphs=None):
    """Lay out a Latin word. Returns dict(path, width, dots=[(cx,cy)], xs=[glyph x])."""
    glyphs = glyphs or LATIN
    kern = kern if kern is not None else P_.kern
    x = 0.0
    parts, dots, xs = [], [], []
    prev, prevch = None, None
    for ch in word:
        if ch == ' ':
            x += P_.space
            prev = None
            continue
        g = glyphs[ch](P_)
        if prev is not None:
            x += sb_for(prev['r'], P_) + sb_for(g['l'], P_) + kern.get(prevch + ch, 0.0)
        xs.append(x)
        parts.append(shift(g['path'], x))
        if g.get('dot'):
            dots.append((x + g['dot'][0], g['dot'][1]))
        x += g['w']
        prev, prevch = g, ch
    return dict(path=union(*parts), width=x, dots=dots, xs=xs)


# ----------------------------------------------------------------- Devanagari

def d_danda(P_, x, y0=0):
    return foot(rect(x, y0, x + P_.dS, P_.H), x, x + P_.dS, P_)


def d_va(P_, x):
    """va: closed bowl hanging left of the danda (same bowl as Latin a)."""
    S, H, Th = P_.dS, P_.H, P_.Th
    B = H - Th
    bw = P_.vaW
    top = B * P_.va_top
    b = bowl(P_, x, x + bw - S * 0.30, -P_.o, top, S_r=S * 0.75, ktr=P_.bowl_ktr)
    dx = x + bw - S
    st = d_danda(P_, dx)
    return dict(path=union(b, st), x0=x, x1=dx + S)


def d_i_na(P_, x, with_bindu=True):
    """i-matra (stem + arch above the headline) + na (shoulder + danda) + anusvara."""
    S, H, Th, T = P_.dS, P_.H, P_.Th, P_.T
    B = H - Th
    st = d_danda(P_, x)
    nx0 = x + S + P_.sb * P_.na_gap * 2      # left edge of na shoulder
    ndx = nx0 + P_.naW - S                   # na danda x
    nd = d_danda(P_, ndx)
    sh_top = B * P_.na_top
    sh_base = B * P_.na_leg
    # na shoulder = the arch, mirrored use: round on the left, merging into the danda on the right
    sh = arch2(nx0, ndx + S, sh_top, sh_base, S * P_.na_legw, S, T * 1.12, apex=0.40,
               kL=P_.kAR, kR=0.98, kinL=P_.kAiR, kinR=0.95, drop=0.0)
    sh = foot(sh, nx0, nx0 + S * P_.na_legw, P_)
    na = union(nd, sh)
    # i-matra arch over the na: leaves the stem, lands just short of the headline above the na danda
    ax0 = x - S * P_.kam_lead
    ax1 = ndx + S * P_.kam_end
    rise = P_.kam_rise
    km = arch2(ax0, ax1, H + rise, H - Th * 0.5, S * 1.0, T * 1.05, T * 0.95, apex=P_.kam_apex,
               kL=P_.kAR, kR=0.72, kinL=P_.kAiR, kinR=0.72, drop=0.0)
    km = cut(km, x0=ax0 + S * 1.6, y1=H + rise * P_.kam_stop)
    parts = [st, na, km]
    dotc = None
    if with_bindu:
        dotc = (ndx + S * P_.bindu_x, H + P_.dgap + P_.dotD / 2)
    return dict(path=union(*parts), x0=x, x1=ndx + S, dot=dotc, na_danda=(ndx, ndx + S), km_end=ax1)


def d_dra(P_, x):
    """da + ra conjunct: c-bowl hanging from a short stem at its top-right; ra legs = an inverted v."""
    S, H, Th, T = P_.dS, P_.H, P_.Th, P_.T
    B = H - Th
    w = P_.daW
    y0, y1 = B * P_.da_bot, B * P_.da_top
    Tb = T * 1.12
    c = bowl(P_, x, x + w, y0, y1, S_l=S * P_.Rk, S_r=S * 0.95, Ttop=T, Tbot=Tb, ktr=0.99)
    ax = x + w * P_.ra_apex
    # open the right side between the bands, and end the bottom band at the ra apex
    L = B * P_.ra_len
    c = cut(c, x0=x + w * 0.45, y0=y0 + Tb, y1=y1 - T)
    # the da tail (down-right, heavy) grows straight out of the bowl's bottom: cut the bottom band
    # along the tail's outer edge so the outline runs on without a step
    xa0, ya0 = ax + P_.vthick * 0.05, y0 + Tb * 0.5
    xb = x + w * P_.ra_r
    wR = P_.vthick * 0.92

    def edge_x(y):
        return xa0 + (xb - xa0) * (ya0 - y) / (ya0 + L) + wR / 2
    ytop = y1 - T
    c = difference(c, poly([(edge_x(-L), -L), (edge_x(ytop), ytop), (x + w + 500, ytop), (x + w + 500, -L)]))
    band = rect(x + w * 0.45, y1 - T, x + w, y1)
    # short stem from the headline down into the bowl's top-right corner
    st = rect(x + w - S * 0.95, y1 - T, x + w, H - 1)
    # ra legs: an inverted v hanging from the bowl's bottom (down-left = ra, light; down-right = da tail, heavy)
    legL = stroke_line(ax - P_.vthin * 0.45, ya0, x + w * P_.ra_l, -L, P_.vthin * 1.2)
    legR = stroke_line(xa0, ya0, xb, -L, wR)
    legs = clip(union(legL, legR), y0=-L, y1=y0 + Tb * 0.9)
    return dict(path=union(c, band, st, legs), x0=x, x1=x + w)


def set_hindi(P_):
    """वनिंद्रा on one headline. Returns dict(path, width, dots, x0, x1)."""
    g = P_.hgap
    x = 0.0
    va = d_va(P_, x)
    x = va['x1'] + g * P_.va_gap
    ina = d_i_na(P_, x)
    x = ina['x1'] + g * P_.dra_gap
    dra = d_dra(P_, x)
    x = dra['x1'] + g * P_.aa_gap
    aa = d_danda(P_, x)
    x_end = x + P_.dS
    hl = rect(-P_.hl_over, P_.H - P_.Th, x_end + P_.hl_over_r, P_.H)
    path = union(va['path'], ina['path'], dra['path'], aa, hl)
    return dict(path=path, width=x_end, dots=[ina['dot']], x0=-P_.hl_over, x1=x_end + P_.hl_over_r,
                na_danda=ina['na_danda'])


# ----------------------------------------------------------------- composition helpers

class Ink:
    """Accumulate coloured shapes (in SVG space) and emit an SVG body."""

    def __init__(self):
        self.items = []

    def add(self, path, fill):
        self.items.append((path, fill))

    def body(self):
        # merge consecutive same-fill paths
        out = []
        for p, f in self.items:
            out.append(f'<path d="{fmt(to_d(p))}" fill="{f}"/>')
        return ''.join(out)

    def bounds(self):
        bs = [bounds(p) for p, _ in self.items]
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


import re as _re  # noqa: E402


def fmt(d):
    """round numbers in a path string to 2 decimals."""
    return _re.sub(r'-?\d+\.\d+', lambda m: ('%.2f' % float(m.group(0))).rstrip('0').rstrip('.'), d)
