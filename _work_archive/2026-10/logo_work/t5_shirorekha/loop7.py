import subprocess, os
from geo import *
import letters2
from letters2 import *
from mono2 import va2
from loop3_wm import fit
OUT = 'loop7'; os.makedirs(OUT, exist_ok=True)
EM, IV = PAL['emerald'], PAL['ivory']

def big(name, path, note, W=1400, H=420, bg=IV, fg=EM):
    body = f'<path d="{d(fit(path, (60, 50, W - 120, H - 130)))}" fill="{fg}"/>'
    t = text(name + '  ' + note, family='jost', weight=400, size=16, x=60, y=H - 30)
    body += f'<path d="{t.d}" fill="#6b5a3a"/>'
    open(f'{OUT}/{name}.svg', 'w').write(V.svg_doc(W, H, body, bg=bg))
    return f'{OUT}/{name}.svg'

st = St()
letters2.BUILD['V'] = lambda st, W=72: g_V3(st, W=W, swell=-24, bo=3)
wmA, _, _ = wordmark(st)
fA = big('Q1', wmA, 'curved blade V (heavier) + straight wedges')
letters2.BUILD['A'] = lambda st, W=74: g_A3(st, W=W, belly=-6)
wmB, _, _ = wordmark(st)
fB = big('Q2', wmB, 'curved blade V + bellied A')
mk = va2(bo=6, bi=-18, t0=4.5, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.4, ovl=12, ovr=7)[0]
fM = big('Q3', U(mk, tr(va2(bo=5, bi=-22, t0=4.5, py=92, yj=0.52, xs=63, px=37, b=10, S=15, h=4.6, ovl=12, ovr=7)[0], 1, 150, 0),
               tr(va2(bo=4, bi=-20, t0=4.0, py=100, yj=0.56, xs=64, px=38, b=10, S=15, h=4.6, ovl=12, ovr=7)[0], 1, 300, 0)), 'marks: D4-like | fuller | point on baseline', H=520)
for f, o in ((fA, 'q1'), (fB, 'q2'), (fM, 'q3')):
    subprocess.run(['node', '../toolkit/render.js', 'png', f, f'study/{o}.png', '1400'], check=True)
