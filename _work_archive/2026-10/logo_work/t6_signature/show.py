import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, word2
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
COLS = ['#c0392b','#2980b9','#27ae60','#8e44ad','#d35400','#16a085','#2c3e50','#e67e22','#7f8c8d','#c71585','#556b2f','#4169e1','#b8860b']

def word_path(cfg=None, hair=4.2, shade=17.0, boost=0.0):
    S, c = word2.build(cfg)
    pen = P.Pen(slant=c['slant'], hair=hair, shade=shade)
    return P.render(S, pen, hair_boost=boost), S, pen

def show(cfg=None, name='w2', colored=False, hair=4.2, shade=17.0, width=1500, grid=True):
    path, S, pen = word_path(cfg, hair, shade)
    xmin, ymin, xmax, ymax = path.bounds; pad = 30
    tx, ty = -xmin + pad, ymax + pad
    body = ''
    if colored:
        for i, s in enumerate(S):
            o = P.stroke_outline(pen.sample(s))
            body += f'<path d="{P.d_of(P.flip(o, 1, tx, ty))}" fill="{COLS[i % len(COLS)]}" fill-opacity="0.7"/>'
    else:
        body += f'<path d="{P.d_of(P.flip(path, 1, tx, ty))}" fill="#0B2A20"/>'
    if grid:
        g = f'<g transform="translate({tx:.1f},{ty:.1f})">'
        for yy in (0, 100, 212, 252):
            g += f'<line x1="{xmin-pad}" x2="{xmax+pad}" y1="{-yy}" y2="{-yy}" stroke="#39f" stroke-width="0.4"/>'
        body += g + '</g>'
    svg = P.vtype.svg_doc(round(xmax - xmin + 2*pad), round(ymax - ymin + 2*pad), body, bg='#F6F1E7')
    open(name + '.svg', 'w').write(svg)
    subprocess.run(['node', RENDER, 'png', name + '.svg', name + '.png', str(width)], check=True)
    return path

if __name__ == '__main__':
    show(None, 'w2c', colored=True)
    show(None, 'w2', grid=False)
