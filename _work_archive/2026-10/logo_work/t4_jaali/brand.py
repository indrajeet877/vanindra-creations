"""VanIndra Creations -- 'The Jaali Stroke'. Builds every deliverable from one 22.5-degree construction."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit, rosette, K83

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'


def place(path, x, y, s):
    return vt.transform(path, s, 0, 0, s, x, y)


def norm_mark(t=10.0):
    """unit V scaled so that its height = 1.0 and its tip is at (0, 1)."""
    m = unit(R=100.0, t=t)
    x0, y0, x1, y1 = vt.bounds(m)
    s = 1.0 / (y1 - y0)
    return vt.transform(m, s, 0, 0, s, -((x0 + x1) / 2) * s, -y0 * s)


def word(text, family, weight, cap, tracking=0.0, pairs=None, x=0.0, baseline=0.0):
    """outlined text with cap height = cap, optional per-pair kerning (in cap units)."""
    gl = vt.glyph_paths(text, family=family, weight=weight, size=100)
    # cap height from 'H'
    H = vt.glyph_paths('H', family=family, weight=weight, size=100)[0].bounds
    capu = H[3] - H[1]
    s = cap / capu
    out = []
    pen = 0.0
    orig = 0.0
    for i, g in enumerate(gl):
        out.append(vt.transform(g.path, s, 0, 0, s, x + (pen - orig) * s, baseline))
        adv = g.width
        orig += adv
        k = 0.0
        if pairs and i < len(text) - 1:
            k = pairs.get(text[i:i + 2], 0.0) * capu
        pen += adv + tracking * 100 + k
    return merge(out)


def _profiles(path, y0, y1, n=48, clamp=None):
    """left/right x-extent of a glyph on n scanlines between y0..y1 (SVG y-down). None where empty."""
    L, Rr = [], []
    h = (y1 - y0) / n
    for i in range(n):
        y = y0 + (i + 0.5) * h
        strip = P([(-1e4, y - h * 0.25), (1e4, y - h * 0.25), (1e4, y + h * 0.25), (-1e4, y + h * 0.25)])
        q = inter(path, strip)
        b = vt.bounds(q)
        if b == (0, 0, 0, 0) or b[2] - b[0] <= 0:
            L.append(None); Rr.append(None)
        else:
            L.append(b[0]); Rr.append(b[2])
    if clamp is not None:
        lv = [v for v in L if v is not None]; rv = [v for v in Rr if v is not None]
        if lv:
            m = min(lv); L = [None if v is None else min(v, m + clamp) for v in L]
        if rv:
            m = max(rv); Rr = [None if v is None else max(v, m - clamp) for v in Rr]
    return L, Rr


def optical_word(text, family, weight, cap, gap, x=0.0, baseline=0.0, clamp=0.30, adjust=None, n=40):
    """Outlined word with optical spacing: every adjacent pair gets the same mean white gap (in cap units).
    adjust: {'AV': +0.02, ...} fine corrections in cap units."""
    Hb = vt.glyph_paths('H', family=family, weight=weight, size=100)[0].bounds
    capu = Hb[3] - Hb[1]
    s = cap / capu
    glyphs = []
    orig = 0.0
    for g in vt.glyph_paths(text, family=family, weight=weight, size=100):
        p = vt.transform(g.path, s, 0, 0, s, -orig * s, baseline)
        orig += g.width
        glyphs.append(p)
    y0, y1 = baseline - cap, baseline
    profs = [_profiles(p, y0, y1, n=n, clamp=clamp * cap) for p in glyphs]
    out = []
    cur = x - vt.bounds(glyphs[0])[0]
    out.append(vt.transform(glyphs[0], 1, 0, 0, 1, cur, 0))
    for i in range(1, len(glyphs)):
        RA = profs[i - 1][1]; LB = profs[i][0]
        diffs = [ra - lb for ra, lb in zip(RA, LB) if ra is not None and lb is not None]
        # rows where only one glyph exists: use the clamp limit (open counters such as A/V corners)
        md = sum(diffs) / len(diffs)
        k = adjust.get(text[i - 1:i + 1], 0.0) * cap if adjust else 0.0
        cur = cur + md + gap * cap + k
        out.append(vt.transform(glyphs[i], 1, 0, 0, 1, cur, 0))
    return merge(out)
