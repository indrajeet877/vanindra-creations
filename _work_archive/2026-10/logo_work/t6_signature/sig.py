"""VanIndra 'Canopy Signature' - final construction.

One gesture defines the identity: the V's hairline rises, turns over as a canopy (the sky, Indra) and
descends as the shaded I. The wordmark and the mark call the SAME functions below, so the mark is
literally the signature with 'an' removed.
"""
import math
from geo import SB, _dir, internal_tangent
from word2 import X, DEF as WDEF, bowl, stem, arch_into, join, connect_from_heading
from mono import v_left2, phi_right

FOOT = 8.6   # stems end at full pressure; the round end then sits on the baseline
CFG = dict(WDEF)
CFG.update(dict(
    slant=18.0, C=252.0, A=212.0, U=70.0, RU=12.0, RO=11.0, rx=31.0, cap_p=1.15, ball=5.0,
    v_lean=-8.0, v_open=38.0,
    # canopy (wordmark)
    can_rise=0.62, can_k=0.58, can_turn=22.0, can_lift=10.0,
    # mark
    m_rise=0.60, m_dIs=78.0, m_k=0.60, m_turn=24.0,
    i_tail=58.0,       # height at which the I's taper begins
    i_turn_p=0.85, i_ramp=18.0, i_ease='taper_soft',
    v_ramp=26.0, v_fade=56.0, v_fade_ease='taper_soft', v_hook_p=0.40,
    gap_nI=100.0,      # n (Van) stem 2 -> I stem
))


def canopy_I(c, Is, rise, k, rc, lift=0.0, i_tail=None, foot='taper', m1=None):
    """The defining stroke: from the V's point, hairline up, canopy over, shaded I down.
    foot='taper' (mark): the nib lifts into a point.  foot='loop' (wordmark): the I's foot loops left,
    crosses back over its own stem and flows into the n."""
    C, cp, RO = c['C'], c['cap_p'], c['RO']
    i_tail = c['i_tail'] if i_tail is None else i_tail
    pr = phi_right(c)
    top = C + lift
    sb = SB(0, 0, pr, p=0.0)
    sb.until_y(C * rise, p=0.0)
    sb.to(Is - rc, top, 0, p=0.0, k=k)
    p_turn = c.get('i_turn_p', 0.32)
    sb.turn_to(rc, -90, p=p_turn, direction=-1)
    sb.fwd(c.get('i_ramp', 46.0), p=cp, ease='ramp')
    if foot == 'taper':
        sb.line(Is, i_tail, p=cp)
        sb.line(Is, 0, p=0.0, ease=c.get('i_ease', 'taper'))
    elif foot == 'blunt':
        sb.line(Is, c.get('i_blunt_y', 0.0), p=cp)
    else:
        rf = 24.0
        sb.line(Is, rf, p=cp)
        sb.arc(rf, -90, p=0.3)            # heading west on the baseline
        sb.arc(19, -90, p=0.0)            # up the back of the loop
        sb.arc(19, -78, p=0.0)            # over the top, already turning to rise
        connect_from_heading(sb, 34, (m1 - RO, X - RO), RO)
        sb.turn_to(RO, -90, p=0.25, direction=-1)
        sb.line(m1, FOOT, p=1.0)
    return sb


def V_left(c):
    return v_left2(c, c['C'] - 14, hook=c.get('v_hook', True))


def mark_strokes(cfg=None):
    c = dict(CFG); c.update(cfg or {})
    pr = phi_right(c)
    dr = _dir(pr)
    y1 = c['C'] * c['m_rise']
    Is = dr[0] / dr[1] * y1 + c['m_dIs']
    return [V_left(c), canopy_I(c, Is, c['m_rise'], c['m_k'], c['m_turn'], foot=c.get('m_foot', 'taper'),
                                lift=c.get('m_lift', 0.0))], c


def wordmark_strokes(cfg=None):
    c = dict(CFG); c.update(cfg or {})
    C, A, U, RU, RO, rx, B = c['C'], c['A'], c['U'], c['RU'], c['RO'], c['rx'], c['ball']
    S = [V_left(c)]
    dr = _dir(phi_right(c))
    # ---------------------------------------------------------------- a n
    xarm = dr[0] / dr[1] * 50.0
    a1 = xarm + 40 + rx
    sa = a1 + rx
    S.append(bowl(a1, rx, X, c, tuck=9.0))
    n1, n2 = sa + U, sa + 2 * U
    sb = stem(sa, X, c)
    join(sb, sa, n1, c)
    sb.line(n1, FOOT, p=1.0)
    S.append(sb)
    sb = arch_into(n1, n2, c)
    a_exit, _, _ = internal_tangent((n2 + RU, RU), RU, True, (n2 + U - RO, X - RO), RO, False)
    sb.turn_to(RU, a_exit, p=0.0, direction=1)
    sb.fwd(26, p=0.0)
    S.append(sb)
    # ---------------------------------------------------------------- canopy + I (+ loop into n)
    Is = n2 + c['gap_nI']
    m1 = Is + 74.0
    m2 = m1 + U
    S.append(canopy_I(c, Is, c['can_rise'], c['can_k'], c['can_turn'], lift=c['can_lift'], foot='loop', m1=m1))
    # ---------------------------------------------------------------- n -> d (connective hugs the bowl)
    dcx = m2 + 44 + rx
    ds = dcx + rx
    sb = arch_into(m1, m2, c)
    sb.turn_to(RU, 52, p=0.0, direction=1)
    t_hit = 208.0
    hx, hy = dcx + rx * math.cos(math.radians(t_hit)), 50 + 50 * math.sin(math.radians(t_hit))
    htan = math.degrees(math.atan2(-50 * math.cos(math.radians(t_hit)), rx * math.sin(math.radians(t_hit))))
    sb.to(hx, hy, htan, p=0.0, k=0.55)
    sb.ellipse(dcx, 50, rx, 50, 38, p=0.0, ccw=False)
    S.append(sb)
    S.append(bowl(dcx, rx, A, c))
    sb = stem(ds, A, c, p_top=0.0, ramp=70)
    rs = ds + U
    join(sb, ds, rs, c)
    sb.line(rs, FOOT, p=1.0)
    S.append(sb)
    # ---------------------------------------------------------------- r a
    sb = SB(rs, 9.0, 90, p=0.0)
    sb.line(rs, 58, p=0.0)
    sb.ellipse(rs + 20, 58, 20, X - 58, 90, p=0.0, ccw=False)
    sb.arc(12, -62, p=0.1)
    sb.end(B * 1.05)
    S.append(sb)
    a2 = rs + 54 + rx
    sa2 = a2 + rx
    S.append(bowl(a2, rx, X, c, tuck=9.0))
    sb = stem(sa2, X, c)
    sb.turn_to(RU, a_exit, p=0.0, direction=1)
    sb.fwd(30, p=0.0)
    S.append(sb)
    return S, c
