"""Build every logo asset as (w, h, body) for any colour theme, write SVG files and a symbol sheet."""
import json
import os
import sys

DEST = sys.argv[1] if len(sys.argv) > 1 else 'final'
sys.argv = sys.argv[:1] + [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')]
import design as D  # noqa: E402
from design import svg, glyph_center, arch_path, mark_maison, wordmark_maison, mark_editorial, wordmark_editorial, mark_frame, wordmark_frame  # noqa: E402
from typeset import centered  # noqa: E402

SYM = {'bg': 'var(--lb)', 'fg': 'currentColor', 'acc': 'var(--la)'}


def small_maison(t):
    """Heavier arch monogram tuned for 16–64 px (favicon, profile picture)."""
    cx, cy, w, h = 256, 256, 250, 420
    top = cy - h / 2
    v = glyph_center('bodoni-sturdy', 'V', 215, cx, cy + 42)
    dsz, dy = 17, cy - 100
    diamond = f'M{cx},{dy - dsz} L{cx + dsz},{dy} L{cx},{dy + dsz} L{cx - dsz},{dy} Z'
    return (f'<path d="{arch_path(cx, top, w, h)}" fill="none" stroke="{t["fg"]}" stroke-width="22"/>'
            f'<path d="{v}" fill="{t["fg"]}"/><path d="{diamond}" fill="{t["acc"]}"/>')


def small_editorial(t):
    v = glyph_center('cormorant-600', 'V', 300, 262, 262)
    return f'<circle cx="256" cy="256" r="240" fill="{t["fg"]}"/><path d="{v}" fill="{t["bg"]}"/>'


def small_frame(t):
    m, _ = mark_frame(256, 256, 440, t, stroke_ratio=0.045, vscale=0.84)
    return m


def assets(t):
    out = {}
    # Direction A
    out['A_icon'] = (512, 512, mark_maison(256, 256, 2.2, t))
    out['A_icon_small'] = (512, 512, small_maison(t))
    body = mark_maison(40 + 48, 110, 1.0, t)
    wm, w1, _ = wordmark_maison(40 + 96 + 44, 108, 1.0, t)
    out['A_horizontal'] = (40 + 96 + 44 + w1 + 48, 220, body + wm)
    body = mark_maison(260, 150, 1.25, t)
    wm, _, _ = wordmark_maison(260, 340, 1.0, t, align='center')
    out['A_stacked'] = (520, 420, body + wm)
    # Direction B
    out['B_icon'] = (512, 512, mark_editorial(256, 256, 200, t))
    out['B_icon_filled'] = (512, 512, mark_editorial(256, 256, 236, t, filled=True))
    out['B_icon_small'] = (512, 512, small_editorial(t))
    r = 52
    body = mark_editorial(40 + r, 100, r, t)
    wm, total = wordmark_editorial(40 + 2 * r + 34, 128, 84, t)
    out['B_horizontal'] = (40 + 2 * r + 34 + total + 44, 200, body + wm)
    body = mark_editorial(300, 130, 78, t)
    wm, _ = wordmark_editorial(300, 320, 80, t, align='center')
    tag, _ = centered('jost-400', 'CONTENT  STRATEGY  ·  VIRAL  SCRIPTING  ·  STUDIO  EDITING', 11.5, 300, 362, 0.22)
    out['B_stacked'] = (600, 400, body + wm + f'<path d="{tag}" fill="{t["fg"]}" fill-opacity="0.72"/>')
    # Direction C
    m, _ = mark_frame(256, 256, 360, t)
    out['C_icon'] = (512, 512, m)
    out['C_icon_small'] = (512, 512, small_frame(t))
    m, _ = mark_frame(40 + 28, 100, 100, t)
    wm, total = wordmark_frame(40 + 56 + 30, 100 + 34 * 0.36, 34, t)
    out['C_horizontal'] = (40 + 56 + 30 + total + 44, 200, m + wm)
    m, _ = mark_frame(300, 135, 170, t)
    wm, _ = wordmark_frame(300, 300, 30, t, align='center')
    out['C_stacked'] = (600, 360, m + wm)
    return out


NAMES = {'A': 'maison', 'B': 'editorial', 'C': 'frame'}


def write_files(dest):
    os.makedirs(dest, exist_ok=True)
    for tn, t in D.THEMES.items():
        for key, (w, h, body) in assets(t).items():
            d, kind = key.split('_', 1)
            fn = f'{d}_{NAMES[d]}_{kind}_on_{tn}.svg'
            with open(os.path.join(dest, fn), 'w') as f:
                f.write(svg(w, h, body, t['bg'], title=f'VanIndra Creations logo proposal {d} ({NAMES[d]})'))


def write_symbols(path):
    data = {k: {'w': round(w, 2), 'h': round(h, 2), 'body': body} for k, (w, h, body) in assets(SYM).items()}
    with open(path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    dest = DEST
    write_files(dest)
    write_symbols(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'symbols.json'))
    print(len(os.listdir(dest)), 'files')
