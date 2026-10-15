"""Monoline lowercase built on the kolam rule: straight lines + true circular arcs, tangent joins,
one stroke weight. Coordinates: y-up, baseline 0, x-height X. Glyph = list of centre-line primitives."""
import math, sys
sys.path.insert(0, '.')
from kolam import *

SLOPE = 2.0           # the mark's knight's-move diagonal (half-angle 26.57 deg)

class Spec:
    def __init__(self, X=100.0, s=11.0, asc=146.0, desc=46.0, ov=1.6, dot=None, rv=None):
        self.X, self.s, self.asc, self.desc, self.ov = X, s, asc, desc, ov
        self.dot = dot if dot is not None else 0.78 * s       # i-dot radius (pulli)
        self.rv = rv if rv is not None else 0.0                # v vertex centre-line radius

def P_line(a, b):
    P = pathops.Path(); P.moveTo(a[0], -a[1]); P.lineTo(b[0], -b[1]); return P

def P_arc(c, r, a0, a1):
    """arc from angle a0 to a1 (degrees, signed sweep = a1-a0)."""
    P = pathops.Path()
    a0r, span = math.radians(a0), math.radians(a1 - a0)
    st = (c[0] + r * math.cos(a0r), c[1] + r * math.sin(a0r))
    P.moveTo(st[0], -st[1])
    for p1, p2, p3 in arc_beziers(c, r, a0r, span):
        P.cubicTo(p1[0], -p1[1], p2[0], -p2[1], p3[0], -p3[1])
    return P

def stroke_all(prims, s, cap='butt'):
    out = [vtype.stroke_to_path(p, s, cap=cap, join='round') for p in prims]
    return vtype.union(*out)

def clip_y(path, ymin=None, ymax=None):
    # SVG coords: y is flipped; ymin/ymax in y-up space
    B = pathops.Path()
    lo = -1e4 if ymax is None else -ymax
    hi = 1e4 if ymin is None else -ymin
    B.moveTo(-1e4, lo); B.lineTo(1e4, lo); B.lineTo(1e4, hi); B.lineTo(-1e4, hi); B.close()
    return vtype.intersection(path, B)

def disc(c, r):
    return circle_path(c, r, flip=True)

# ---------------------------------------------------------------- glyphs
# each returns (outline path, advance width, left x of ink, right x of ink) drawn with origin at x=0
def g_o(S):
    R = S.X / 2 - S.s / 2 + S.ov
    c = (S.s / 2 + R, S.X / 2)
    p = vtype.stroke_to_path(circle_path(c, R, flip=True), S.s, cap='butt', join='round')
    return p, 2 * R + S.s

def bowl(S, cx):
    R = S.X / 2 - S.s / 2 + S.ov
    return circle_path((cx, S.X / 2), R, flip=True), R

def g_a(S, stem_top=None):
    R = S.X / 2 - S.s / 2 + S.ov
    cx = S.s / 2 + R
    b, _ = bowl(S, cx)
    top = S.X if stem_top is None else stem_top
    stem = P_line((cx + R, top), (cx + R, 0))
    p = vtype.union(vtype.stroke_to_path(b, S.s, 'butt', 'round'), vtype.stroke_to_path(stem, S.s, 'butt', 'round'))
    return p, 2 * R + S.s

def g_d(S):
    return g_a(S, stem_top=S.asc)

def g_b(S):
    R = S.X / 2 - S.s / 2 + S.ov
    x0 = S.s / 2
    cx = x0 + R
    b, _ = bowl(S, cx)
    stem = P_line((x0, S.asc), (x0, 0))
    p = vtype.union(vtype.stroke_to_path(b, S.s, 'butt', 'round'), vtype.stroke_to_path(stem, S.s, 'butt', 'round'))
    return p, 2 * R + S.s

def g_n(S, Rn=None):
    Rn = Rn or (0.40 * S.X)
    x0 = S.s / 2
    yc = S.X - S.s / 2 - Rn + 0.8
    prims = [P_line((x0, 0), (x0, yc)), P_arc((x0 + Rn, yc), Rn, 180, 0), P_line((x0 + 2 * Rn, yc), (x0 + 2 * Rn, 0))]
    return stroke_all(prims, S.s), 2 * Rn + S.s

def g_r(S, Rn=None, end=62):
    Rn = Rn or (0.40 * S.X)
    x0 = S.s / 2
    yc = S.X - S.s / 2 - Rn + 0.8
    prims = [P_line((x0, 0), (x0, yc)), P_arc((x0 + Rn, yc), Rn, 180, end)]
    p = stroke_all(prims, S.s)
    xmax = x0 + Rn + Rn * math.cos(math.radians(end)) + S.s / 2 * math.sin(math.radians(end))
    return p, xmax

def g_i(S):
    x0 = S.s / 2
    stem = P_line((x0, 0), (x0, S.X))
    dy = S.X + 1.05 * S.s + S.dot
    p = vtype.union(vtype.stroke_to_path(stem, S.s, 'butt', 'round'), disc((x0, dy), S.dot))
    return p, S.s

def g_v(S, height=None):
    H = height or S.X
    half = H / SLOPE / 2 * 1.0   # half-width at top for slope 2 over height H -> H/2/... see below
    # slope 2: dy/dx = 2 -> dx = H/2 per arm
    dx = H / SLOPE
    s = S.s
    beta = math.atan(1 / SLOPE)        # half-angle from vertical
    if S.rv > 0:
        rv = S.rv
        cy = rv + s / 2 - S.ov
        # tangent points of arm lines on circle centred (0, cy): arms are lines with direction (sin b, cos b)
        # left arm offset: point on circle at angle 180+... normal to arm
        nx, ny = math.cos(beta), -math.sin(beta)   # outward normal of left arm (pointing down-left) mirrored
        tl = (-rv * math.cos(beta), cy - rv * math.sin(beta))
        tr = (rv * math.cos(beta), cy - rv * math.sin(beta))
        # extend arms up to beyond H
        L = H * 1.3
        top_l = (tl[0] - L * math.sin(beta), tl[1] + L * math.cos(beta))
        top_r = (tr[0] + L * math.sin(beta), tr[1] + L * math.cos(beta))
        a0 = 180 + math.degrees(beta); a1 = 360 - math.degrees(beta)
        prims = [P_line(top_l, tl), P_arc((0, cy), rv, a0, a1), P_line(tr, top_r)]
        p = stroke_all(prims, s)
    else:
        vy = s / 2 / math.sin(beta) - S.ov      # centre-line vertex so the miter tip sits at -ov
        L = H * 1.4
        P = pathops.Path()
        P.moveTo(-L * math.sin(beta), -(vy + L * math.cos(beta)))
        P.lineTo(0, -vy)
        P.lineTo(L * math.sin(beta), -(vy + L * math.cos(beta)))
        p = vtype.stroke_to_path(P, s, cap='butt', join='miter', miter_limit=20)
    p = clip_y(p, ymax=H)
    x0, y0, x1, y1 = vtype.bounds(p)
    p = vtype.transform(p, 1, 0, 0, 1, -x0, 0)
    return p, x1 - x0

def g_y(S):
    s = S.s; H = S.X
    beta = math.atan(1 / SLOPE)
    # right arm: through (dx, H) to below baseline; left arm meets it at baseline point
    dx = H / SLOPE
    meet = (0.0, 0.0)
    top_l = (-dx, H); top_r = (dx, H)
    L = H * 0.6
    bot = (meet[0] - (S.desc + 10) / SLOPE, -S.desc - 10)
    prims = [P_line((top_r[0] + 10 / SLOPE, H + 10), bot), P_line((top_l[0] - 10 / SLOPE, H + 10), (meet[0] + 0.0, meet[1] + 0.0))]
    p = stroke_all(prims, s)
    p = clip_y(p, ymin=-S.desc, ymax=H)
    x0, y0, x1, y1 = vtype.bounds(p)
    p = vtype.transform(p, 1, 0, 0, 1, -x0, 0)
    return p, x1 - x0

def g_c(S, open_deg=48):
    R = S.X / 2 - S.s / 2 + S.ov
    c = (S.s / 2 + R, S.X / 2)
    p = stroke_all([P_arc(c, R, open_deg, 360 - open_deg)], S.s)
    x0, y0, x1, y1 = vtype.bounds(p)
    return p, x1

def g_e(S, open_deg=38):
    R = S.X / 2 - S.s / 2 + S.ov
    c = (S.s / 2 + R, S.X / 2)
    prims = [P_arc(c, R, 0, 360 - open_deg), P_line((c[0] - R, S.X / 2), (c[0] + R, S.X / 2))]
    p = stroke_all(prims, S.s)
    x0, y0, x1, y1 = vtype.bounds(p)
    return p, 2 * R + S.s

def g_t(S, T=None, arm=None):
    T = T or (S.X * 1.28)
    arm = arm or 0.27 * S.X
    x0 = arm
    prims = [P_line((x0, 0), (x0, T)), P_line((x0 - arm, S.X - S.s / 2), (x0 + arm, S.X - S.s / 2))]
    p = stroke_all(prims, S.s)
    x0b, _, x1b, _ = vtype.bounds(p)
    return p, x1b

def g_s(S):
    s = S.s
    tot = (S.X - s + 2 * S.ov) / 2 - 0.09 * S.X    # keep the circles apart so the spine is a real crossing tangent
    Rt = tot * 0.48
    Rb = tot * 0.52
    cx = Rb + s / 2
    ct = (cx, S.X - s / 2 - Rt + S.ov)
    cb = (cx, s / 2 + Rb - S.ov)
    p1, p2, phi = tangent(ct, Rt, +1, cb, Rb, -1)
    a_dep = math.degrees(math.atan2(p1[1] - ct[1], p1[0] - ct[0]))
    a_arr = math.degrees(math.atan2(p2[1] - cb[1], p2[0] - cb[0]))
    t_start = 22
    b_end = 202
    a_dep = a_dep % 360
    if a_dep < t_start: a_dep += 360
    a_arr = a_arr % 360
    # bottom: from a_arr going CW (decreasing) to b_end-360
    end = b_end - 360
    while end > a_arr: end -= 360
    prims = [P_arc(ct, Rt, t_start, a_dep), P_line(p1, p2), P_arc(cb, Rb, a_arr, end)]
    p = stroke_all(prims, s)
    x0, y0, x1, y1 = vtype.bounds(p)
    p = vtype.transform(p, 1, 0, 0, 1, -x0, 0)
    return p, x1 - x0

GLYPHS = {'o': g_o, 'a': g_a, 'd': g_d, 'b': g_b, 'n': g_n, 'r': g_r, 'i': g_i, 'v': g_v, 'y': g_y,
          'c': g_c, 'e': g_e, 't': g_t, 's': g_s}

# side bearings in units of X (left, right) -- straight stems get more, rounds less
SB = {'o': (0.055, 0.055), 'a': (0.055, 0.10), 'd': (0.055, 0.10), 'b': (0.10, 0.055), 'n': (0.10, 0.10),
      'r': (0.10, 0.02), 'i': (0.10, 0.10), 'v': (0.02, 0.02), 'y': (0.02, 0.02), 'c': (0.055, 0.02),
      'e': (0.055, 0.04), 't': (0.02, 0.03), 's': (0.045, 0.045)}
KERN = {('r', 'a'): -0.03, ('v', 'a'): -0.035, ('a', 'v'): -0.03, ('t', 'i'): 0.0, ('r', 'e'): -0.02, ('e', 'a'): 0.0}

def word(text, S, tracking=0.0, kern=KERN, sb=SB):
    x = 0.0
    parts = []
    prev = None
    for ch in text:
        if ch == ' ':
            x += 0.30 * S.X; prev = None; continue
        p, adv = GLYPHS[ch](S)
        l, r = sb[ch]
        if prev is not None:
            x += kern.get((prev, ch), 0.0) * S.X
        x += l * S.X
        parts.append(vtype.transform(p, 1, 0, 0, 1, x, 0))
        x += adv + r * S.X + tracking * S.X
        prev = ch
    return vtype.union(*parts), x

if __name__ == '__main__':
    body = ''
    y = 40
    for s, rv, tr in ((8.5, 0, 0.02), (11, 0, 0.02), (11, 9, 0.02), (13, 0, 0.0)):
        S = Spec(s=s, rv=rv)
        for txt in ('vanindra', 'creations', 'edit by'):
            p, wdt = word(txt, S, tracking=tr)
            body += f'<g transform="translate(30,{y + 150})"><path d="{vtype.to_d(p)}" fill="#0B2A20"/></g>'
            body += f'<text x="{60 + wdt}" y="{y+150}" font-family="sans-serif" font-size="14" fill="#888">s={s} rv={rv}</text>'
            y += 200
    open('wm_test.svg', 'w').write(vtype.svg_doc(1300, y + 40, body, bg='#F6F1E7'))
