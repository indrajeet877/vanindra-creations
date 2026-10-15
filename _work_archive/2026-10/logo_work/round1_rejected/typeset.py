"""Shape text with HarfBuzz and emit SVG path data (text converted to outlines)."""
import io
import os
from functools import lru_cache

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'fonts')


def _fs(pkg, name):
    return os.path.join(FONTS, pkg, 'package', 'files', name)


FONT_FILES = {
    'bodoni': ('bmv', 'bodoni-moda-latin-opsz-normal.woff2', {'opsz': 28, 'wght': 500}),
    'bodoni-display': ('bmv', 'bodoni-moda-latin-opsz-normal.woff2', {'opsz': 60, 'wght': 500}),
    'bodoni-sturdy': ('bmv', 'bodoni-moda-latin-opsz-normal.woff2', {'opsz': 11, 'wght': 650}),
    'bodoni-light': ('bmv', 'bodoni-moda-latin-opsz-normal.woff2', {'opsz': 96, 'wght': 400}),
    'bodoni-italic': ('bmv', 'bodoni-moda-latin-opsz-italic.woff2', {'opsz': 96, 'wght': 400}),
    'cormorant-500': ('fontsource-cormorant-garamond-5.3.0', 'cormorant-garamond-latin-500-normal.woff2', None),
    'cormorant-600': ('fontsource-cormorant-garamond-5.3.0', 'cormorant-garamond-latin-600-normal.woff2', None),
    'cormorant-italic-500': ('fontsource-cormorant-garamond-5.3.0', 'cormorant-garamond-latin-500-italic.woff2', None),
    'jost-300': ('fontsource-jost-5.3.0', 'jost-latin-300-normal.woff2', None),
    'jost-400': ('fontsource-jost-5.3.0', 'jost-latin-400-normal.woff2', None),
    'jost-500': ('fontsource-jost-5.3.0', 'jost-latin-500-normal.woff2', None),
    'cinzel-500': ('fontsource-cinzel-5.3.0', 'cinzel-latin-500-normal.woff2', None),
    'italiana': ('fontsource-italiana-5.3.0', 'italiana-latin-400-normal.woff2', None),
    'marcellus': ('fontsource-marcellus-5.3.0', 'marcellus-latin-400-normal.woff2', None),
}


@lru_cache(maxsize=None)
def load(key):
    pkg, name, axes = FONT_FILES[key]
    tt = TTFont(_fs(pkg, name))
    if axes:
        tt = instancer.instantiateVariableFont(tt, axes)
    tt.flavor = None
    buf = io.BytesIO()
    tt.save(buf)
    data = buf.getvalue()
    tt = TTFont(io.BytesIO(data))
    face = hb.Face(data)
    font = hb.Font(face)
    return tt, font, tt['head'].unitsPerEm


def shape(key, text, size, tracking=0.0, x=0.0, y=0.0, features=None):
    """Return (svg_path_d, advance_width_px). y is the baseline. tracking is in em."""
    tt, font, upem = load(key)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {'kern': True, 'liga': True})
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    pen = SVGPathPen(glyph_set)
    cursor = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        gname = order[info.codepoint]
        gx = x + (cursor + pos.x_offset) * scale
        gy = y - pos.y_offset * scale
        tpen = TransformPen(pen, (scale, 0, 0, -scale, gx, gy))
        glyph_set[gname].draw(tpen)
        cursor += pos.x_advance
        if i < n - 1:
            cursor += tracking * upem
    return pen.getCommands(), cursor * scale


def measure(key, text, size, tracking=0.0):
    return shape(key, text, size, tracking)[1]


def centered(key, text, size, cx, y, tracking=0.0):
    w = measure(key, text, size, tracking)
    return shape(key, text, size, tracking, x=cx - w / 2, y=y)[0], w


def glyph_bbox(key, text, size):
    """Ink bounds (xmin, ymin, xmax, ymax) in px for text at origin baseline, y-down."""
    tt, font, upem = load(key)
    from fontTools.pens.boundsPen import BoundsPen
    d, _ = shape(key, text, size)
    glyph_set = tt.getGlyphSet()
    bp = BoundsPen(glyph_set)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, {'kern': True})
    order = tt.getGlyphOrder(); scale = size / upem; cursor = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        tp = TransformPen(bp, (scale, 0, 0, -scale, cursor * scale, 0))
        glyph_set[order[info.codepoint]].draw(tp)
        cursor += pos.x_advance
    return bp.bounds
