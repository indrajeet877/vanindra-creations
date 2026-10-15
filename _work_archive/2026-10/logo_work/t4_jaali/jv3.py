"""Jaali V v3: a stone V with one carved jaali window in each arm (solid base, solid caps, solid rails)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore8 import contours, area

TH = 22.5
S, C, TN = math.sin(TH * D2R), math.cos(TH * D2R), math.tan(TH * D2R)


def v_outline(H, t):
    dv = t / S
    return [(-H * TN, 0), (-(H - dv) * TN, 0), (0, H - dv), ((H - dv) * TN, 0), (H * TN, 0), (0, H)]


class Frame:
    def __init__(self, H, t, side):
        dv = t / S
        self.O = (0.0, H - dv / 2)
        self.u = (side * S, -C)
        self.n = (C, side * S)
        self.ang = math.degrees(math.atan2(-self.u[1], self.u[0]))
        self.L = (H - dv / 2) / C

    def w(self, a, b):
        return (self.O[0] + self.u[0] * a + self.n[0] * b, self.O[1] + self.u[1] * a + self.n[1] * b)


def build(H=124.0, t=26.0, rail=4.0, web=1.8, n=3, start=None, ends='square', kind=3, gap=None, ret=False):
    region = P(v_outline(H, t))
    dv = t / S
    band = t - 2 * rail
    R = band / 2                                   # star radius: points touch the rails' inner faces (web added below)
    g = web if gap is None else gap
    pitch = 2 * R * math.cos(22.5 * D2R) + g if kind == 3 else 2 * R + g
    # window starts just above the junction: the point on the axis where the inner rail of the other arm stops
    a0 = start if start is not None else (dv / 2) / math.cos(TH * D2R) * 0.0 + t * 1.05
    length = n * pitch + g
    windows, seeds = [], []
    for side in (-1, 1):
        F = Frame(H, t, side)
        b0, b1 = -band / 2, band / 2
        if ends == 'square':
            win = [F.w(a0, b0), F.w(a0 + length, b0), F.w(a0 + length, b1), F.w(a0, b1)]
        else:  # pointed ends (45-degree star-point tips on the axis)
            h = band / 2 / math.tan(22.5 * D2R)
            win = [F.w(a0 - h, 0), F.w(a0, b0), F.w(a0 + length, b0), F.w(a0 + length + h, 0), F.w(a0 + length, b1), F.w(a0, b1)]
        windows.append(P(win))
        for k in range(n):
            c = F.w(a0 + g + pitch * k + pitch / 2 - g / 2, 0)
            seeds.append(star_pts(c[0], c[1], R - g / 2 - web / 2 + web / 2 - 0.0, 8, kind, a0=F.ang + 22.5))
    win = merge(windows)
    stars = [P(offset(s, web / 2)) for s in seeds]
    grown = merge([P(offset(s, -web / 2)) for s in seeds])
    left = [c for c in contours(diff(P_inset(win, web), grown)) if area(c) > 0.6]
    holes = inter(merge(stars + left), P_inset(win, 0.0))
    mark = diff(region, holes)
    if ret:
        return mark, dict(win=win, seeds=seeds)
    return mark


def P_inset(path, d):
    if d <= 0:
        return path
    st = vt.stroke_to_path(path, 2 * d, join='miter')
    return diff(path, st)
