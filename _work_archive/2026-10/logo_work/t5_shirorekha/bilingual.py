"""Optional bilingual lockup: VANINDRA and वनिंद्रा hang from one shirorekha line (Devanagari TO BE VERIFIED BY THE TEAM).
Devanagari is typeset in Tiro Devanagari Hindi; its own headline band is replaced by the identity's 8.8u shirorekha so both
words share exactly the same line weight."""
import os, subprocess
from build import *

def deva_word(text='वनिंद्रा', fam='tiro-devanagari-hindi', w=400, bar=8.8, H=100):
    ref = V.text_path('न', family=fam, weight=w, subset='devanagari', size=100)
    top = -ref.bounds[1]                       # headline top above baseline at size 100
    hl_rel = 7.5 / 62.0                        # measured headline thickness / body (Tiro)
    body = (H - bar) / (1 - hl_rel)            # body before normalisation
    s = body / top
    t = V.text_path(text, family=fam, weight=w, subset='devanagari', size=100)
    g = tr(t.path, s, 0, top * s)              # headline top at y=0, baseline at y=body
    hl = hl_rel * body
    above = I(g, rect(-1e4, -1e4, 1e4, 0))     # matras / bindu above the line
    below = I(g, rect(-1e4, hl, 1e4, 1e4))     # letter bodies under the headline band
    below = tr(below, 1, 0, -(hl - bar))       # lift so they hang from the new bar
    x0, _, x1, _ = bbox(U(above, below))
    line = rect(x0 - 4, 0, x1 + 3, bar)
    return U(above, below, line)

def make_bilingual():
    wm, st = build_word()
    wm = norm(wm)
    wb = bbox(wm)
    dv = deva_word(bar=st.b, H=st.H)
    db = bbox(dv)
    gap = st.H * 0.42
    dv = tr(dv, 1, wb[2] + gap - db[0], 0)
    db = bbox(dv)
    capH = st.H * 0.20
    ds = descriptor(capH)
    ds = place(ds, 10, st.H + st.H * 0.38)
    allb = bbox(U(wm, dv, ds))
    m = st.H * 0.45
    W, Hh = allb[2] - allb[0] + 2 * m, allb[3] - allb[1] + 2 * m
    ox, oy = m - allb[0], m - allb[1]
    def mk(bg, c1, c2):
        return svg(W, Hh, [(tr(wm, 1, ox, oy), c1), (tr(dv, 1, ox, oy), c1), (tr(ds, 1, ox, oy), c2)], bg=bg)
    a = write('lockup_bilingual_on_ivory.svg', mk(IV, EM, GO))
    b = write('lockup_bilingual_on_emerald.svg', mk(EM, IV, GL))
    return a, b

if __name__ == '__main__':
    a, b = make_bilingual()
    subprocess.run(['node', '../toolkit/render.js', 'sheet', 'study/bil2.png', a, b], check=True)
    subprocess.run(['node', '../toolkit/render.js', 'png', a, 'study/bil2_big.png', '1400'], check=True)
    print(os.path.getsize(a))
