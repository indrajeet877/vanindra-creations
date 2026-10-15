"""construction.png (F1): how the system is built. Supporting sheet only; the idea is visible without it."""
import subprocess
from r5system import *
from r4mark import va_vloop
import vtype as V
from r5small import small16

TINT = '#E6D7AE'
NOTE = '#7a6233'


def label(txt, x, y, size=19, color=NOTE, weight=500):
    return (V.text_path(txt, family='manrope', weight=weight, size=size, x=x, y=y).path, color)


def seg(a, b, w=2.0, c=GO):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return (poly([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]), c)


def main():
    W, H = 1600, 1120
    L = []
    g, info = va_vloop(**MK5)
    x0, y0, x1, y1 = bbox(g)
    s = 500 / (y1 - y0)
    ox, oy = 120 - x0 * s, 150 - y0 * s
    T = lambda p: tr(p, s, ox, oy)
    X = lambda u: ox + u * s
    Y = lambda v: oy + v * s
    L.append((T(info['counter']), TINT))
    L.append((T(g), EM))
    L += [label('va   the mark', 120, 100, 26, EM, 600)]
    K, P, Jp = MK5['K'], MK5['P'], info['J']
    ext = lambda a, b, t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    L.append(seg((X(ext(P, (8.0, 52.0), 1.35)[0]), Y(ext(P, (8.0, 52.0), 1.35)[1])), (X(P[0]), Y(P[1])), 2.0))
    L.append(seg((X(P[0]), Y(P[1])), (X(ext(P, Jp, 1.35)[0]), Y(ext(P, Jp, 1.35)[1])), 2.0))
    # weight ticks: danda 13 (heaviest), shoulder 11.9, loop top 6.0, return 10.5
    for (u, v) in (P, Jp, info['T1']):
        L.append((circle(X(u), Y(v), 4.5), GO))
    yb = Y(100) + 56
    L += [label('the counter (tinted) and the silhouette (gold guides) are both a V.', 120, yb),
          label('stroke weights: danda 13 > shoulder 11.9 > return 10.5 > loop top 6.0.', 120, yb + 26),
          label('the loop hangs from the danda, never from the line (va, not pa);', 120, yb + 52),
          label('one cubic per side, no knuckle; the danda runs on below the point.', 120, yb + 78)]
    # small cut on its pixel grid
    gs, _, _ = small16()
    k = 15.0
    gx, gy = 120, 860
    grid = []
    for i in range(17):
        grid.append(rect(gx + i * k - 0.5, gy, gx + i * k + 0.5, gy + 16 * k))
        grid.append(rect(gx, gy + i * k - 0.5, gx + 16 * k, gy + i * k + 0.5))
    L.append((U(*grid), '#D9CCAE'))
    L.append((tr(gs, k, gx, gy), EM))
    L += [label('mark_small on the 16 px grid: line, danda,', gx + 16 * k + 30, gy + 40),
          label('the loop top and the empty row land on', gx + 16 * k + 30, gy + 66),
          label('whole pixels at 16, 32, 48 and 64 px.', gx + 16 * k + 30, gy + 92)]
    # right column: the system
    wx = 820
    wm, tot, st = vanindra('master')
    kk = 700 / (tot + 2 * OVL)
    wy = 180
    L += [label('VANINDRA   the name hangs from one line', wx, 140, 26, EM, 600)]
    L.append((tr(wm, kk, wx + OVL * kk, wy), EM))
    L += [label('verticals are dandas; diagonals are leaves (hairline at the line,', wx, wy + 100 * kk + 40),
          label('full weight at the foot); bowls are k = 0.60 superellipses.', wx, wy + 100 * kk + 66)]
    wmf, crs, cline, end = full_name5('master')
    k2 = 700 / (end + OVL)
    fy = 430
    L.append((tr(U(wmf, crs, cline), k2, wx + OVL * k2, fy), EM))
    L += [label('full name: each word hangs from its own line, as words do in', wx, fy + 100 * k2 + 40),
          label('Devanagari. VANINDRA from the heavy line, CREATIONS from a hairline', wx, fy + 100 * k2 + 66),
          label('at its own cap height; both stand on one baseline.', wx, fy + 100 * k2 + 92)]
    cy = 690
    L += [label('three cuts of one drawing', wx, cy, 22, EM, 600)]
    mh, toth, sth = vanindra('sturdy')
    k3 = 330 / (toth + 2 * OVL)
    L.append((tr(mh, k3, wx + OVL * k3, cy + 24), EM))
    L += [label('sturdy: headers, Reel credits, embroidery', wx, cy + 24 + 100 * k3 + 26, 16)]
    ml, _ = mark5('lockup')
    mb = bbox(ml)
    k4 = 110 / (mb[3] - mb[1])
    L.append((tr(ml, k4, wx + 400 - mb[0] * k4, cy + 20), EM))
    mm, _ = mark5('master')
    L.append((tr(mm, k4, wx + 560 - bbox(mm)[0] * k4, cy + 20), EM))
    L += [label('lockup cut   master', wx + 400, cy + 160, 16)]
    gl, gline = global_parts5('master')
    gb = bbox(U(gl, gline))
    k5 = 640 / (gb[2] - gb[0])
    gy2 = 940
    L.append((tr(gl, k5, wx - gb[0] * k5, gy2), EM))
    L.append((tr(gline, k5, wx - gb[0] * k5, gy2), GO))
    L += [label('global (USD): the lines become gold hairlines; the caps touch them.', wx, gy2 + 100 * k5 + 34)]
    out = write(os.path.join(HERE, '_work', 'construction3.svg'), svg(W, H, L, bg=IV))
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js'), 'png', out, os.path.join(HERE, 'construction.png'), str(W)], check=True)


if __name__ == '__main__':
    main()
