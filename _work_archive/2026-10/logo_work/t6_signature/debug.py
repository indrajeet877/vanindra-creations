import sys, os, subprocess, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P
import word

OUT = os.path.dirname(os.path.abspath(__file__))
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'


def nodes_overlay(strokes, pen):
    out = []
    for s in strokes:
        for n in s:
            x = n.x + n.y * pen.t
            out.append(f'<circle cx="{x:.1f}" cy="{-n.y:.1f}" r="2.2" fill="#e33"/>')
    return ''.join(out)


def main(cfg=None, name='debug', overlay=True, pen_kw=None):
    pen = P.Pen(**(pen_kw or {}))
    S = word.build(cfg)
    t0 = time.time()
    path = P.render(S, pen)
    xmin, ymin, xmax, ymax = path.bounds
    pad = 40
    w, h = xmax - xmin + 2 * pad, ymax - ymin + 2 * pad
    fl = P.flip(path, 1, -xmin + pad, ymax + pad)
    body = f'<path d="{P.d_of(fl)}" fill="#0B2A20"/>'
    if overlay:
        g = f'<g transform="translate({-xmin + pad:.1f},{ymax + pad:.1f})">'
        g += f'<path d="{P.skeleton_d(S, pen)}" fill="none" stroke="#e33" stroke-width="0.8" opacity="0.8"/>'
        g += nodes_overlay(S, pen)
        for yy in (0, 100, 250, 270):
            g += f'<line x1="{xmin - pad}" x2="{xmax + pad}" y1="{-yy}" y2="{-yy}" stroke="#39f" stroke-width="0.5"/>'
        g += '</g>'
        body += g
    svg = P.vtype.svg_doc(round(w), round(h), body, bg='#F6F1E7')
    f = os.path.join(OUT, f'{name}.svg')
    open(f, 'w').write(svg)
    subprocess.run(['node', RENDER, 'png', f, os.path.join(OUT, f'{name}.png'), '1500'], check=True)
    print('ok', round(time.time() - t0, 2), 's', len(svg) // 1024, 'KB')


if __name__ == '__main__':
    main()
