import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, mono, explore
from explore import place, label
RENDER = explore.RENDER
def study(items, out, cols=4, size=300, pen_kw=None):
    W = cols * (size + 40) + 40
    rows = (len(items) + cols - 1) // cols
    H = rows * (size + 80) + 40
    body = ''
    for i, (name, strokes, cfg) in enumerate(items):
        kw = dict(slant=cfg.get('slant', 18), hair=4.2, shade=17.0); kw.update(pen_kw or {})
        kw.update(cfg.get('_pen', {}))
        pth = P.render(strokes, P.Pen(**kw), hair_boost=cfg.get('_boost', 0))
        x = 40 + (i % cols) * (size + 40); y = 40 + (i // cols) * (size + 80)
        body += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="#fff"/>'
        body += place(pth, (x + 30, y + 30, size - 60, size - 60))
        body += label(name, x, y + size + 30, 18, '#333')
    open(out + '.svg', 'w').write(P.vtype.svg_doc(W, H, body, bg='#F6F1E7'))
    subprocess.run(['node', RENDER, 'png', out + '.svg', out + '.png', str(min(W, 1500))], check=True)
if __name__ == '__main__':
    its = []
    for rise in (0.45, 0.6, 0.75):
        for dIs in (30, 64):
            S = mono.m_canopy({}, rise=rise)
            its.append((f'rise {rise} dIs {dIs}', mono.m_canopy({}, rise=rise, Is=None if dIs == 64 else None), {}))
    study(its, 'mstudy')
