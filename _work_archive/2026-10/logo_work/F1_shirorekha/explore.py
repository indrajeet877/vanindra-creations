"""Round 3 exploration: nine genuinely different ways to finish the Shirorekha idea. -> explore.png"""
import subprocess
from r3geo import *
from r3mark import va_mark, va_loop
from r3latin import St, wordmark
from r3deva import devanagari_word

OUT = os.path.join(HERE, 'explore')
os.makedirs(OUT, exist_ok=True)
BW, BH = 900, 560


def cap(txt, x, y, size=17, color='#6b5a35'):
    t = V.text_path(txt, family='manrope', weight=500, size=size, x=x, y=y)
    return (t.path, color)


def fit(path, x, y, w=None, h=None, anchor='tl'):
    x0, y0, x1, y1 = bbox(path)
    s = min((w or 1e9) / (x1 - x0), (h or 1e9) / (y1 - y0))
    p = tr(path, s, -x0 * s, -y0 * s)
    bw, bh = (x1 - x0) * s, (y1 - y0) * s
    if anchor == 'c':
        return tr(p, 1, x - bw / 2, y - bh / 2)
    return tr(p, 1, x, y)


def board(name, layers, bg=IV):
    return write(os.path.join(OUT, name + '.svg'), svg(BW, BH, layers, bg=bg))


MARK_A = dict(px=26, py=87, yj=0.48, h=8.5, leaf=dict(ko1=11, ko2=9, ki1=-1, ki2=-18))
files = []

# E1 master: pointed leaf va/V + VANINDRA hanging from one line
mk, _ = va_mark(**MARK_A)
st = St()
wm, _, _ = wordmark(st)
files.append(board('E1', [(fit(mk, 90, 70, h=250), EM), (fit(wm, 330, 170, w=500), EM),
                          cap('E1  Master: leaf va/V, one 8.8 line; outward leaf, tip left of centre, danda runs on', 40, 520)]))

# E2 notch: the leaf hangs from the line by a neck, a clear notch instead of a sliver
mk2, _ = va_mark(notch=6.0, **MARK_A)
wm2, _, _ = wordmark(St(h=5.5))
files.append(board('E2', [(fit(mk2, 90, 70, h=250), EM), (fit(wm2, 330, 170, w=500), EM),
                          cap('E2  Open notch where leaf meets line (judge option A)', 40, 520)]))

# E3 global: VANINDRA hanging from a gold hairline rule, no headline bar
stg = St(bar=False)
wmg, totg, _ = wordmark(stg, bar=False)
rule = rect(-4, 0, totg + 4, 3.2)
both = U(wmg)
x0, y0, x1, y1 = bbox(both)
s = 640 / (x1 - x0)
files.append(board('E3', [(tr(wmg, s, 130 - x0 * s, 200), EM), (tr(rule, s, 130 - x0 * s, 200), GO),
                          cap('E3  Global: the same capitals hang from a gold hairline rule', 40, 520)]))

# E4 global: bar only over the V
wmv, _, _ = wordmark(St(), bar_span=('V',))
files.append(board('E4', [(fit(wmv, 130, 200, w=640), EM), cap('E4  Global: the line only over the V', 40, 520)]))

# E5 one line, two scripts
stb = St()
wl, tl, _ = wordmark(stb, ovr=0)
dv, (dx0, dx1) = devanagari_word()
gap = 42
dv2 = tr(dv, 1, tl + gap - dx0, 0)
bridge = rect(tl - 1, 0, tl + gap + 1, stb.b)
line2 = U(wl, dv2, bridge)
files.append(board('E5', [(fit(line2, 60, 210, w=780), EM),
                          cap('E5  One line, two scripts: VANINDRA + drawn Devanagari (to be verified)', 40, 520)]))

# E6 the line extends: deck title, everything hangs from one headline
stx = St()
wmx, totx, _ = wordmark(stx, ovl=0, ovr=0)
k = 300 / totx
long_line = rect(0, 0, 820 / k, stx.b)
title = V.text_path('Hooks that hold.', family='bodoni-moda', weight=500, size=46, x=0, y=0)
tb = bbox(title.path)
lay = [(tr(U(wmx, long_line), k, 40, 150), EM), (tr(title.path, 1, 40 + 360 - tb[0], 150 + stx.b * k - tb[1] + 6), EM),
       cap('E6  The line extends: name and title hang from one headline (deck / Reel cover)', 40, 520)]
files.append(board('E6', lay))

# E7 full name: CREATIONS drawn in-system, hanging from a hairline under VANINDRA
stc = St(b=2.6, S=11.0, h=7.0, ns=9.0, t0=6.0, Tf=12.0, lb=1.5, top=9.5, trap=0)
spc = {('C', 'R'): 15, ('R', 'E'): 16, ('E', 'A'): 6, ('A', 'T'): 2, ('T', 'I'): 15, ('I', 'O'): 14, ('O', 'N'): 15, ('N', 'S'): 15}
cr, tc, _ = wordmark(stc, 'CREATIONS', space=spc, ovl=3, ovr=3)
wb = bbox(wm)
cb = bbox(cr)
sc = (wb[2] - wb[0]) * 0.52 / (cb[2] - cb[0])
cr2 = tr(cr, sc, wb[0] + ((wb[2] - wb[0]) - (cb[2] - cb[0]) * sc) / 2 - cb[0] * sc, 100 + 38)
full = U(wm, cr2)
files.append(board('E7', [(fit(full, 190, 130, w=520), EM), cap('E7  Full name: CREATIONS drawn in-system, hung from its own hairline', 40, 520)]))

# E8 header cut: lower contrast for 16-40 px cap heights
sth = St(h=7.2, ns=10.0, t0=5.5, S=13.5, Tf=14.0, trap=0)
wmh, _, _ = wordmark(sth, space={('N', 'I'): 24, ('I', 'N'): 24, ('A', 'N'): 11})
small = fit(wmh, 130, 120, w=640)
tiny = fit(wmh, 130, 330, w=200)
tiny2 = fit(wm, 430, 330, w=200)
files.append(board('E8', [(small, EM), (tiny, EM), (tiny2, EM), cap('header cut', 130, 400, 13), cap('master', 430, 400, 13),
                          cap('E8  Header cut: hairlines 7.2, N stems 10, NI/IN opened 20%', 40, 520)]))

# E9 loop va (rounded lower third) - tested and rejected: reads as pa
ml, _ = va_loop()
files.append(board('E9', [(fit(ml, 330, 80, h=320), EM), cap('E9  Rounded loop (judge fallback): drifts to pa, rejected', 40, 520)]))

subprocess.run(['node', os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js'), 'sheet', os.path.join(HERE, 'explore.png')] + files, check=True)
print('ok')
