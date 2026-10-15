"""Build every SVG deliverable for R3 'The Hinge' (final)."""
import sys, re, math
sys.path.insert(0, '.')
from vitype import *
from deva import DP, vanindra_deva

EM = '#0B2A20'; IV = '#F6F1E7'; GD = '#A8843A'; GL = '#D2B26A'; WH = '#FFFFFF'
OUT = '.'

# optical cuts
pd = P(**DISPLAY)                                     # lockups, wordmark, print
ps = P(**SMALL)                                       # header, Reel credit, avatar
DESC = dict(S=92, Sc=98, H=34, Ht=38, Hb=37, ft=26, fe=30, fb=16, it=28, ie=31, tw=58)   # 'Creations' at 58 %
pc = P(**DESC)
FAV = dict(SMALL, Sc=122, H=58, it=40, fb=12)         # favicon V: hairline at ~half the stem
pf = P(**FAV)
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
VF, _ = g_V(pf)               # favicon V


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


def deva_placed(ratio=0.70):
    """वनिंद्रा centred under the one-line wordmark, its width = 70 % of the name's."""
    b = bbox(WM['ink'], WM['I']); db = bbox(DV['ink'], DV['i'], DV['bindu'])
    s = (b[2] - b[0]) * ratio / (db[2] - db[0])
    x = b[0] + ((b[2] - b[0]) - (db[2] - db[0]) * s) / 2 - db[0] * s
    y = -(pd.X * 1.12) - (DV_P.HB + DV_P.hl) * s
    tr = lambda q: T(T(q, 0, 0, s, s), x, y)
    return tr(DV['ink']), tr(DV['i']), tr(DV['bindu'])


def lockup_bilingual(ink, icol, bg, unit=0.5):
    dk, di, dbd = deva_placed()
    parts = [(WM['ink'], ink), (WM['I'], icol), (dk, ink), (di, icol), (dbd, ink)]
    return fit(parts, padx=pd.X * 1.1, pady=pd.X * 0.9, unit=unit, bg=bg,
               title='VanIndra Creations — bilingual (Devanagari to be verified by the team)')


if __name__ == '__main__':
    # marks (the staircase is the mark; built in the small cut because its life is 32-320 px)
    write('mark.svg', square(stair_parts(STS, EM, GD), fill=0.86, title='VanIndra Creations — staircase mark'))
    write('mark_on_ivory.svg', square(stair_parts(STS, EM, GD), fill=0.88, bg=IV, circle=0.88))
    write('mark_on_emerald.svg', square(stair_parts(STS, IV, GL), fill=0.88, bg=EM, circle=0.88))
    write('mark_one_colour_gold.svg', square(stair_parts(STS, GD, GD), fill=0.86))
    write('mark_one_colour_emerald.svg', square(stair_parts(STS, EM, EM), fill=0.86))
    write('mark_small.svg', square([(VF, EM)], fill=0.80, title='VanIndra Creations — favicon V (48 px and below)'))
    write('mark_small_ivory.svg', square([(VF, IV)], fill=0.80, title='VanIndra Creations — favicon V on dark'))
    write('mark_small_tile.svg', square([(VF, IV)], fill=0.62, bg=EM, title='VanIndra Creations — favicon tile'))
    # wordmarks
    write('wordmark.svg', fit([(WM['ink'], EM), (WM['I'], GD)], unit=0.5))
    write('wordmark_mono.svg', fit([(WM['ink'], EM), (WM['I'], EM)], unit=0.5))
    write('wordmark_small.svg', fit([(WT['ink'], EM), (WT['I'], GD)], unit=0.5))
    write('wordmark_devanagari.svg', fit([(DV['ink'], EM), (DV['i'], GD), (DV['bindu'], EM)], unit=0.5,
                                         title='वनिंद्रा — to be verified by the team'))
    write('staircase.svg', fit(stair_parts(ST, EM, GD), unit=0.5))
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
