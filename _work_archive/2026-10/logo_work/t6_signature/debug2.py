import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, word
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
def run(cfg=None, name='dbg_strokes', pen_kw=None, width=1500):
    pen = P.Pen(**(pen_kw or {}))
    S = word.build(cfg)
    cols = ['#c0392b','#2980b9','#27ae60','#8e44ad','#d35400','#16a085','#2c3e50','#e67e22','#7f8c8d','#c71585','#556b2f','#4169e1','#b8860b']
    parts = []; allp = None
    for i, s in enumerate(S):
        o = P.stroke_outline(pen.sample(s))
        parts.append((o, cols[i % len(cols)]))
        allp = o if allp is None else P.pathops.op(allp, o, P.pathops.PathOp.UNION)
    xmin, ymin, xmax, ymax = allp.bounds; pad = 30
    body = ''
    for o, c in parts:
        body += f'<path d="{P.d_of(P.flip(o, 1, -xmin + pad, ymax + pad))}" fill="{c}" fill-opacity="0.75"/>'
    g = f'<g transform="translate({-xmin + pad:.1f},{ymax + pad:.1f})">'
    for i, s in enumerate(S):
        for n in s:
            g += f'<circle cx="{n.x + n.y * pen.t:.1f}" cy="{-n.y:.1f}" r="1.6" fill="#000"/>'
    for yy in (0, 100, 250, 270):
        g += f'<line x1="{xmin-pad}" x2="{xmax+pad}" y1="{-yy}" y2="{-yy}" stroke="#39f" stroke-width="0.4"/>'
    g += '</g>'
    svg = P.vtype.svg_doc(round(xmax - xmin + 2*pad), round(ymax - ymin + 2*pad), body + g, bg='#FFFFFF')
    f = name + '.svg'; open(f, 'w').write(svg)
    subprocess.run(['node', RENDER, 'png', f, name + '.png', str(width)], check=True)
if __name__ == '__main__':
    run()
