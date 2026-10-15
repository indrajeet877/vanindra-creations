"""Exploration round 2: openings built as true tracery aligned to each arm (not stamped badges)."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import v_pts, RENDER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5
S, C = math.sin(TH * D2R), math.cos(TH * D2R)
BIG = P([(-400, 0), (400, 0), (400, 400), (-400, 400)])  # keep below the top cut line


class Arm:
    """Local frame of one arm. a = distance along centre line from the vertex point (upwards), b = across."""

    def __init__(self, H, t, side):
        dv = t / S
        self.O = (0.0, H - dv / 2)
        self.u = (side * S, -C)          # up the arm
        self.n = (C, side * S)           # across the arm (towards outside for side=-1? sign irrelevant)
        self.t = t
        self.L = (H - dv / 2) / C        # centre line length to the top cut

    def pt(self, a, b):
        return (self.O[0] + self.u[0] * a + self.n[0] * b, self.O[1] + self.u[1] * a + self.n[1] * b)

    def poly(self, local_pts):
        return P([self.pt(a, b) for a, b in local_pts])

    def strip(self, b0, b1, a0=-200, a1=400):
        return self.poly([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])


def star_local(a, b, R, n=8, m=3, rot=0.0, r=None):
    return star_pts(a, b, R, n, m, a0=rot, r=r)


def base_V(H=100.0, t=24.0):
    return P(v_pts(H, TH, t))


def arm_only(H, t, side):
    """strip of one arm, excluding the overlap diamond with the other arm"""
    A = Arm(H, t, side)
    Bm = Arm(H, t, -side)
    return diff(inter(A.strip(-t / 2, t / 2), BIG), Bm.strip(-t / 2, t / 2))


def trellis_holes(arm, w, pitch, a_start, a_end):
    """rhombic openings: rails parallel to the arm, rungs parallel to the OTHER arm (45 deg to this one)."""
    t = arm.t
    hb = t / 2 - w            # half-height of opening band
    holes = []
    a = a_start
    k = 0
    while a < a_end:
        # parallelogram with sides along the arm and at 45 degrees (rung direction)
        sh = 2 * hb  # 45 degree shear across the full band
        q = [(a, -hb), (a + pitch - w * math.sqrt(2), -hb), (a + pitch - w * math.sqrt(2) + sh, hb), (a + sh, hb)]
        holes.append(arm.poly(q))
        a += pitch
        k += 1
    return holes


def frieze_83(arm, w, a_start, a_end, R=None, gap=None):
    t = arm.t
    R = R or (t / 2 - w)
    gap = gap if gap is not None else w
    pitch = 2 * R * math.cos(22.5 * D2R) + gap  # stars edge-to-edge-ish
    holes = []
    a = a_start
    while a <= a_end:
        holes.append(arm.poly(star_local(a, 0, R, 8, 3, rot=0)))
        a += pitch
    return holes


def octagon_chain(arm, w, a_start, a_end):
    t = arm.t
    A = t / 2 - w                    # octagon apothem
    Rr = A / math.cos(22.5 * D2R)
    pitch = 2 * A + w
    holes = []
    a = a_start
    while a <= a_end:
        holes.append(arm.poly(ngon_pts(a, 0, Rr, 8, a0=22.5)))
        # small diamond (square at 45) sitting on each rail between octagons
        a += pitch
    # squares between octagons near the rails: the classic 4.8.8 frieze
    sq = []
    a = a_start + pitch / 2
    side = 2 * A * math.tan(22.5 * D2R)
    while a <= a_end:
        for bsign in (-1, 1):
            pass
        a += pitch
    return holes


def V_with(holes_fn, H=100.0, t=24.0):
    V = base_V(H, t)
    holes = holes_fn(H, t)
    return inter(diff(V, union(*holes)), BIG)


# ---------------- variants
def c_trellis(H=100.0, t=24.0):
    w = 3.0
    R_ = Arm(H, t, 1)
    holes = trellis_holes(R_, w, 13.0, t * 0.75, R_.L + 20)
    return inter(diff(base_V(H, t), inter(union(*holes), P(offset(v_pts(H, TH, t), w)))), BIG)


def c_frieze83(H=100.0, t=24.0):
    w = 2.6
    R_ = Arm(H, t, 1)
    holes = frieze_83(R_, w, t * 0.85, R_.L + 10)
    clipzone = inter(arm_only(H, t, 1), P(offset(v_pts(H, TH, t), w)))
    return inter(diff(base_V(H, t), inter(union(*holes), clipzone)), BIG)


def c_octchain(H=100.0, t=24.0):
    w = 2.6
    R_ = Arm(H, t, 1)
    holes = octagon_chain(R_, w, t * 0.85, R_.L + 10)
    clipzone = inter(arm_only(H, t, 1), P(offset(v_pts(H, TH, t), w)))
    return inter(diff(base_V(H, t), inter(union(*holes), clipzone)), BIG)


def c_growing(H=100.0, t=24.0):
    """stone to light: star openings grow as the right arm rises"""
    w = 2.4
    R_ = Arm(H, t, 1)
    holes = []
    rmax = t / 2 - w
    a = t * 0.7
    k = 0
    sizes = [0.30, 0.48, 0.66, 0.84, 1.0, 1.0]
    for f in sizes:
        R = rmax * f
        holes.append(R_.poly(star_local(a + R, 0, R, 8, 3)))
        a += 2 * R + w * 1.3
    return inter(diff(base_V(H, t), union(*holes)), BIG)


def jewel(H=100.0, t=26.0):
    V = base_V(H, t)
    A = Arm(H, t, 1)
    # node where the two centre lines meet; the star sits in the overlap diamond
    R = t * 0.43
    star = P(star_pts(A.O[0], A.O[1], R, 8, 3, a0=90))
    return diff(V, star)


def sym_frieze(H=100.0, t=24.0):
    w = 2.4
    holes = []
    for side in (-1, 1):
        a = Arm(H, t, side)
        holes += frieze_83(a, w, t * 0.95, a.L + 10)
    A0 = Arm(H, t, 1)
    holes.append(P(star_pts(A0.O[0], A0.O[1], t / 2 - w + 1.5, 8, 3, a0=90)))
    clipzone = P(offset(v_pts(H, TH, t), w))
    return inter(diff(base_V(H, t), inter(union(*holes), clipzone)), BIG)


def sym_trellis(H=100.0, t=24.0):
    w = 2.8
    holes = []
    for side in (-1, 1):
        a = Arm(H, t, side)
        holes += trellis_holes(a, w, 12.0, t * 0.62, a.L + 20)
    return inter(diff(base_V(H, t), inter(union(*holes), P(offset(v_pts(H, TH, t), w)))), BIG)


def lattice8(H=100.0, t=30.0):
    """full 8-fold lattice: lines parallel to both arms + horizontals, as thin webs; openings are the cells"""
    w = 2.4
    V = base_V(H, t)
    inner = P(offset(v_pts(H, TH, t), w))
    webs = []
    sp = 12.0
    for side in (-1, 1):
        dx, dy = side * S, -C
        nx, ny = C, side * S
        for k in range(-20, 21):
            ox, oy = 0 + nx * k * sp, H + ny * k * sp
            p1 = (ox - dx * 300, oy - dy * 300)
            p2 = (ox + dx * 300, oy + dy * 300)
            line = P([p1, p2, (p2[0] + nx * 0.01, p2[1] + ny * 0.01)])
            webs.append(vt.stroke_to_path(P([p1, p2]), w))
    webp = union(*webs)
    holes = diff(inner, webp)
    return inter(diff(V, holes), BIG)


def star_split(H=100.0):
    """8/3 star whose lower point is separated as a V-shaped rim by a V channel"""
    R = 50.0
    st = star_pts(0, 0, R, 8, 3, a0=90)
    star = P(st)
    # channel parallel to the lower point's edges
    tip = (0, R)
    t = 11.0
    g = 3.0
    dv1 = t / S
    dv2 = (t + g) / S
    tn = math.tan(TH * D2R)
    ch = P([(-(200) * tn - 0, R - dv1 - 200), (0, R - dv1), ((200) * tn, R - dv1 - 200),
            ((200) * tn + 0.0, R - dv2 - 200 + 0), (0, R - dv2), (-(200) * tn, R - dv2 - 200)])
    # build the channel as the band between two nested V lines
    outer = P([(-200 * tn, R - dv1 - 200), (0, R - dv1), (200 * tn, R - dv1 - 200)])
    band = diff(P([(-200 * tn, R - dv1 - 200), (0, R - dv1), (200 * tn, R - dv1 - 200)]),
                P([(-200 * tn, R - dv2 - 200), (0, R - dv2), (200 * tn, R - dv2 - 200)]))
    return diff(star, band)


VARS = [('A contrast: trellis hairline', c_trellis), ('B contrast: 8/3 star frieze', c_frieze83), ('C contrast: octagon chain', c_octchain),
        ('D stone to light', c_growing), ('E jewel at the knot', jewel), ('F symmetric star frieze', sym_frieze),
        ('G symmetric trellis', sym_trellis), ('H 8-fold lattice', lattice8), ('I star with V rim', star_split)]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'y{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r1.png')] + files, check=True)
    print('ok')
