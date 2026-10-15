"""Build every SVG deliverable for F2 'The Hinge' (finalist polish)."""
import sys, re, math
sys.path.insert(0, '.')
from vitype import *
from deva import DP, vanindra_deva

EM = '#0B2A20'; IV = '#F6F1E7'; GD = '#A8843A'; GL = '#D2B26A'; WH = '#FFFFFF'
OUT = '.'

# optical cuts
pd = P(**DISPLAY)                                     # lockups, wordmark, print
ps = P(**SMALL)                                       # header, Reel credit, avatar
DESC = dict(S=86, Sc=90, H=29, Ht=33, Hb=32, ft=24, fe=28, fb=15, it=26, ie=30, tw=52, Ck=1.0, ebar=0.47, ebk=0.86, sk=0.90)   # 'Creations' at 58 %: ~+10 % optical compensation
pc = P(**DESC)
FAV = dict(SMALL, Sc=122, H=58, it=40, fb=12)         # (retired) favicon V
pf = P(**FAV)
# ICON cut (F2): the hinge symbol for the avatar, favicon and app icon - heavier stems, thick arch top, thick slabs
ICON = dict(S=116, Sc=122, H=48, Ht=58, Hb=56, ft=40, fe=30, fb=10, he=40, hd=46, ie=27, it=38, cw=240, tw=62)
pi = P(**ICON)
CR_RATIO = 0.58                                       # Creations cap height = 58 % of the name's


def rnd(d, nd=1):
    return re.sub(r'-?\d+\.\d+', lambda m: f'{float(m.group()):.{nd}f}'.rstrip('0').rstrip('.'), d)


def bbox(*ps_):
    bs = [vt.bounds(p) for p in ps_ if p is not None]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def write(name, s):
    open(f'{OUT}/{name}', 'w').write(s)


def body(parts, s, dx, dy):
    return ''.join(f'<path d="{rnd(to_svg_d(p, s, dx, dy))}" fill="{c}"/>' for p, c in parts if p is not None)


def fit(parts, W=None, H=None, padx=0, pady=0, unit=0.5, bg=None, title='VanIndra Creations'):
    """artwork at `unit` px per design unit, with padding (design units)."""
    b = bbox(*[p for p, c in parts])
    w = (b[2] - b[0] + 2 * padx) * unit; h = (b[3] - b[1] + 2 * pady) * unit
    dx = (padx - b[0]) * unit; dy = (pady + b[3]) * unit
    return vt.svg_doc(round(w, 1), round(h, 1), body(parts, unit, dx, dy), bg=bg, title=title)


def square(parts, size=1000, fill=0.80, bg=None, title='VanIndra Creations', circle=None):
    """centre artwork in a square. circle: keep every point inside a circle of this fraction of the size."""
    allp = U(*[p for p, c in parts])
    b = vt.bounds(allp)
    s = size * fill / max(b[2] - b[0], b[3] - b[1])
    cx = (b[0] + b[2]) / 2; cy = (b[1] + b[3]) / 2
    if circle:
        pts = [pt for c in allp.contours for pt in c.points]
        far = max(math.hypot(x - cx, y - cy) for x, y in pts)
        s = min(s, size / 2 * circle / far)
    dx = size / 2 - cx * s; dy = size / 2 + cy * s
    return vt.svg_doc(size, size, body(parts, s, dx, dy), bg=bg, title=title)


# ---------------------------------------------------------------- geometry
ST = staircase(pd)            # display staircase
STS = staircase(ps)           # small-cut staircase
WM = wordmark_text(pd)        # one-line wordmark (display cut): n and I side by side, gold I marks the join
WT = wordmark_text(ps)        # one-line text cut (small)
CR = creations(pc)
DV_P = DP(); DV = vanindra_deva(DV_P)
# lighter cut of the Devanagari for the bilingual lockup (danda ~ Latin stem once scaled)
DPL = DP(S=65, h=24, hl=32, tw=43); DVL = vanindra_deva(DPL)
SYM = hinge_symbol(ps)                         # the symbol, full I (mark.svg, one-colour marks)
SYMI = hinge_symbol(pi, L=1400)                # icon cut, long pin that runs off the edge (avatar, tile)
SYMS = hinge_symbol(pi, L=pi.X * 1.0)          # icon cut, short pin with its foot (mark_small, transparent)


def stair_parts(st, ink, icol):
    return [(st['van'], ink), (st['I'], icol), (st['indra'], ink)]


def creations_placed(st, x_mode='right_of_indra', ratio=CR_RATIO, p=pd):
    crb = vt.bounds(CR['ink']); s = ratio
    idb = vt.bounds(st['indra'])
    if x_mode == 'right_of_indra':            # horizontal: on line 2, after Indra, same baseline
        return T(T(CR['ink'], -crb[0], 0, s, s), idb[2] + p.X * 0.58, -st['L'])
    # stacked: third line, right-aligned to Indra
    y = -st['L'] - (p.X * 0.60 + p.C * s)
    x = idb[2] - (crb[2] - crb[0]) * s
    return T(T(CR['ink'], -crb[0], 0, s, s), x, y)


def lockup_horizontal(ink, icol, bg, unit=0.5):
    parts = stair_parts(ST, ink, icol) + [(creations_placed(ST, 'right_of_indra'), ink)]
    return fit(parts, padx=pd.X * 1.0, pady=pd.X * 0.9, unit=unit, bg=bg)


def lockup_stacked(ink, icol, bg, unit=0.5):
    parts = stair_parts(ST, ink, icol) + [(creations_placed(ST, 'stacked'), ink)]
    return fit(parts, padx=pd.X * 1.15, pady=pd.X * 1.0, unit=unit, bg=bg)


def deva_placed(clear=60):
    """वनिंद्रा under the one-line wordmark (F2).
    - axis: the gold ि stem sits on the same vertical as the gold I, so the gold reads as one line through both
      scripts (the bilingual idea, made visible);
    - size: the Hindi headline height equals the Latin cap height (700);
    - weight: drawn in a lighter cut (DPL) so a danda ~ the Latin lowercase stem;
    - clear: gap between the Latin baseline and the top of the ि hook (design units)."""
    b = bbox(WM['ink'], WM['I']); db = bbox(DVL['ink'], DVL['i'], DVL['bindu'])
    ib = vt.bounds(WM['I']); axis = (ib[0] + ib[2]) / 2
    s = pd.C / DPL.HB                                  # Hindi headline height = Latin cap height
    x = axis - DVL['istem'] * s
    hook_top = vt.bounds(DVL['i'])[3]
    y = -clear - hook_top * s
    tr = lambda q: T(T(q, 0, 0, s, s), x, y)
    return tr(DVL['ink']), tr(DVL['i']), tr(DVL['bindu'])


def lockup_bilingual(ink, icol, bg, unit=0.5):
    dk, di, dbd = deva_placed()
    parts = [(WM['ink'], ink), (WM['I'], icol), (dk, ink), (di, icol), (dbd, ink)]
    return fit(parts, padx=pd.X * 1.1, pady=pd.X * 0.9, unit=unit, bg=bg,
               title='VanIndra Creations — bilingual (Devanagari to be verified by the team)')


def sym_parts(h, ink, gold):
    return [(h['n'], ink), (h['pin'], gold)]


def bleed(h, p, ink, gold, bg, xh=0.40, cyk=0.40, size=1000, rx=0, title='VanIndra Creations — the hinge'):
    """The hinge set large in a square (made for the circle crop): the n's x-height = xh of the size, its centre at
    cyk of the height; the gold pin runs down and off the bottom edge (it continues into Indra)."""
    nb = vt.bounds(h['n']); pb = vt.bounds(h['pin'])
    s = size * xh / p.X
    x0 = nb[0]; x1 = max(nb[2], pb[2] - p.ie)                # optical: centre on the n plus the pin stem
    dx = size / 2 - (x0 + x1) / 2 * s; dy = size * cyk + p.X / 2 * s
    clip = D(h['pin'], rect(-9000, -9000, 9000, (dy - size - 4) / s))   # cut the pin just past the bottom edge
    bgsvg = f'<rect width="{size}" height="{size}" rx="{rx}" fill="{bg}"/>' if bg else ''
    inner = bgsvg + body([(h['n'], ink), (clip, gold)], s, dx, dy)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}"><title>{title}</title>{inner}</svg>'


if __name__ == '__main__':
    # THE SYMBOL: the hinge (n of Van + I of Indra, one gold stroke shared)
    write('mark.svg', square(sym_parts(SYM, EM, GD), fill=0.86, title='VanIndra Creations — the hinge (symbol)'))
    write('mark_one_colour_gold.svg', square(sym_parts(SYM, GD, GD), fill=0.86, title='VanIndra Creations — the hinge, one colour gold'))
    write('mark_one_colour_emerald.svg', square(sym_parts(SYM, EM, EM), fill=0.86, title='VanIndra Creations — the hinge, one colour emerald'))
    write('mark_one_colour_ivory.svg', square(sym_parts(SYM, IV, IV), fill=0.86, bg=EM, title='VanIndra Creations — the hinge, one colour ivory'))
    # AVATAR (Instagram / WhatsApp): icon cut, set large, pin bleeding off the bottom
    write('mark_on_emerald.svg', bleed(SYMI, pi, IV, GL, EM, title='VanIndra Creations — profile picture'))
    write('mark_on_ivory.svg', bleed(SYMI, pi, EM, GD, IV, title='VanIndra Creations — profile picture (light)'))
    # 48 px and below: favicon / app icon
    write('mark_small.svg', square(sym_parts(SYMS, EM, GD), fill=0.92, title='VanIndra Creations — small hinge (48 px and below)'))
    write('mark_small_ivory.svg', square(sym_parts(SYMS, IV, GL), fill=0.92, title='VanIndra Creations — small hinge on dark'))
    write('mark_small_tile.svg', bleed(SYMI, pi, IV, GL, EM, xh=0.46, cyk=0.40, rx=0, title='VanIndra Creations — favicon / app icon'))
    # wordmarks (one line: n and I apart, I at cap height, gold I)
    write('wordmark.svg', fit([(WM['ink'], EM), (WM['I'], GD)], unit=0.5))
    write('wordmark_mono.svg', fit([(WM['ink'], EM), (WM['I'], EM)], unit=0.5))
    write('wordmark_small.svg', fit([(WT['ink'], EM), (WT['I'], GD)], unit=0.5))
    write('wordmark_devanagari.svg', fit([(DV['ink'], EM), (DV['i'], GD), (DV['bindu'], EM)], unit=0.5,
                                         title='वनिंद्रा — to be verified by the team'))
    # THE SIGNATURE: the staircase (primary logo)
    write('staircase.svg', fit(stair_parts(ST, EM, GD), unit=0.5))
    write('staircase_on_emerald.svg', fit(stair_parts(ST, IV, GL), unit=0.5, padx=pd.X, pady=pd.X * 0.9, bg=EM))
    write('staircase_one_colour_emerald.svg', fit(stair_parts(ST, EM, EM), unit=0.5))
    write('staircase_one_colour_gold.svg', fit(stair_parts(ST, GD, GD), unit=0.5))
    write('staircase_one_colour_ivory.svg', fit(stair_parts(ST, IV, IV), unit=0.5, padx=pd.X, pady=pd.X * 0.9, bg=EM))
    # lockups
    write('lockup_horizontal_on_ivory.svg', lockup_horizontal(EM, GD, IV))
    write('lockup_horizontal_on_emerald.svg', lockup_horizontal(IV, GL, EM))
    write('lockup_stacked_on_ivory.svg', lockup_stacked(EM, GD, IV))
    write('lockup_stacked_on_emerald.svg', lockup_stacked(IV, GL, EM))
    write('lockup_bilingual_on_ivory.svg', lockup_bilingual(EM, GD, IV))
    write('lockup_bilingual_on_emerald.svg', lockup_bilingual(IV, GL, EM))
    write('global.svg', lockup_horizontal(EM, GD, WH))
    # small-cut helpers for header / context / Reel (transparent, tight)
    write('header_staircase_emerald.svg', fit(stair_parts(STS, EM, GD), unit=0.1))
    write('header_staircase_ivory.svg', fit(stair_parts(STS, IV, GL), unit=0.1))
    write('header_staircase_mono_emerald.svg', fit(stair_parts(STS, EM, EM), unit=0.1))
    write('header_staircase_mono_ivory.svg', fit(stair_parts(STS, IV, IV), unit=0.1))
    print('built')
