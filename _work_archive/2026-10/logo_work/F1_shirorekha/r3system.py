"""Round 3 Shirorekha system: every parameter in one place, plus the composed pieces (mark, words, lines).
Units: VANINDRA cap body H = 100 (top of the line to baseline)."""
from r3geo import *
from r3mark import va_cloop
from r3latin import St, wordmark
import r3deva

# ----------------------------------------------------------------- the mark: a leaf-loop va whose counter is a V
MK = dict(b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0, jt=20.0, ht=5.5, o1=(-6.0, -6.0), o2=(-11.0, 0.48),
          i1=(10.0, 0.0), i2=(13.0, 0.20), P=(29.0, 93.0), yj=0.57, h=10.0)
MKS = dict(b=13.5, S=16.5, xs=58.0, ovl=2.0, ovr=2.0, jt=24.0, ht=8.5, o1=(-7.0, -6.0), o2=(-10.0, 0.48),
           i1=(14.0, 0.0), i2=(11.0, 0.22), P=(28.0, 92.0), yj=0.60, h=12.5)

# ----------------------------------------------------------------- the capitals
WORD = dict(H=100, b=8.8, S=13.0, h=5.0, ns=8.5, t0=3.8, Tf=13.5, lb=3.0, trap=0,
            vleaf=dict(t0=3.8, ko1=3.5, ko2=3.0, ki1=-2.5, ki2=-12.0))
WORD_SP = {('V', 'A'): -7.0, ('A', 'N'): 10.0, ('N', 'I'): 21.0, ('I', 'N'): 21.0, ('N', 'D'): 18.0,
           ('D', 'R'): 14.0, ('R', 'A'): 4.0}
HEADER = dict(H=100, b=10.0, S=14.0, h=7.4, ns=10.5, t0=6.0, Tf=14.5, lb=2.5, trap=0,
              vleaf=dict(t0=6.0, ko1=3.5, ko2=3.0, ki1=-3.0, ki2=-13.0))
HEADER_SP = {('V', 'A'): -4.0, ('A', 'N'): 12.0, ('N', 'I'): 25.0, ('I', 'N'): 25.0, ('N', 'D'): 20.0,
             ('D', 'R'): 16.0, ('R', 'A'): 6.0}
CRE = dict(H=100, b=4.5, S=13.0, h=7.0, ns=9.5, t0=5.5, Tf=14.0, lb=2.5, top=13.0, trap=0)
HAIR = 3.6          # the line's hairline weight, in VANINDRA units
CRE_SP = {('C', 'R'): 16, ('R', 'E'): 16, ('E', 'A'): 7, ('A', 'T'): 3, ('T', 'I'): 16, ('I', 'O'): 15,
          ('O', 'N'): 16, ('N', 'S'): 16}
OVL, OVR = 4.0, 4.0


def mark(small=False):
    g, info = va_cloop(**(MKS if small else MK))
    return norm(g), info


def vanindra(cut='master', bar=True, ovl=OVL, ovr=OVR):
    p = dict(WORD if cut == 'master' else HEADER)
    sp = WORD_SP if cut == 'master' else HEADER_SP
    st = St(**p, bar=bar)
    g, tot, spans = wordmark(st, space=sp, ovl=ovl, ovr=ovr, bar=bar)
    return g, tot, st


def creations(bar=True, ovl=3.0, ovr=3.0):
    st = St(**CRE, bar=bar)
    g, tot, spans = wordmark(st, 'CREATIONS', space=CRE_SP, ovl=ovl, ovr=ovr, bar=bar)
    return g, tot, st


def devanagari(**kw):
    return r3deva.devanagari_word(**kw)
