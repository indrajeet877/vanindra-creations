"""Wordmark builder: per-glyph placement with tracking + optical pair adjustments (all outlined)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import *  # noqa: F401,F403,E402
from vtype import glyph_paths, bodoni_variable  # noqa: E402

BODONI = bodoni_variable()


def setline(text, size, tracking, pairs=None, **font):
    """Lay out text glyph by glyph: advance + tracking*size + pairs[(a,b)]*size. Returns (Path, width)."""
    pairs = pairs or {}
    gl = glyph_paths(text, size=size, x=0, y=0, **font)
    out, x = [], 0.0
    for k, (ch, g) in enumerate(zip(text, gl)):
        # glyph_paths positions glyphs with their own advances; re-place each glyph at x
        gx0 = sum(gg.width for gg in gl[:k])
        out.append(transform(g.path, 1, 0, 0, 1, x - gx0, 0))
        adv = g.width
        if k < len(text) - 1:
            adv += tracking * size + pairs.get((ch, text[k + 1]), 0.0) * size
        x += adv
    p = union(*out)
    x0, _, x1, _ = bounds(p)
    return transform(p, 1, 0, 0, 1, -x0, 0), x1 - x0


VAN_PAIRS = {('V', 'A'): -0.07, ('A', 'N'): -0.015, ('R', 'A'): -0.045, ('D', 'R'): 0.0, ('N', 'I'): 0.0,
             ('I', 'N'): 0.0, ('N', 'D'): 0.0}
CRE_PAIRS = {('C', 'R'): 0.0, ('R', 'E'): 0.0, ('E', 'A'): -0.02, ('A', 'T'): -0.06, ('T', 'I'): -0.01,
             ('O', 'N'): 0.0}

OPTIONS = {
    'bodoni_jost': dict(
        main=dict(text='VANINDRA', tracking=0.13, pairs=VAN_PAIRS, file=BODONI, variations={'wght': 500, 'opsz': 96}),
        sub=dict(text='CREATIONS', tracking=0.62, pairs=CRE_PAIRS, family='jost', weight=400)),
    'bodoni_bodoni': dict(
        main=dict(text='VANINDRA', tracking=0.13, pairs=VAN_PAIRS, file=BODONI, variations={'wght': 450, 'opsz': 96}),
        sub=dict(text='CREATIONS', tracking=0.55, pairs=CRE_PAIRS, file=BODONI, variations={'wght': 500, 'opsz': 11})),
    'jost_jost': dict(
        main=dict(text='VANINDRA', tracking=0.30, pairs=VAN_PAIRS, family='jost', weight=300),
        sub=dict(text='CREATIONS', tracking=0.62, pairs=CRE_PAIRS, family='jost', weight=400)),
    'cormorant_jost': dict(
        main=dict(text='VANINDRA', tracking=0.14, pairs=VAN_PAIRS, family='cormorant-garamond', weight=500),
        sub=dict(text='CREATIONS', tracking=0.62, pairs=CRE_PAIRS, family='jost', weight=400)),
    'tenor_tenor': dict(
        main=dict(text='VANINDRA', tracking=0.26, pairs=VAN_PAIRS, family='tenor-sans', weight=400),
        sub=dict(text='CREATIONS', tracking=0.62, pairs=CRE_PAIRS, family='tenor-sans', weight=400)),
}


def wordmark(opt, cap=100.0, sub_ratio=0.30, gap_ratio=0.62, align='justify'):
    """Main line with cap height `cap`; sub line with cap height cap*sub_ratio, placed gap_ratio*cap below baseline.
    align='justify' stretches sub tracking so both lines share the same width."""
    o = OPTIONS[opt] if isinstance(opt, str) else opt
    m = dict(o['main'])
    s = dict(o['sub'])
    # measure cap height of the font at size 100 using 'H'
    def cap_of(fontkw):
        kw = {k: v for k, v in fontkw.items() if k not in ('text', 'tracking', 'pairs')}
        p = glyph_paths('H', size=100, **kw)[0].path
        b = bounds(p)
        return (b[3] - b[1]) / 100.0
    msize = cap / cap_of(m)
    mp, mw = setline(m.pop('text'), msize, m.pop('tracking'), m.pop('pairs'), **m)
    scap = cap * sub_ratio
    ssize = scap / cap_of(s)
    stext, strk, spairs = s.pop('text'), s.pop('tracking'), s.pop('pairs')
    sp, sw = setline(stext, ssize, strk, spairs, **s)
    if align == 'justify':
        # solve tracking so sw == mw
        extra = (mw - sw) / (len(stext) - 1) / ssize
        sp, sw = setline(stext, ssize, strk + extra, spairs, **s)
        sx = 0
    else:
        sx = (mw - sw) / 2
    sy = cap * gap_ratio + scap
    sp = transform(sp, 1, 0, 0, 1, sx, sy)
    both = union(mp, sp)
    return dict(main=mp, sub=sp, all=both, width=max(mw, sw), cap=cap, bottom=sy)
