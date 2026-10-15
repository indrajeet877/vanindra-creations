import subprocess, os
from geo import *
from mono import va_mark
OUT = 'loop1'; os.makedirs(OUT, exist_ok=True)
EM, IV = PAL['emerald'], PAL['ivory']

def fit(path, box):
    x0, y0, x1, y1 = bbox(path); bx, by, bw, bh = box
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    return tr(path, s, bx + (bw - (x1 - x0) * s) / 2 - x0 * s, by + (bh - (y1 - y0) * s) / 2 - y0 * s)

def card(name, p, note):
    W = 484
    body = f'<path d="{d(fit(p, (92, 30, 300, 300)))}" fill="{EM}"/>'
    # small sizes at true px on ivory and emerald
    x = 40
    for s in (16, 24, 32, 48):
        body += f'<path d="{d(fit(p, (x, 380 - s, s, s)))}" fill="{EM}"/>'
        body += f'<rect x="{x - 4}" y="{392}" width="{s + 8}" height="{s + 8}" fill="{EM}"/>'
        body += f'<path d="{d(fit(p, (x, 396, s, s)))}" fill="{IV}"/>'
        x += s + 30
    # circle DP preview 110px
    body += f'<circle cx="400" cy="400" r="55" fill="{EM}"/><path d="{d(fit(p, (400 - 33, 400 - 33, 66, 66)))}" fill="{IV}"/>'
    t = text(name + '  ' + note, family='jost', weight=400, size=13, x=12, y=472)
    body += f'<path d="{t.d}" fill="#6b5a3a"/>'
    open(f'{OUT}/{name}.svg', 'w').write(V.svg_doc(W, 484, body, bg=IV))
    return f'{OUT}/{name}.svg'

if __name__ == "__main__":
  cs = []
  cs.append(card('M1', va_mark(yj=0.55)[0], 'va: V right arm meets danda mid-height'))
  cs.append(card('M2', va_mark(yj=0.70, vx=38)[0], 'lower junction, longer V'))
  cs.append(card('M3', va_mark(yj=0.40, vx=42, h=4)[0], 'high junction: reads VI'))
  cs.append(card('M4', va_mark(yj=0.55, bindu='stem')[0], 'vam: bindu over danda (Vi / वं)'))
  cs.append(card('M5', va_mark(yj=0.55, bindu='centre')[0], 'bindu centred over headline'))
  cs.append(card('M6', va_mark(yj=0.58, curve=10)[0], 'bowed left arm = va bowl'))
  cs.append(card('M7', va_mark(yj=0.55, b=9, S=15, Td=16, h=3.2, ovl=16)[0], 'lighter, long left headline'))
  cs.append(card('M8', va_mark(yj=0.55, b=16, S=19, Td=20, h=7, ovl=6, ovr=6)[0], 'heavy, tight headline'))
  cs.append(card('M9', va_mark(yj=0.6, bindu='stem', b=12, S=17, Td=18, h=6, bar_cut=8, ovl=16)[0], 'kalam-cut headline end + bindu'))
  subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop1_mono.png'] + cs, check=True)
