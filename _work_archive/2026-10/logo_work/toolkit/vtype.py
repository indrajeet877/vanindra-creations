"""VanIndra logo toolkit: text -> vector outlines, boolean path ops, SVG helpers.

Run scripts with:  /tmp/.../scratchpad/logo_venv/bin/python your_script.py
and put   sys.path.insert(0, '<scratchpad>/logo2/toolkit')   at the top.

Key functions
-------------
font_file(family, weight=400, style='normal', subset='latin') -> path to a .woff2 in logo2/fonts
text_path(text, family=..., weight=..., style=..., subset=..., size=100, x=0, y=0, tracking=0.0, variations=None, features=None)
    -> TextResult(d=<svg path d>, width=<advance px>, path=<pathops.Path>, bounds=(xmin,ymin,xmax,ymax))
    y is the BASELINE; coordinates are SVG y-down. tracking is in em.
glyph_paths(...) -> list of per-glyph TextResult (same args as text_path) for manipulating letters individually
union(*paths) / difference(a, b) / intersection(a, b) / xor(a, b)  -> pathops.Path
to_d(path) -> SVG path d string;  from_d(d) -> pathops.Path (supports M L H V C Q Z, absolute and relative; no arcs)
transform(path, a, b, c, d, e, f) -> new Path (affine, SVG matrix order)
stroke_to_path(path, width, cap='butt', join='miter') -> filled outline of a stroke (for boolean ops on strokes)
bounds(path) -> (xmin, ymin, xmax, ymax)
svg_doc(w, h, body, bg=None, title='VanIndra Creations') -> full SVG string
"""
import io
import os
import re
from dataclasses import dataclass
from functools import lru_cache

import pathops
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.normpath(os.path.join(HERE, '..', 'fonts'))

PALETTE = {
    'emerald': '#0B2A20',   # deep emerald ink (primary dark)
    'emerald_2': '#0E6B4E', # brighter studio emerald (use sparingly)
    'ivory': '#F6F1E7',     # warm ivory paper
    'white': '#FFFFFF',
    'gold': '#A8843A',      # antique gold on light grounds
    'gold_lt': '#D2B26A',   # soft gold on dark grounds
}


def font_file(family, weight=400, style='normal', subset='latin'):
    """Locate a static woff2, e.g. font_file('cormorant-garamond', 500, 'italic')."""
    d = os.path.join(FONT_DIR, family)
    if not os.path.isdir(d):
        raise FileNotFoundError(f'no font family {family!r}; available: {sorted(os.listdir(FONT_DIR))}')
    name = f'{family}-{subset}-{weight}-{style}.woff2'
    p = os.path.join(d, name)
    if os.path.exists(p):
        return p
    opts = sorted(f for f in os.listdir(d) if f.endswith('.woff2'))
    raise FileNotFoundError(f'{name} not found; options: {opts[:40]}')


def bodoni_variable(style='normal'):
    return os.path.join(FONT_DIR, 'bodoni-moda-variable', 'package', 'files', f'bodoni-moda-latin-opsz-{style}.woff2')


@lru_cache(maxsize=None)
def _load(path, variations_key=None):
    tt = TTFont(path)
    if variations_key:
        from fontTools.varLib import instancer
        tt = instancer.instantiateVariableFont(tt, dict(variations_key))
    tt.flavor = None
    buf = io.BytesIO()
    tt.save(buf)
    data = buf.getvalue()
    tt = TTFont(io.BytesIO(data))
    font = hb.Font(hb.Face(data))
    return tt, font, tt['head'].unitsPerEm


class _PathopsPen(BasePen):
    def __init__(self, glyphset, path):
        super().__init__(glyphset)
        self.p = path

    def _moveTo(self, pt):
        self.p.moveTo(*pt)

    def _lineTo(self, pt):
        self.p.lineTo(*pt)

    def _curveToOne(self, p1, p2, p3):
        self.p.cubicTo(*p1, *p2, *p3)

    def _qCurveToOne(self, p1, p2):
        self.p.quadTo(*p1, *p2)

    def _closePath(self):
        self.p.close()


@dataclass
class TextResult:
    d: str
    width: float
    path: object
    bounds: tuple


def _resolve(family, weight, style, subset, file):
    if file:
        return file
    return font_file(family, weight, style, subset)


def glyph_paths(text, family='cormorant-garamond', weight=400, style='normal', subset='latin', size=100, x=0.0, y=0.0,
                tracking=0.0, variations=None, features=None, file=None):
    path_file = _resolve(family, weight, style, subset, file)
    vkey = tuple(sorted(variations.items())) if variations else None
    tt, font, upem = _load(path_file, vkey)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {'kern': True, 'liga': True})
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    cursor = 0.0
    out = []
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        gname = order[info.codepoint]
        gx = x + (cursor + pos.x_offset) * scale
        gy = y - pos.y_offset * scale
        p = pathops.Path()
        gs[gname].draw(TransformPen(_PathopsPen(gs, p), (scale, 0, 0, -scale, gx, gy)))
        adv = pos.x_advance * scale
        out.append(TextResult(to_d(p), adv, p, bounds(p)))
        cursor += pos.x_advance
        if i < n - 1:
            cursor += tracking * upem
    return out


def text_path(text, **kw):
    glyphs = glyph_paths(text, **kw)
    size = kw.get('size', 100)
    tracking = kw.get('tracking', 0.0)
    total = sum(g.width for g in glyphs) + tracking * size * max(len(glyphs) - 1, 0)
    p = union(*[g.path for g in glyphs]) if glyphs else pathops.Path()
    return TextResult(to_d(p), total, p, bounds(p))


def measure(text, **kw):
    return text_path(text, **kw).width


def bounds(path):
    try:
        return tuple(path.bounds)
    except Exception:
        return (0, 0, 0, 0)


def union(*paths):
    paths = [p for p in paths if p is not None]
    if not paths:
        return pathops.Path()
    return pathops.op(paths[0], paths[0], pathops.PathOp.UNION) if len(paths) == 1 else _reduce(paths, pathops.PathOp.UNION)


def _reduce(paths, op):
    acc = paths[0]
    for p in paths[1:]:
        acc = pathops.op(acc, p, op)
    return acc


def difference(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def intersection(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def xor(a, b):
    return pathops.op(a, b, pathops.PathOp.XOR)


def to_d(path):
    pen = SVGPathPen(None)
    path.draw(pen)
    return pen.getCommands()


_TOK = re.compile(r'[MmLlHhVvCcQqZz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?')


def from_d(d):
    """Parse an SVG path (M L H V C Q Z, abs/rel; no arcs/S/T) into a pathops.Path."""
    toks = _TOK.findall(d)
    p = pathops.Path()
    i, cmd = 0, None
    cx = cy = sx = sy = 0.0

    def num():
        nonlocal i
        v = float(toks[i]); i += 1
        return v
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]; i += 1
            if cmd in 'Zz':
                p.close(); cx, cy = sx, sy
                continue
        rel = cmd.islower()
        c = cmd.upper()
        if c == 'M':
            x, y = num(), num()
            if rel: x, y = x + cx, y + cy
            p.moveTo(x, y); cx, cy = sx, sy = x, y
            cmd = 'l' if rel else 'L'
        elif c == 'L':
            x, y = num(), num()
            if rel: x, y = x + cx, y + cy
            p.lineTo(x, y); cx, cy = x, y
        elif c == 'H':
            x = num(); x = x + cx if rel else x
            p.lineTo(x, cy); cx = x
        elif c == 'V':
            y = num(); y = y + cy if rel else y
            p.lineTo(cx, y); cy = y
        elif c == 'C':
            a = [num() for _ in range(6)]
            if rel: a = [a[k] + (cx if k % 2 == 0 else cy) for k in range(6)]
            p.cubicTo(*a); cx, cy = a[4], a[5]
        elif c == 'Q':
            a = [num() for _ in range(4)]
            if rel: a = [a[k] + (cx if k % 2 == 0 else cy) for k in range(4)]
            p.quadTo(*a); cx, cy = a[2], a[3]
        else:
            raise ValueError(f'unsupported command {cmd}')
    return p


def transform(path, a, b, c, d, e, f):
    out = pathops.Path()
    pen = TransformPen(_PathopsPen(None, out), (a, b, c, d, e, f))
    path.draw(pen)
    return out


def stroke_to_path(path, width, cap='butt', join='miter', miter_limit=10):
    p = pathops.Path(path)
    caps = {'butt': pathops.LineCap.BUTT_CAP, 'round': pathops.LineCap.ROUND_CAP, 'square': pathops.LineCap.SQUARE_CAP}
    joins = {'miter': pathops.LineJoin.MITER_JOIN, 'round': pathops.LineJoin.ROUND_JOIN, 'bevel': pathops.LineJoin.BEVEL_JOIN}
    p.stroke(width, caps[cap], joins[join], miter_limit)
    return union(p)


def svg_doc(w, h, body, bg=None, title='VanIndra Creations'):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')
