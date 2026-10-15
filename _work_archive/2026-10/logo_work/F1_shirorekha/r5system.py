"""F1 polish (Round 3 finalist, before the team vote). Every parameter that changed from r4system lives here.
Units: VANINDRA cap body H = 100 (top of the line to baseline)."""
import r4latin, r5pen
r4latin.vstroke_pts = r5pen.vstroke_pts          # the contrast pen (C, S of CREATIONS) now emits fitted Beziers
from r4system import *
import r4system as R4
from r3latin import St, g_T
from r4latin import word, CRE_BUILD
from r4mark import va_vloop
from r5small import small16

# ----------------------------------------------------------------- the mark
# master: the loop is a leaf: 6.0 hairline where it leaves the danda, at most 11.9 on the shoulder (was 15.3, heavier
# than the 13 danda), tapering into the point. Open, round shoulder; long straight arm; the counter V is larger.
MK5 = dict(b=9.5, S=13.0, jt=20.0, ht=6.0, K=(0.5, 43.0), ks=(40.0, 17.0), Ki=(12.0, 46.5), kis=(35.0, 15.0),
           karm=(15.0, 0.8), kiarm=(15.0, -1.0), P=(30.0, 96.0), yj=0.54, h=10.5)
# lockup cut (stacked over the name, drawn at the wordmark's weights): shoulder <= the 8.4 danda
MKL5 = dict(b=6.2, S=8.4, jt=18.0, ht=3.4, h=6.4, K=(1.5, 41.0), ks=(40.0, 16.0), Ki=(8.6, 43.5), kis=(36.0, 14.5),
            karm=(15.0, 0.8), kiarm=(15.0, -1.0), P=(30.0, 96.0), yj=0.53)


def mark5(cut='master'):
    if cut == 'small':
        g, info, _ = small16()
        return g, info
    g, info = va_vloop(**{'master': MK5, 'lockup': MKL5}[cut])
    return norm(g), info


# ----------------------------------------------------------------- CREATIONS: it hangs from its own hairline
# Judges: the hairline over CREATIONS floated ~0.42 cap above its tops, so CREATIONS was the one element that did not
# hang from a line. Now each word hangs from its own line, as separate words do in Devanagari: VANINDRA from the heavy
# line, CREATIONS (0.55 cap, on the same baseline) from a hairline at its own cap height. The caps overlap their
# hairline by 45% of its weight (they touch, no anti-alias seam).
CRE_HAIR = 5.0          # = VANINDRA's hairline stroke (and 0.55 x the heavy line): the system's second line weight
CRE_HAIR_ST = 6.4       # sturdy (headers, small print)
T_BAR = 1.8             # T's crossbar = 1.8 x the CREATIONS top stroke, so the T still reads under its hairline
CRE_BUILD5 = dict(CRE_BUILD)
CRE_BUILD5['T'] = lambda st, W=62: g_T(st, W, tbar=max(st.top, st.h) * T_BAR)


def creations5(cut='master'):
    st = St(**(CRE if cut == 'master' else CRE_ST), bar=False)
    g, tot, spans = word(st, 'CREATIONS', CRE_SP if cut == 'master' else CRE_SP_ST, build=CRE_BUILD5)
    return g, tot, st


def creations_hung(cut='master', k=CRE_K, hair=None, ovl=None, ovr=None):
    """CREATIONS at scale k hanging from its own hairline. Origin: x = left edge of C, y = top of the hairline."""
    hair = (CRE_HAIR if cut == 'master' else CRE_HAIR_ST) if hair is None else hair
    cr, totc, stc = creations5(cut)
    ovl = OVL * k if ovl is None else ovl
    ovr = OVR * k if ovr is None else ovr
    crs = tr(cr, k, 0, hair * 0.55)
    line = rect(-ovl, 0, totc * k + ovr, hair)
    return crs, line, totc * k


def full_name5(cut='master', k=CRE_K, gap=36.0, b=None, hair=None):
    """VANINDRA hangs from the heavy line; CREATIONS stands on the same baseline and hangs from its own hairline.
    b / hair override the line weights (used to pixel-fit the header cut at a fixed cap)."""
    wm, tot, st = vanindra(cut, bar=False)
    b = st.b if b is None else b
    wm = U(wm, rect(-OVL, 0, tot + OVR, b))
    hair = (CRE_HAIR if cut == 'master' else CRE_HAIR_ST) if hair is None else hair
    crs, cline, wc = creations_hung(cut, k, hair=hair)
    y_line = 100.0 * (1 - k) - hair * 0.55
    x0 = tot + gap
    return wm, tr(crs, 1, x0, y_line), tr(cline, 1, x0, y_line), x0 + wc + OVR * k


def full_name_px(cap=28.0, cut='sturdy', bar_px=None, hair_px=2.0):
    """The full name pixel-fitted for one cap height (header / email signature): the heavy line, CREATIONS' hairline
    and the baseline all land on whole pixels. Returns the path in px (line top at y=0)."""
    u = cap / 100.0
    st_b = (STURDY if cut == 'sturdy' else WORD)['b']
    bar_px = bar_px or max(1, round(st_b * u))
    hair = hair_px / u
    y_px = round((100.0 * (1 - CRE_K) - hair * 0.55) * u)
    k = 1 - (y_px / u + hair * 0.55) / 100.0
    wm, crs, cline, end = full_name5(cut, k=k, b=bar_px / u, hair=hair)
    return tr(U(wm, crs, cline), u, round(OVL * u), 0), k


def global_parts5(cut='master', hair=None, k=CRE_K, gap=36.0, cre=True):
    """Global (USD): the heavy line becomes one gold hairline; VANINDRA's caps touch it (overlap 45%). CREATIONS hangs
    from its own gold hairline at its cap height. Returns (letters, gold lines)."""
    hair = (HAIR if cut == 'master' else HAIR_ST) if hair is None else hair
    wm, tot, st = vanindra(cut, bar=False)
    dy = hair * 0.55
    letters = tr(wm, 1, 0, dy)
    lines = rect(-OVL, 0, tot + OVR, hair)
    if cre:
        ch = hair * (0.85 if cut == 'master' else 0.8)
        crs, cline, wc = creations_hung(cut, k, hair=ch)
        y_line = dy + 100.0 * (1 - k) - ch * 0.55
        letters = U(letters, tr(crs, 1, tot + gap, y_line))
        lines = U(lines, tr(cline, 1, tot + gap, y_line))
    return letters, lines

# CREATIONS colour: now that it hangs from its own hairline (more ink at the top), its stems come down slightly so
# the word's colour still matches VANINDRA (stem / cap 13.5% vs VANINDRA's 13%).
CRE.update(S=13.5, ns=8.5)
CRE_ST.update(S=17.0, ns=11.5)
