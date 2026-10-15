"""The chosen One Dot parameters (master + small cut)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from od import P


def derive(P_):
    return P_.copy(vaW=P_.aW * 0.98, naW=P_.nW * 0.95, daW=P_.aW * 0.86, dS=P_.S, hgap=P_.sb * 1.25)


MASTER_KW = dict(S=96, T=48, ktop=0.70, kbot=0.56, kin_top=0.74, kin_bot=0.58, kAR=0.68, kAiR=0.66, apex=0.56,
                 nW=420, aW=430, vW=420, rW=255, dotD=140, dotGap=60, asc=700, vthin=60, vthick=108, Th=58, bowl_ktr=0.99)
DEVA_KW = dict(H=550.0, ra_len=0.24, ra_l=0.12, ra_r=0.94, ra_apex=0.60, dra_gap=1.5, aa_gap=1.6, kam_stop=0.12,
               da_bot=0.10, da_top=0.64, va_top=0.68)


KERN = {'it': 34.0, 'ti': 34.0, 'ty': 0.0, 'ra': -6.0, 'va': -6.0, 'yv': 10.0}


def master(**kw):
    q = derive(P(**MASTER_KW)).copy(**dict(DEVA_KW, **kw))
    q.kern = dict(KERN)
    return q


SMALL_KW = dict(S=108, T=68, dotD=160, dotGap=64, vthin=72, Th=72, sb=56, nW=430, apex=0.55, kAR=0.66, kAiR=0.62)
LIGHT_KW = dict(S=58, T=36, vthin=40, vthick=64, dotD=76, dotGap=52, Rk=1.04)


def small(**kw):
    return master(**dict(SMALL_KW, **kw))


def light(**kw):
    return master(**dict(LIGHT_KW, **kw))


def deva_for_scale(P_, f):
    """Devanagari parameters that, drawn and then scaled by f, keep the Latin stroke weights and dot size."""
    return P_.copy(dS=P_.S / f, T=P_.T / f, Th=P_.Th / f, dotD=P_.dotD / f, dgap=P_.dotGap / f,
                   vthin=P_.vthin / f, vthick=P_.vthick / f, Rk=P_.Rk)


BOOK_KW = dict(S=74, T=42, vthin=46, vthick=82, dotD=96, dotGap=56, Rk=1.04)


def book(**kw):
    return master(**dict(BOOK_KW, **kw))
