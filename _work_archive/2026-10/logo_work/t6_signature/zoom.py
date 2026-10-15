import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, sig
from explore import RENDER
MK = dict(m_dIs=78, m_k=.6, m_turn=24, m_rise=.6, v_fade=30, v_fade_ease=1.2, i_tail=36, i_ease=1.2)
def go(name='zoom', pk=dict(hair=7, shade=26), extra=None, crop=None, width=1400, overlay=True):
    cfg = dict(MK); cfg.update(extra or {})
    S, c = sig.mark_strokes(cfg)
    pen = P.Pen(slant=c['slant'], **pk)
    path = P.render(S, pen)
    xmin, ymin, xmax, ymax = crop or path.bounds
    pad = 10
    W, H = xmax - xmin + 2 * pad, ymax - ymin + 2 * pad
    fl = P.flip(path, 1, -xmin + pad, ymax + pad)
    body = f'<path d="{P.d_of(fl)}" fill="#0B2A20"/>'
    if overlay:
        body += f'<path d="{P.d_of(fl)}" fill="none" stroke="#e33" stroke-width="0.25"/>'
        # on-curve points
        import re
    svg = P.vtype.svg_doc(round(W), round(H), body, bg='#fff')
    open(name + '.svg', 'w').write(svg)
    subprocess.run(['node', RENDER, 'png', name + '.svg', name + '.png', str(width)], check=True)
if __name__ == '__main__':
    go()
