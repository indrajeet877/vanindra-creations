import sys
sys.path.insert(0,'.')
from surgery import *
EM='#0B2A20'; IV='#F6F1E7'; GD='#A8843A'; GL='#D2B26A'
V=[
 ('E1 Fraunces 400 · single hinge, I at cap', dict(font='fraunces', weight=400, mode='single')),
 ('E2 Fraunces 400 · double hinge nIn', dict(font='fraunces', weight=400, mode='double')),
 ('E3 Fraunces 500 · double, I rises 1.18x (sky)', dict(font='fraunces', weight=500, mode='double', i_top=1.18)),
 ('E4 Cormorant Garamond 600 · single, I rises 1.25x', dict(font='cormorant-garamond', weight=600, mode='single', i_top=1.25)),
 ('E5 Playfair 500 · double, wide hairline horizon head', dict(font='playfair-display', weight=500, mode='double', i_top=1.12, head_scale=1.8)),
 ('E6 Tenor Sans · double, slab-capped I', dict(font='tenor-sans', weight=400, mode='double', i_top=1.1, sans_head=(34,7))),
 ('E7 Libre Caslon Display · double, I tall 1.3x', dict(font='libre-caslon-display', weight=400, mode='double', i_top=1.3)),
 ('E8 DM Serif Display · double, gold I', dict(font='dm-serif-display', weight=400, mode='double', i_top=1.12, gold=True)),
 ('E9 Fraunces 400 · double, gold I, rises 1.1x', dict(font='fraunces', weight=400, mode='double', i_top=1.1, gold=True)),
]
W=1500; tile_h=300; cols=1
body=''; y=0
for i,(label,kw) in enumerate(V):
    r=build(size=150, **kw)
    b=vt.bounds(r['ink'])
    ox=60-b[0]; oy=y+210
    bg=IV
    body+=f'<rect x="0" y="{y}" width="{W}" height="{tile_h}" fill="{bg}" stroke="#ccc"/>'
    body+=f'<path d="{vt.to_d(r["ink"])}" fill="{EM}" transform="translate({ox:.1f},{oy:.1f})"/>'
    if r['gold'] is not None:
        body+=f'<path d="{vt.to_d(r["gold"])}" fill="{GD}" transform="translate({ox:.1f},{oy:.1f})"/>'
    # hinge glyph: big on emerald disc + small sizes
    h=r['hinge']; hb=vt.bounds(h); hw=hb[2]-hb[0]; hh=hb[3]-hb[1]
    for (cxp, R) in [(1060,105),(1260,40),(1350,20),(1410,10)]:
        sc = (R*1.25)/max(hw,hh)
        tx = cxp - (hb[0]+hw/2)*sc; ty = y+150 - (hb[1]+hh/2)*sc
        body+=f'<circle cx="{cxp}" cy="{y+150}" r="{R}" fill="{EM}"/>'
        body+=f'<path d="{vt.to_d(h)}" fill="{IV}" transform="translate({tx:.2f},{ty:.2f}) scale({sc:.4f})"/>'
        if r['gold'] is not None:
            body+=f'<path d="{vt.to_d(r["gold"])}" fill="{GL}" transform="translate({tx:.2f},{ty:.2f}) scale({sc:.4f})"/>'
    body+=f'<text x="60" y="{y+275}" font-family="sans-serif" font-size="18" fill="#555">{label}</text>'
    y+=tile_h
open('work/explore1.svg','w').write(vt.svg_doc(W,y,body))
