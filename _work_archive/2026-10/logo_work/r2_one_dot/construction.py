"""One Dot construction card: the idea, visible in the drawing (not only here)."""
import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from build import *
import vtype
from build import *

GUIDE = '#C9B79A'
LABEL = '#5E6B63'


def label(txt, x, y, size=26, col=LABEL, weight=500, anchor='start'):
    t = vtype.text_path(txt, family='manrope', weight=weight, size=size, x=0, y=0)
    if anchor == 'end':
        x -= t.width
    elif anchor == 'middle':
        x -= t.width / 2
    p = vtype.transform(t.path, 1, 0, 0, 1, x, y)
    return f'<path d="{fmt(to_d(p))}" fill="{col}"/>'


def main():
    Pm = master()
    W, H = 2400, 1540
    s = 0.46
    ox, oy = 150, 520            # Latin baseline origin (svg)
    lw = set_word('vanindra', Pm)
    body = ''
    # guides: baseline, x-height (the line), ascender/dot top
    def hline(y, x0=60, x1=W - 60, dash=None, col=GUIDE, w=2):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'
    yb = oy
    yx = oy - Pm.X * s
    ya = oy - Pm.asc * s
    body += hline(yb, x1=ox + lw['width'] * s + 40, dash='6 8')
    body += hline(yx, x1=ox + lw['width'] * s + 40, col='#B08A3E', w=2.5)
    body += hline(ya, x1=ox + lw['width'] * s + 40, dash='6 8')
    # Devanagari placed with its anusvara on the same vertical axis
    f = 1.0
    Pd = deva_for_scale(Pm, f)
    hw = set_hindi(Pd)
    dxl = lw['dots'][0][0] - hw['dots'][0][0] * f
    oy2 = oy + 560
    yh = oy2 - Pd.H * f * s
    body += hline(yh, x0=ox + (dxl - 80) * s, x1=ox + lw['width'] * s + 40, col='#B08A3E', w=2.5)
    body += hline(oy2, x0=ox + (dxl - 80) * s, x1=ox + lw['width'] * s + 40, dash='6 8')
    # dot axis
    ax = ox + lw['dots'][0][0] * s
    body += f'<line x1="{ax:.1f}" x2="{ax:.1f}" y1="{ya-30:.1f}" y2="{oy2+150:.1f}" stroke="#B08A3E" stroke-width="2.5" stroke-dasharray="2 7"/>'
    ink = Ink()
    add_word(ink, lw['path'], [dot(Pm, *lw['dots'][0])], s, ox, oy, EMERALD, GOLD)
    hp = transform(hw['path'], f, 0, 0, f, 0, 0)
    hd = transform(dot(Pd, *hw['dots'][0]), f, 0, 0, f, 0, 0)
    add_word(ink, hp, [hd], s, ox + dxl * s, oy2, EMERALD, GOLD)
    body += ink.body()
    # labels (left column notes)
    rx = ox + lw['width'] * s + 70
    body += label('one line: every Latin top is flat on the x-height', rx, yx + 9)
    body += label('the dot’s top = the ascender line', rx, ya + 9)
    body += label('the same line, drawn: the shirorekha', rx, yh + 9)
    body += label('baseline', rx, yb + 9, col='#9AA39D')
    body += label('one dot, one axis: it falls over “ni” in both scripts', ax + 24, oy2 + 120, size=26, col='#8C6A2A')
    # pairs row: one arch / one bowl / one pair of diagonals / one dot
    py = 1395
    px = 150
    sc = 0.27
    rN = d_i_na(Pd, 0, with_bindu=False)
    rI = d_i_na(Pd, 0)
    hl = lambda x1: rect(-Pd.hl_over * 0.6, Pd.H - Pd.Th, x1, Pd.H)
    pairs = [
        ('n', 'one arch: n  /  i-matra', union(rN['path'], hl(rN['x1'] + 14)), []),
        ('a', 'one bowl: a  /  va', union(d_va(Pd, 0)['path'], hl(d_va(Pd, 0)['x1'] + 14)), []),
        ('v', 'one pair of diagonals: v  /  ra', union(d_dra(Pd, 0)['path'], hl(Pd.daW + 14)), []),
        ('i', 'one dot: tittle  /  anusvara', union(rI['path'], hl(rI['x1'] + 14)), [dot(Pd, *rI['dot'])]),
    ]
    for ch, what, part, pdots in pairs:
        g = LATIN[ch](Pm)
        dots = [dot(Pm, *g['dot'])] if g.get('dot') else []
        ink2 = Ink()
        add_word(ink2, g['path'], dots, sc, px, py, EMERALD, GOLD)
        add_word(ink2, part, pdots, sc * f, px + (g['w'] + 110) * sc, py + Pd.Th * 0 * sc, EMERALD, GOLD)
        body += ink2.body()
        body += label(what, px, py + 75, size=23)
        px += 560
    body += label('Latin and Devanagari drawn as one system: same stems, same contrast, flat tops, round bottoms, one gold dot.', 150, 120, size=30, col='#2E3B35', weight=600)
    body += label('Devanagari drawn in the same system; to be verified by the team (the da-ra conjunct and every letter shape).', 150, 165, size=24)
    open('work/construction.svg', 'w').write(svg_doc(W, H, body, bg=IVORY))
    subprocess.run(['node', 'pngx.js', 'work/construction.svg', 'construction.png', '2400'], check=True)


main()
