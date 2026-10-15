"""construction.png: how the system is built (supporting sheet; the idea is meant to be visible without it)."""
import subprocess
from r3system import *
from r3mark import va_cloop

TINT = '#E6D7AE'
NOTE = '#7a6233'


def label(txt, x, y, size=19, color=NOTE, weight=500):
    return (V.text_path(txt, family='manrope', weight=weight, size=size, x=x, y=y).path, color)


def hline(x0, x1, y, w=1.2, c=NOTE):
    return (rect(x0, y - w / 2, x1, y + w / 2), c)


def vline(x, y0, y1, w=1.2, c=NOTE):
    return (rect(x - w / 2, y0, x + w / 2, y1), c)


def main():
    W, H = 1600, 980
    L = []
    # ---- the mark, large, with the V counter tinted
    g, info = va_cloop(**MK)
    x0, y0, x1, y1 = bbox(g)
    s = 520 / (y1 - y0)
    ox, oy = 120 - x0 * s, 150 - y0 * s
    T = lambda p: tr(p, s, ox, oy)
    L.append((T(info['counter']), TINT))
    L.append((T(g), EM))
    X = lambda u: ox + u * s
    Y = lambda v: oy + v * s
    L += [label('va / V   the mark', 120, 100, 26, EM, 600)]
    # annotations
    L += [hline(X(x1) + 20, X(x1) + 60, Y(MK['b'] / 2)), label('the line: shirorekha, 9.5', X(x1) + 70, Y(MK['b'] / 2) + 7)]
    L += [hline(X(x1) + 20, X(x1) + 60, Y(70)), label('danda, 13: the letter hangs from the line', X(x1) + 70, Y(70) + 7)]
    L += [label('leaf-loop: hairline where it leaves the danda (5.5),', 120, Y(100) + 70),
          label('swells on the left, ends in a point at the tip', 120, Y(100) + 96),
          label('counter (tinted) = a V.  ink = va: the loop hangs from the danda,', 120, Y(100) + 140),
          label('never from the line, so it cannot read as pa', 120, Y(100) + 166)]
    # tip / join markers
    P, J, T1 = info['P'], info['J'], info['T1']
    for (u, v) in (P, J, T1):
        L.append((circle(X(u), Y(v), 4.5), GO))
    # ---- the wordmark system, right
    wm, tot, st = vanindra()
    k = 700 / (tot + 2 * OVL)
    wx, wy = 840, 250
    L.append((tr(wm, k, wx + OVL * k, wy), EM))
    L += [label('VANINDRA   the name hangs from one line', wx, 215, 26, EM, 600)]
    L += [hline(wx, wx + (tot + 2 * OVL) * k, wy + 100 * k + 18, 1.0), label('every vertical is a danda (13); every diagonal is a leaf:', wx, wy + 100 * k + 48),
          label('a hairline at the line, full weight at the foot. line 8.8', wx, wy + 100 * k + 74)]
    # full name + step
    letters, line, end = (lambda: None)() or (None, None, None)
    from build import full_name
    letters, line, end = full_name()
    k2 = 700 / (end + OVL)
    fy = 560
    L.append((tr(U(letters, line), k2, wx + OVL * k2, fy), EM))
    L += [label('one continuous line: heavy over the name, then a hairline', wx, fy + 100 * k2 + 40),
          label('that CREATIONS hangs from (drawn, not typeset; no repeated initial)', wx, fy + 100 * k2 + 66)]
    # global
    gl, gline, gend = full_name(bar=False)
    k3 = 480 / (gend + OVL)
    gy = 800
    L.append((tr(gl, k3, wx + OVL * k3, gy), EM))
    L.append((tr(gline, k3, wx + OVL * k3, gy), GO))
    L += [label('global (USD): same capitals, the line becomes a gold hairline', wx, gy + 100 * k3 + 36)]
    out = write(os.path.join(HERE, '_work', 'construction.svg'), svg(W, H, L, bg=IV))
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js'), 'png', out, os.path.join(HERE, 'construction.png'), str(W)], check=True)


if __name__ == '__main__':
    main()
