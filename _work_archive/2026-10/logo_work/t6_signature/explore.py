"""Exploration sheet: six signature directions, each with a monogram drawn from its own strokes."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, word2, mono

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
INK, IVORY = '#0B2A20', '#F6F1E7'


def place(path, box, ink=INK):
    """Fit a y-up path into box=(x, y, w, h) (SVG coords), centred."""
    xmin, ymin, xmax, ymax = path.bounds
    s = min(box[2] / (xmax - xmin), box[3] / (ymax - ymin))
    w, h = (xmax - xmin) * s, (ymax - ymin) * s
    tx = box[0] + (box[2] - w) / 2 - xmin * s
    ty = box[1] + (box[3] - h) / 2 + ymax * s
    return f'<path d="{P.d_of(P.flip(path, s, tx, ty))}" fill="{ink}"/>'


def label(text, x, y, size=22, ink='#6b6b6b'):
    t = P.vtype.text_path(text, family='jost', weight=400, size=size, x=x, y=y, tracking=0.08)
    return f'<path d="{t.d}" fill="{ink}"/>'


VARIANTS = [
    ('1 Copperplate - hook V, crook arm', dict(), {}, 'crook'),
    ('2 Canopy - V rises into the I', dict(v_arm='canopy', gap_nI=96), {}, 'canopy'),
    ('3 Paraph - signature return stroke', dict(end='paraph', gap_nI=100), {}, 'jewel'),
    ('4 Monoline pen signature', dict(slant=22, gap_nI=100), dict(mode='mono', hair=6.5), 'crook'),
    ('5 Broad-nib italic', dict(slant=10, gap_nI=104), dict(mode='broad', nib_angle=38, hair=3.0, shade=18), 'canopy'),
    ('6 Upright couture, wave I', dict(slant=8, i_top='wave', v_entry='clean', U=64, gap_nI=110), dict(hair=3.6, shade=18.5), 'footwrap'),
]


def cell(name, cfg, pen_kw, mono_kind, fname):
    S, c = word2.build(cfg)
    kw = dict(slant=c['slant'], hair=4.2, shade=17.0)
    kw.update(pen_kw)
    pen = P.Pen(**kw)
    wpath = P.render(S, pen)
    mcfg = dict(cfg)
    M = getattr(mono, 'm_' + mono_kind)(mcfg)
    mpath = P.render(M, pen)
    W, H = 1000, 600
    body = place(wpath, (50, 40, 900, 300))
    body += place(mpath, (60, 370, 200, 200))
    body += label(name, 300, 470, 26, '#333')
    body += label('monogram: ' + mono_kind, 300, 510, 20)
    svg = P.vtype.svg_doc(W, H, body, bg=IVORY)
    open(fname, 'w').write(svg)
    return fname


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'explore'), exist_ok=True)
    files = []
    for i, (name, cfg, pk, mk) in enumerate(VARIANTS):
        files.append(cell(name, cfg, pk, mk, os.path.join(HERE, 'explore', f'e{i + 1}.svg')))
    subprocess.run(['node', RENDER, 'sheet', os.path.join(HERE, 'explore.png')] + files, check=True)
    print('done')
