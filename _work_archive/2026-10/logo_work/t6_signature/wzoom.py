import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, sig, build
from explore import RENDER
def go(name, x0, x1, extra=None):
    cfg = dict(build.CFG); cfg.update(extra or {})
    S, c = sig.wordmark_strokes(cfg)
    path = P.render(S, P.Pen(slant=c['slant'], **build.WPEN))
    xmin, ymin, xmax, ymax = path.bounds
    pad = 8
    W, H = x1 - x0 + 2 * pad, ymax - ymin + 2 * pad
    fl = P.flip(path, 1, -x0 + pad, ymax + pad)
    body = f'<path d="{P.d_of(fl)}" fill="#0B2A20"/>'
    open(name + '.svg', 'w').write(P.vtype.svg_doc(round(W), round(H), body, bg='#fff'))
    subprocess.run(['node', RENDER, 'png', name + '.svg', name + '.png', '1500'], check=True)
    return path.bounds
if __name__ == '__main__':
    b = go('wz_full', -200, 2000)
    print(b)
    go('wz_left', b[0] - 5, b[0] + 560)
    go('wz_right', b[0] + 540, b[2] + 5)
