import subprocess, os
from geo import *
import letters2
from letters2 import *
from mono2 import va2
OUT = 'loop4'; os.makedirs(OUT, exist_ok=True)
EM, IV = PAL['emerald'], PAL['ivory']
from loop3_wm import fit

def big(name, path, note, W=1400, H=420, bg=IV, fg=EM):
    body = f'<path d="{d(fit(path, (60, 50, W - 120, H - 130)))}" fill="{fg}"/>'
    t = text(name + '  ' + note, family='jost', weight=400, size=16, x=60, y=H - 30)
    body += f'<path d="{t.d}" fill="#6b5a3a"/>'
    open(f'{OUT}/{name}.svg', 'w').write(V.svg_doc(W, H, body, bg=bg))
    return f'{OUT}/{name}.svg'

st = St()
letters2.BUILD['V'] = lambda st, W=72: g_V2(st, W=W, qh=0.66)
wm, tot, spans = wordmark(st)
f1 = big('P1', wm, 'straight wedge V')
# mark: straight-wedge version built from the V2 + danda
def mark_straight(H=100, b=10, S=15, h=4.4, t0=4.5, px=37, py=90, yj=0.5, xs=62, qh=0.62, ovl=12, ovr=7):
    P = (px, py)
    J = (xs, yj * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx > 0: nx, ny = -nx, -ny
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_x((Pi[1], Pi[0]), (Ji[1], Ji[0]), xs))
    yq = H * qh
    Q = (line_x(Pi, Ji, yq), yq)
    I0 = (t0 + b * px / py, b)
    x_top = line_x(I0, Q, 0)
    bowl = poly([(0, 0), (x_top, 0), Q, J2, (xs + 0.5, J2[1]), (xs + 0.5, J[1]), J, P])
    g = U(bowl, rect(xs, 0, xs + S, H), rect(-ovl, 0, xs + S + ovr, b))
    return g
m1 = va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.4, ovl=12, ovr=7)[0]
m2 = mark_straight()
m3 = mark_straight(qh=0.70, t0=4)
both = U(m1, tr(m2, 1, 140, 0), tr(m3, 1, 280, 0))
f2 = big('P2', both, 'mark: curved blade | straight wedge | straight wedge longer')
# lockup on one line: mark at cap height + word gap
lk = U(m2, tr(wm, 1, 62 + 15 + 7 + 10 + 34, 0))
f3 = big('P3', lk, 'one headline sentence: mark + wordmark, word gap')
lk2 = U(m1, tr(wm, 1, 62 + 15 + 7 + 10 + 34, 0))
f4 = big('P4', lk2, 'same with curved blade mark')
subprocess.run(['node', '../toolkit/render.js', 'png', f1, 'study/p1.png', '1400'], check=True)
subprocess.run(['node', '../toolkit/render.js', 'png', f2, 'study/p2.png', '1400'], check=True)
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'study/p34.png', f3, f4], check=True)
