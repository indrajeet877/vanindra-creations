import subprocess, os
from geo import *
from letters2 import *
from mono2 import va2
OUT = 'loop3w'; os.makedirs(OUT, exist_ok=True)
EM, IV = PAL['emerald'], PAL['ivory']

def fit(path, box, align='center'):
    x0, y0, x1, y1 = bbox(path); bx, by, bw, bh = box
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    dx = bx + (bw - (x1 - x0) * s) / 2 - x0 * s if align == 'center' else bx - x0 * s
    return tr(path, s, dx, by + (bh - (y1 - y0) * s) / 2 - y0 * s)

def card(name, wm, note, mark=None, bg=IV, fg=EM):
    W, H = 1400, 420
    body = ''
    if mark is not None:
        body += f'<path d="{d(fit(mark, (60, 70, 220, 220)))}" fill="{fg}"/>'
        body += f'<path d="{d(fit(wm, (330, 120, 1010, 140), "left"))}" fill="{fg}"/>'
    else:
        body += f'<path d="{d(fit(wm, (60, 80, 1280, 200)))}" fill="{fg}"/>'
    # small size test: wordmark at 120px wide and 220 wide
    body += f'<path d="{d(fit(wm, (60, 340, 140, 30), "left"))}" fill="{fg}"/>'
    body += f'<path d="{d(fit(wm, (240, 335, 260, 40), "left"))}" fill="{fg}"/>'
    t = text(name + '  ' + note, family='jost', weight=400, size=16, x=560, y=365)
    body += f'<path d="{t.d}" fill="#6b5a3a"/>'
    open(f'{OUT}/{name}.svg', 'w').write(V.svg_doc(W, H, body, bg=bg))
    return f'{OUT}/{name}.svg'

cs = []
st = St()
wm, tot, spans = wordmark(st)
cs.append(card('W1', wm, 'v2 caps: strokes grow from the headline'))
wm2, _, _ = wordmark(st, vgap=(st.t0 + 6, 4.0))
cs.append(card('W2', wm2, 'headline opened over the V'))
st3 = St(b=11, S=15, h=4.0, t0=3.8)
wm3, _, _ = wordmark(st3)
cs.append(card('W3', wm3, 'heavier headline (more Devanagari)'))
st4 = St(b=7, S=13, h=3.0, t0=2.8)
wm4, _, _ = wordmark(st4, space={('N', 'I'): 18, ('I', 'N'): 18, ('N', 'D'): 18, ('A', 'N'): 12, ('D', 'R'): 16})
cs.append(card('W4', wm4, 'lighter, airier'))
mk = va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.4, ovl=12, ovr=7)[0]
cs.append(card('W5', wm, 'with mark', mark=mk))
cs.append(card('W6', wm, 'with mark, reversed', mark=mk, bg=EM, fg=PAL['ivory']))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop3_wm.png'] + cs, check=True)
