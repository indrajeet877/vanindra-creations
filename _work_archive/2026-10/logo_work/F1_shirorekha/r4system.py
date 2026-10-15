"""Round 3 final-final system: every parameter in one place, plus the composed pieces.
Units: VANINDRA cap body H = 100 (top of the line to baseline)."""
from r3geo import *
from r3latin import St
from r4latin import word, CRE_BUILD, VAN_BUILD
from r4mark import va_vloop

# ----------------------------------------------------------------- the mark: व whose counter AND silhouette are a V
MK = dict(b=9.5, S=13.0, jt=20.0, ht=5.5, K=(2.0, 40.0), ks=(32.0, 13.0), P=(31.0, 95.0), Ki=(17.0, 43.0),
          kis=(24.0, 10.0), yj=0.54, h=10.5)
MKS = dict(b=13.5, S=17.0, jt=24.0, ht=8.5, h=13.0, ovl=2.0, ovr=2.0, K=(0.0, 42.0), ks=(32.0, 13.0), P=(31.0, 95.0),
           Ki=(19.0, 47.0), kis=(20.0, 10.0), yj=0.57)
# lockup cut: drawn at the wordmark's weights (used only above the name, see stacked lockup)
MKL = dict(b=6.2, S=8.4, jt=18.0, ht=3.4, h=6.4, K=(3.0, 38.0), ks=(32.0, 13.0), P=(31.0, 95.0), Ki=(11.5, 40.0),
           kis=(28.0, 11.0), yj=0.53)

# ----------------------------------------------------------------- the capitals
WORD = dict(H=100, b=8.8, S=13.0, h=5.0, ns=8.5, t0=3.8, Tf=13.5, lb=3.0, trap=0,
            vleaf=dict(t0=3.8, ko1=3.5, ko2=3.0, ki1=-2.5, ki2=-12.0))
WORD_SP = {('V', 'A'): -7.0, ('A', 'N'): 10.0, ('N', 'I'): 21.0, ('I', 'N'): 21.0, ('N', 'D'): 18.0,
           ('D', 'R'): 14.0, ('R', 'A'): 4.0}
# sturdy cut: website/app headers (cap 12-40 px), Reel credits, embroidery, foil, small print.
# every hairline >= 10.2 units = 1.6% of the word width (the embroidery/foil minimum) and >= 1.7 px at a 17 px cap.
STURDY = dict(H=100, b=11.0, S=16.0, h=10.2, ns=12.0, t0=10.2, Tf=18.5, lb=2.4, trap=0,
              vleaf=dict(t0=10.2, ko1=3.0, ko2=2.5, ki1=-2.0, ki2=-10.0))
STURDY_SP = {('V', 'A'): -1.0, ('A', 'N'): 14.0, ('N', 'I'): 25.0, ('I', 'N'): 25.0, ('N', 'D'): 21.0,
             ('D', 'R'): 17.0, ('R', 'A'): 7.0}

# CREATIONS: same constructors (leaf A / R / N diagonals, contrast C / O / S), set at CRE_K of the VANINDRA cap,
# standing on VANINDRA's baseline under the same line.
CRE = dict(H=100, b=4.5, S=14.5, h=6.2, ns=9.0, t0=5.5, Tf=15.0, lb=2.6, top=6.2, trap=0)
CRE_ST = dict(H=100, b=4.5, S=18.0, h=10.5, ns=12.0, t0=10.5, Tf=19.0, lb=2.2, top=10.5, trap=0)   # sturdy
CRE_SP = {('C', 'R'): 19, ('R', 'E'): 19, ('E', 'A'): 8, ('A', 'T'): 4, ('T', 'I'): 19, ('I', 'O'): 17,
          ('O', 'N'): 19, ('N', 'S'): 19}
CRE_SP_ST = {('C', 'R'): 22, ('R', 'E'): 22, ('E', 'A'): 11, ('A', 'T'): 7, ('T', 'I'): 22, ('I', 'O'): 20,
             ('O', 'N'): 22, ('N', 'S'): 22}
CRE_K = 0.55
HAIR = 3.6          # the line's hairline weight in VANINDRA units (master); sturdy uses HAIR_ST
HAIR_ST = 6.0
OVL, OVR = 4.0, 4.0


def mark(cut='master'):
    g, info = va_vloop(**{'master': MK, 'small': MKS, 'lockup': MKL}[cut])
    return norm(g), info


def vanindra(cut='master', bar=True, ovl=OVL, ovr=OVR, grid=None, widths=None):
    p = dict(WORD if cut == 'master' else STURDY)
    sp = WORD_SP if cut == 'master' else STURDY_SP
    st = St(**p, bar=bar)
    g, tot, spans = word(st, 'VANINDRA', sp, build=VAN_BUILD, grid=grid, widths=widths)
    if bar:
        g = U(g, rect(-ovl, 0, tot + ovr, st.b))
    return g, tot, st


def creations(cut='master'):
    st = St(**(CRE if cut == 'master' else CRE_ST), bar=False)
    g, tot, spans = word(st, 'CREATIONS', CRE_SP if cut == 'master' else CRE_SP_ST)
    return g, tot, st


def full_name(cut='master', k=CRE_K, gap=36.0, hair=None, bar=True, cre_cut=None):
    """VANINDRA hangs from the heavy line. CREATIONS stands on VANINDRA's baseline, under the same line, which steps
    to a hairline in the middle of the gap (never over a letter). bar=False -> global: one uniform hairline over both
    words, and VANINDRA's caps hang from it (they touch it)."""
    hair = (HAIR if cut == 'master' else HAIR_ST) if hair is None else hair
    wm, tot, st = vanindra(cut, bar=False, ovl=OVL, ovr=0.0)
    cr, totc, stc = creations(cre_cut or cut)
    crs = tr(cr, k, tot + gap, 100.0 * (1 - k))
    end = tot + gap + totc * k + OVR
    xs = tot + gap * 0.5
    if bar:
        line = U(rect(-OVL, 0, xs, st.b), rect(xs - 0.5, 0, end, hair))
    else:
        line = rect(-OVL, 0, end, hair)
    return U(wm, crs), line, end
