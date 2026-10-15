"""Exploration round 3: ideas where the jaali GEOMETRY builds the V (not pattern-filled letters)."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import v_pts, RENDER
from explore2 import Arm, BIG, TH, S, C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
K = math.cos(math.pi * 3 / 8) / math.cos(math.pi * 2 / 8)  # inner radius ratio of {8/3}: 0.5412


def star83(cx, cy, R, a0=90):
    return star_pts(cx, cy, R, 8, 3, a0=a0)


# N1: V = one hollow point of an 8-point jaali star; terminals mitred on the star's radial lines
def n1_point(t=0.16):
    R = 100.0
    outer = star83(0, 0, R)
    inner = offset(outer, t * R)
    band = diff(P(outer), P(inner))
    # keep the bottom point: wedge between radial lines at 247.5 and 292.5 degrees
    wedge = P([(0, 0), polar(0, 0, 400, 247.5), polar(0, 0, 400, 292.5)])
    return inter(band, wedge)


def n1_rosette(t=0.16):
    R = 100.0
    outer = star83(0, 0, R)
    inner = offset(outer, t * R)
    band = diff(P(outer), P(inner))
    gaps = []
    for k in range(8):
        a = 247.5 + 45 * k
        p0 = polar(0, 0, 0, a)
        gaps.append(vt.stroke_to_path(P([polar(0, 0, 20, a), polar(0, 0, 200, a)]), 3.0))
    return diff(band, union(*gaps))


# N2: octagon + square frieze in both arms (classic jaali cells), constant webs
def n2_octagons(H=100.0, t=26.0, w=2.6):
    V = P(v_pts(H, TH, t))
    holes = []
    A = t / 2 - w                       # octagon apothem
    Rr = A / math.cos(22.5 * D2R)
    pitch = 2 * A + w
    sq = (pitch - 2 * A)                # (unused, web)
    for side in (-1, 1):
        arm = Arm(H, t, side)
        a = pitch * 0.9
        while a < arm.L + pitch:
            # octagon with flats on the rails: vertices at 22.5 + 45k in the local frame
            holes.append(arm.poly([(a + Rr * math.cos((22.5 + 45 * k) * D2R), Rr * math.sin((22.5 + 45 * k) * D2R)) for k in range(8)]))
            a += pitch
    arm = Arm(H, t, 1)
    holes.append(P(ngon_pts(arm.O[0], arm.O[1], Rr, 8, a0=22.5)))
    clip = P(offset(v_pts(H, TH, t), w))
    return inter(diff(V, inter(union(*holes), clip)), BIG)


# N3: solid stone jambs, a jaali screen spanning the counter
def n3_screen(H=100.0, t=22.0, w=1.8):
    V = P(v_pts(H, TH, t))
    tn = math.tan(TH * D2R)
    dv = t / S
    counter = P([(-(H - dv) * tn, 0), ((H - dv) * tn, 0), (0, H - dv)])
    gap = 3.2
    cin = P(offset([(-(H - dv) * tn, 0), ((H - dv) * tn, 0), (0, H - dv)], gap))
    a = 9.0
    holes = []
    for i in range(-8, 9):
        for j in range(0, 12):
            holes.append(P(star83(i * a, j * a + a / 2, a * 0.5 - w * 0.2)))
    screen = diff(cin, union(*holes))
    return union(inter(V, BIG), inter(screen, BIG))


# N4: the counter is an 8-point star opening into the sky: star points bite into the stone
def n4_starcounter(H=100.0, t=30.0):
    tn = math.tan(TH * D2R)
    dv = t / S
    V = P(v_pts(H, TH, t))
    apex = H - dv
    R = 22.0
    cy = apex - R
    star = P(star83(0, cy, R))
    r = R * K
    # open slot upward from the inner vertices next to the top point
    p1, p2 = polar(0, cy, r, 112.5), polar(0, cy, r, 67.5)
    slot = P([p1, (p1[0] - (p1[1]) * tn, 0 - 0.01), (p2[0] + p2[1] * tn, -0.01), p2])
    slot = P([p1, (p1[0] - p1[1] * tn, -1), (p2[0] + p2[1] * tn, -1), p2])
    tri = P([(-200, 0), (200, 0), (0, H)])
    solid = inter(P([(-H * tn, 0), (H * tn, 0), (0, H)]), BIG)
    return diff(solid, union(star, slot))


# N5: 60-degree V cut from a hexagonal jaali (hexagon openings + triangle openings, no hexagrams)
def n5_hex(H=100.0, t=34.0):
    th = 30.0
    V = P(v_pts(H, th, t))
    w = 2.2
    inner = P(offset(v_pts(H, th, t), w))
    a = 12.0
    holes = []
    for i in range(-12, 13):
        for j in range(-1, 14):
            x = i * a + (j % 2) * a / 2
            y = H - j * a * math.sqrt(3) / 2
            holes.append(P(offset(ngon_pts(x, y, a / math.sqrt(3), 6, a0=90), w / 2)))
    return inter(diff(V, inter(union(*holes), inner)), BIG)


# N6: V from a continuous interlaced band, tied in an octagonal knot at the base
def n6_knot(H=100.0, t=10.0, g=2.6):
    tn = math.tan(TH * D2R)
    # left band: top-left to below the vertex; right band mirrored; they cross at the base forming a diamond knot
    def band(side):
        x0 = side * -H * tn * 0.92
        y0 = 0.0
        dx, dy = -side * S * -1, C
        dx, dy = (S if side < 0 else -S), C
        L = H / C * 1.12
        nx, ny = C, -dx / 1 * 0 + (S if side > 0 else -S)
        nx, ny = dy, -dx
        p1 = (x0 - nx * t / 2, y0 - ny * t / 2)
        p2 = (x0 + nx * t / 2, y0 + ny * t / 2)
        return P([p1, p2, (p2[0] + dx * L, p2[1] + dy * L), (p1[0] + dx * L, p1[1] + dy * L)])
    Lb, Rb = inter(band(-1), BIG), inter(band(1), BIG)
    # over / under: left over right at the crossing
    cut = vt.stroke_to_path(Lb, g * 2)
    return union(Lb, diff(Rb, cut))


VARS = [('N1 V = one point of the jaali star', n1_point), ('N1b eight Vs = the jaali rosette', n1_rosette),
        ('N2 octagon frieze', n2_octagons), ('N3 jambs + screen', n3_screen), ('N4 star counter', n4_starcounter),
        ('N5 hex jaali 60deg', n5_hex), ('N6 interlaced knot', n6_knot)]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'z{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r2.png')] + files, check=True)
    print('ok')
