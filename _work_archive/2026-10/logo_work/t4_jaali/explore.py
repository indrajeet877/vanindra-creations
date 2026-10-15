"""Round-0 exploration: >= 6 genuinely different jaali V ideas."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
os.makedirs(OUT, exist_ok=True)
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'


def v_pts(H, theta, t, cut=0.0):
    tn = math.tan(theta * D2R)
    dv = t / math.sin(theta * D2R)
    Wo, Wi = H * tn, (H - dv) * tn
    if cut > 0:
        bot = [(cut * tn, H - cut), (-cut * tn, H - cut)]
    else:
        bot = [(0, H)]
    return [(-Wo, 0), (-Wi, 0), (0, H - dv), (Wi, 0), (Wo, 0)] + bot


def arm_axis(H, theta, t):
    """returns vertex point on axis and unit directions (up-left, up-right) of the arm centre lines"""
    dv = t / math.sin(theta * D2R)
    v = (0.0, H - dv / 2)
    s, c = math.sin(theta * D2R), math.cos(theta * D2R)
    return v, (-s, -c), (s, -c)


# 1 ---- chain of rotated khatim stars, point to point along each arm
def var_chain_khatim():
    H, th, t, w = 100.0, 22.5, 24.0, 3.2
    V = P(v_pts(H, th, t))
    v, uL, uR = arm_axis(H, th, t)
    R = t / 2 - w
    holes = []
    step = 2 * R + w * 1.0
    for u in (uL, uR):
        for k in range(1, 6):
            c = (v[0] + u[0] * step * k, v[1] + u[1] * step * k)
            holes.append(P(star_pts(c[0], c[1], R, 8, 2, a0=90 - th)))
    # vertex star, bigger
    holes.append(P(star_pts(v[0], v[1] + 2, R * 1.15, 8, 2, a0=90 - th)))
    m = diff(V, union(*holes))
    return inter(m, P([(-200, 0), (200, 0), (200, 200), (-200, 200)]))


# 2 ---- {8/3} stars, upright, sitting in each arm, fewer & larger
def var_chain_83():
    H, th, t, w = 100.0, 22.5, 26.0, 3.0
    V = P(v_pts(H, th, t))
    v, uL, uR = arm_axis(H, th, t)
    R = t / 2 - w + 1.2
    holes = []
    step = 2 * R * 0.93
    for u in (uL, uR):
        for k in range(1, 5):
            c = (v[0] + u[0] * step * k, v[1] + u[1] * step * k)
            holes.append(P(star_pts(c[0], c[1], R, 8, 3, a0=90)))
    holes.append(P(star_pts(v[0], v[1], R, 8, 3, a0=90)))
    m = diff(V, union(*holes))
    return inter(m, P([(-200, 0), (200, 0), (200, 200), (-200, 200)]))


# 3 ---- solid inverted triangle carved by one big {8/3} star: the V is the stone left over
def var_star_carved():
    H, th = 100.0, 22.5
    tn = math.tan(th * D2R)
    tri = P([(-H * tn, 0), (H * tn, 0), (0, H)])
    R = 30.0
    cy = H - 22 - R
    star = P(star_pts(0, cy, R, 8, 3, a0=90))
    return diff(tri, star)


# 4 ---- 60-degree V on a triangular grid, filled with hexagonal jaali (6-pt star openings)
def var_hex_lattice():
    H, th, t = 100.0, 30.0, 30.0
    V = P(v_pts(H, th, t))
    rim = 3.0
    inner = P(offset(v_pts(H, th, t), rim))
    a = 10.0  # lattice spacing
    holes = []
    for i in range(-12, 13):
        for j in range(0, 14):
            x = i * a + (j % 2) * a / 2
            y = j * a * math.sqrt(3) / 2
            holes.append(P(star_pts(x, y, a * 0.5, 6, 2, a0=90, r=a * 0.5 * 0.62)))
    holes = inter(union(*holes), inner)
    return diff(V, holes)


# 5 ---- reveal / conceal: one arm solid stone, other arm pierced
def var_reveal():
    H, th, t, w = 100.0, 22.5, 24.0, 3.0
    V = P(v_pts(H, th, t))
    v, uL, uR = arm_axis(H, th, t)
    R = t / 2 - w
    holes = []
    step = 2 * R + w
    for k in range(0, 6):
        c = (v[0] + uR[0] * step * k, v[1] + uR[1] * step * k)
        holes.append(P(star_pts(c[0], c[1], R, 8, 2, a0=90 - th)))
    m = diff(V, union(*holes))
    return inter(m, P([(-200, 0), (200, 0), (200, 200), (-200, 200)]))


# 6 ---- V filled with a square-grid star-and-cross jaali (as if sawn from a screen)
def var_lattice_fill():
    H, th, t = 100.0, 22.5, 28.0
    V = P(v_pts(H, th, t))
    inner = P(offset(v_pts(H, th, t), 2.6))
    a = 11.0
    holes = []
    for i in range(-10, 11):
        for j in range(-1, 12):
            holes.append(P(star_pts(i * a, j * a, a * 0.47, 8, 2, a0=90)))
    holes = inter(union(*holes), inner)
    return diff(V, holes)


# 7 ---- negative V: an inverted-triangle slab, openings arranged in a V (container test)
def var_negative():
    H, th = 100.0, 22.5
    tn = math.tan(th * D2R)
    tri = P([(-H * tn - 8, -4), (H * tn + 8, -4), (0, H + 14)])
    t = 22.0
    v, uL, uR = arm_axis(H, th, t)
    R = 8.0
    holes = [P(star_pts(v[0], v[1], R, 8, 2, a0=90 - th))]
    for u in (uL, uR):
        for k in range(1, 5):
            c = (v[0] + u[0] * 19 * k, v[1] + u[1] * 19 * k)
            holes.append(P(star_pts(c[0], c[1], R, 8, 2, a0=90 - th)))
    return diff(tri, union(*holes))


# 8 ---- V built of stone octagon cells, each pierced with an 8-point star (cells touch at edges)
def var_cells():
    a = 20.0  # cell pitch
    holes, cells = [], []
    s = math.sin(22.5 * D2R)
    pos = [(0, 0)]
    for k in range(1, 5):
        pos += [(-k * a * 0.5, -k * a * 0.92), (k * a * 0.5, -k * a * 0.92)]
    for (x, y) in pos:
        cells.append(P(ngon_pts(x, y, a * 0.5 / math.cos(22.5 * D2R) + 0.4, 8, a0=22.5)))
        holes.append(P(star_pts(x, y, a * 0.36, 8, 2, a0=90)))
    return diff(union(*cells), union(*holes))


# 9 ---- interlaced strap V: two straps crossing at the base with over/under break, ends cut on 8-fold angles
def var_strap():
    H, th, t = 100.0, 22.5, 14.0
    s, c = math.sin(th * D2R), math.cos(th * D2R)
    L = 112.0
    # left strap: runs from top-left down through the axis and a little past it to the lower right
    def strap(sign):
        x0, y0 = -sign * H * math.tan(th * D2R), 0.0
        dx, dy = sign * s, c
        nx, ny = c, -sign * s
        p1 = (x0 - nx * t / 2, y0 - ny * t / 2)
        p2 = (x0 + nx * t / 2, y0 + ny * t / 2)
        p3 = (p2[0] + dx * L, p2[1] + dy * L)
        p4 = (p1[0] + dx * L, p1[1] + dy * L)
        return P([p1, p2, p3, p4])
    A, B = strap(1), strap(-1)
    top = inter(A, P([(-200, 0), (200, 0), (200, 200), (-200, 200)]))
    B = inter(B, P([(-200, 0), (200, 0), (200, 200), (-200, 200)]))
    gap = vt.stroke_to_path(top, 5.0)
    m = union(top, diff(B, gap))
    # cut a star at the crossing
    return m


VARS = [('1 khatim chain', var_chain_khatim), ('2 star 8/3 chain', var_chain_83), ('3 star-carved stone', var_star_carved),
        ('4 hex lattice 60deg', var_hex_lattice), ('5 reveal / conceal', var_reveal), ('6 sawn from a screen', var_lattice_fill),
        ('7 negative V (container test)', var_negative), ('8 octagon cells', var_cells), ('9 interlaced strap', var_strap)]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'x{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r0.png')] + files, check=True)
    print('ok')
