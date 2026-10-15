"""Construction drawing of the va/V mark on its 100-unit grid."""
import subprocess
from build import *
from mono2 import va2
p = P['mark']
g, info = va2(**p)
s = 5.0
ox, oy = 120, 110
W, H = 900, 760
L = []
def X(x): return ox + x * s
def Y(y): return oy + y * s
body = f'<path d="{d(tr(g, s, ox, oy))}" fill="{EM}" fill-opacity="0.92"/>'
guide = '#A8843A'
def hl(y, lab):
    return (f'<line x1="40" x2="{W-40}" y1="{Y(y)}" y2="{Y(y)}" stroke="{guide}" stroke-width="1" stroke-dasharray="4 4"/>' +
            f'<path d="{V.text_path(lab, family="jost", weight=400, size=13, x=W-150, y=Y(y)-5).d}" fill="{guide}"/>')
def vl(x, lab):
    return (f'<line y1="40" y2="{H-60}" x1="{X(x)}" x2="{X(x)}" stroke="{guide}" stroke-width="1" stroke-dasharray="4 4"/>' +
            f'<path d="{V.text_path(lab, family="jost", weight=400, size=13, x=X(x)+4, y=H-48).d}" fill="{guide}"/>')
xs, S = info['xs'], info['S']
for y, lab in [(0, 'headline 0'), (p['b'], f'bar {p["b"]}'), (p['yj'] * 100, f'junction {p["yj"]*100:g}'), (p['py'], f'leaf tip {p["py"]:g}'), (100, 'baseline 100')]:
    body += hl(y, lab)
for x, lab in [(0, '0'), (p['px'], f'tip {p["px"]}'), (xs, f'danda {xs:g}'), (xs + S, f'{xs+S:g}')]:
    body += vl(x, lab)
# leaf chords and control points
P_ = info['P']
for a, c, b in [((0, 0), info['co'], P_)]:
    body += f'<polyline points="{X(a[0])},{Y(a[1])} {X(c[0])},{Y(c[1])} {X(b[0])},{Y(b[1])}" fill="none" stroke="#D2B26A" stroke-width="1.2"/>'
    body += f'<circle cx="{X(c[0])}" cy="{Y(c[1])}" r="4" fill="#D2B26A"/>'
body += f'<circle cx="{X(P_[0])}" cy="{Y(P_[1])}" r="4" fill="none" stroke="#D2B26A" stroke-width="1.5"/>'
t = V.text_path('va / V — leaf blade (quadratic), hairline return h=5, danda 14.5, headline 9.6; all units of a 100-unit body', family='jost', weight=400, size=14, x=40, y=30)
body += f'<path d="{t.d}" fill="#6b5a3a"/>'
open('construction.svg', 'w').write(V.svg_doc(W, H, body, bg=IV))
subprocess.run(['node', '../toolkit/render.js', 'png', 'construction.svg', 'construction.png', '900'], check=True)
