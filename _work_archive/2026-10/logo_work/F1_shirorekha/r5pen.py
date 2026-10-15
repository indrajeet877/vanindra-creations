"""F1 polish: the contrast pen, now emitting fitted cubic Beziers instead of a sampled polygon (same width rule as
r4latin.vstroke_pts: full weight where the stroke travels vertically, hairline where it travels along the line)."""
from r3geo import *
from r4latin import _u
from r5fit import outline


def vstroke_pts(pts, S, h, p=1.35, taper=(None, None), tz=0.16, tpow=0.9, smooth=0, wfun=None, tol=0.05):
    N = len(pts)
    tang, ws = [], []
    for i in range(N):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, N - 1)]
        tx, ty = _u(b[0] - a[0], b[1] - a[1])
        tang.append((tx, ty))
        ws.append(h + (S - h) * abs(ty) ** p if wfun is None else wfun(i / (N - 1), tx, ty))
    if smooth:
        ws = [sum(ws[max(0, i - smooth):i + smooth + 1]) / len(ws[max(0, i - smooth):i + smooth + 1]) for i in range(N)]
    L, R = [], []
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
    return outline(L, R, tol)
