"""construction.png (final-final): how the system is built. Supporting sheet only; the idea is visible without it."""
import subprocess
from r4system import *
from r4mark import va_vloop
import vtype as V
from build2 import global_parts

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
    W, H = 1600, 1040
    L = []
    g, info = va_vloop(**MK)
    x0, y0, x1, y1 = bbox(g)
    s = 520 / (y1 - y0)
    ox, oy = 120 - x0 * s, 160 - y0 * s
    T = lambda p: tr(p, s, ox, oy)
    X = lambda u: ox + u * s
    Y = lambda v: oy + v * s
    L.append((T(info['counter']), TINT))
    L.append((T(g), EM))
    L += [label('va / V   the mark', 120, 100, 26, EM, 600)]
    # the silhouette V: shoulder -> point -> up the return stroke
    K, P, Jp = MK['K'], MK['P'], info['J']
    ext = lambda a, b, t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    L.append(seg((X(ext(P, K, 1.25)[0]), Y(ext(P, K, 1.25)[1])), (X(P[0]), Y(P[1])), 2.0))
    L.append(seg((X(P[0]), Y(P[1])), (X(ext(P, Jp, 1.35)[0]), Y(ext(P, Jp, 1.35)[1])), 2.0))
    for (u, v) in (P, Jp, info['T1']):
        L.append((circle(X(u), Y(v), 4.5), GO))
    yb = Y(100) + 60
    L += [label('two Vs: the counter (tinted) and the silhouette (gold guide).', 120, yb),
          label('the loop leaves the danda as a hairline, swells down the left,', 120, yb + 26),
          label('ends in a point; the return stroke is the V\'s right arm.', 120, yb + 52),
          label('the loop hangs from the danda, never from the line (so: va, not pa);', 120, yb + 92),
          label('the danda runs on below the point (a letter, not a pennant).', 120, yb + 118)]
    # right column: the system
    wx = 820
    wm, tot, st = vanindra('master')
    k = 700 / (tot + 2 * OVL)
    wy = 190
    L += [label('VANINDRA   the name hangs from one line', wx, 150, 26, EM, 600)]
    L.append((tr(wm, k, wx + OVL * k, wy), EM))
    L += [label('verticals are dandas; diagonals are leaves (hairline at the line,', wx, wy + 100 * k + 40),
          label('full weight at the foot); bowls are k = 0.60 superellipses.', wx, wy + 100 * k + 66)]
    letters, line, end = full_name('master')
    k2 = 700 / (end + OVL)
    fy = 440
    L.append((tr(U(letters, line), k2, wx + OVL * k2, fy), EM))
    xs = wx + OVL * k2 + (tot + 18.0) * k2
    L.append((rect(xs - 1, fy - 22, xs + 1, fy - 6), GO))
    L += [label('full name: CREATIONS stands on VANINDRA\'s baseline under the same line;', wx, fy + 100 * k2 + 40),
          label('the line steps to a hairline in the gap (gold tick), never over a letter.', wx, fy + 100 * k2 + 66)]
    # cuts
    cy = 640
    L += [label('three cuts of one drawing', wx, cy, 22, EM, 600)]
    mh, toth, sth = vanindra('sturdy')
    k3 = 330 / (toth + 2 * OVL)
    L.append((tr(mh, k3, wx + OVL * k3, cy + 24), EM))
    L += [label('sturdy: headers, Reel credits, embroidery', wx, cy + 24 + 100 * k3 + 26, 16),
          label('(hairline 1.6% of the word width)', wx, cy + 24 + 100 * k3 + 46, 16)]
    ml, _ = mark('lockup')
    mb = bbox(ml)
    k4 = 120 / (mb[3] - mb[1])
    L.append((tr(ml, k4, wx + 400 - mb[0] * k4, cy + 20), EM))
    mm, _ = mark('master')
    L.append((tr(mm, k4, wx + 560 - bbox(mm)[0] * k4, cy + 20), EM))
    L += [label('lockup cut   master', wx + 400, cy + 170, 16)]
    gl, gline = global_parts('master')
    gb = bbox(U(gl, gline))
    k5 = 600 / (gb[2] - gb[0])
    gy = 880
    L.append((tr(gl, k5, wx - gb[0] * k5, gy), EM))
    L.append((tr(gline, k5, wx - gb[0] * k5, gy), GO))
    L += [label('global (USD): the line becomes one gold hairline; the caps touch it.', wx, gy + 100 * k5 + 34)]
    out = write(os.path.join(HERE, '_work', 'construction2.svg'), svg(W, H, L, bg=IV))
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js'), 'png', out, os.path.join(HERE, 'construction.png'), str(W)], check=True)


if __name__ == '__main__':
    main()
