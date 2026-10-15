"""Round-5: 'Threaded' — small-cap I threaded through the V's hairline arm (thin passes over thick)."""
import os
import subprocess
from mono import *  # noqa
from explore import didone_V, didone_I, H


def threaded(L=450, R=470, thick=190, thin=30, d=225, stem=140, itop=830, sw=70, gap=20, os_=16,
             vserif=True, iserif=True):
    V, g = didone_V(L=L, R=R, thick=thick, thin=thin, os_=os_, serifs=vserif)
    I = didone_I(d, 0, itop, stem=stem, sw=sw, head=iserif, foot=iserif)
    P, B, B2, J = g['P'], g['B'], g['B2'], g['J']
    hair = intersection(V, poly([P, B, B2, J]))
    I = over(hair, I, gap)
    return union(V, I), g


def info(g, d, stem, R, H=1000):
    pass


VARS = [
    ('a I 0.83, centre-right', dict()),
    ('b I 0.78, further right', dict(d=262, itop=780, R=480)),
    ('c I 0.88, slimmer', dict(d=215, itop=880, stem=124, sw=62, R=490)),
    ('d wider V, I 0.80', dict(L=500, R=520, d=250, itop=800)),
    ('e I 0.72 small cap', dict(d=230, itop=720, stem=128, sw=62)),
    ('f heavier I', dict(d=232, stem=168, itop=820, sw=72)),
    ('g no V serifs', dict(vserif=False)),
    ('h condensed V', dict(L=380, R=400, thick=170, d=190, stem=120, itop=820, sw=58)),
    ('i light hairline gap', dict(gap=14)),
]

if __name__ == '__main__':
    files = []
    OUT = os.path.join(HERE, 'explore')
    for i, (name, kw) in enumerate(VARS):
        shape, g = threaded(**kw)
        p = to_svg_space(shape)
        S = 600
        big, _ = place(p, 110, 70, 380, 400)
        small = []
        for k, sz in enumerate((48, 24, 16)):
            sp, _ = place(p, 150 + k * 90, 505, sz, sz)
            small.append(path_el(sp, EMERALD))
        lab = vtype.text_path(name, family='jost', weight=400, size=22, x=24, y=578)
        body = path_el(big, EMERALD) + ''.join(small) + path_el(lab.path, '#777')
        fn_ = os.path.join(OUT, f'r5_{i + 1}.svg')
        write_svg(fn_, S, S, body, bg=IVORY)
        files.append(fn_)
    subprocess.run(['node', os.path.join(HERE, '..', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore_r5.png')] + files, check=True)
    print('ok')
