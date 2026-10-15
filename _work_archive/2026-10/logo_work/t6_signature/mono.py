"""Monograms derived from the signature's own strokes (same pen, same slant, same construction)."""
import math
from geo import SB, _dir
from word2 import final_to_upright, hook_start, DEF, X


def _norm(a):
    return (a + 180) % 360 - 180


def v_left(c, H, entry='hook', r=15.0, lead=16.0, ramp=46.0):
    t = math.tan(math.radians(c['slant']))
    cp, B = c['cap_p'], c['ball']
    phi_l = _norm(final_to_upright(c['v_lean'], t) + 180)
    dl = _dir(phi_l)
    Lt = (dl[0] / dl[1] * H, H)
    if entry == 'hook':
        S0 = hook_start(Lt, phi_l, r, 64, cw=True)
        d = _dir(64)
        sb = SB(S0[0] - d[0] * lead, S0[1] - d[1] * lead, 64, p=0.0, ball0=B)
        sb.line(*S0, p=0.0)
        sb.turn_to(r, phi_l, p=0.3, direction=-1)
        sb.fwd(ramp, p=cp)
    else:
        sb = SB(Lt[0] - dl[0] * 10, Lt[1] - dl[1] * 10, phi_l, p=0.0)
        sb.line(*Lt, p=0.3)
        sb.fwd(ramp, p=cp)
    sb.line(dl[0] / dl[1] * 16, 16, p=cp)
    sb.line(0, 0, p=0.3)
    return sb


def phi_right(c):
    t = math.tan(math.radians(c['slant']))
    return final_to_upright(c['v_lean'] + c['v_open'], t)


def m_crook(cfg=None):
    """The signature V on its own: hook entry, shaded arm, hairline arm ending in a crook."""
    c = dict(DEF); c.update(cfg or {})
    C, B = c['C'], c['ball']
    S = [v_left(c, C - 14)]
    sb = SB(0, 0, phi_right(c), p=0.0)
    sb.until_y(C - 34, p=0.0)
    sb.arc(13, 205, p=0.35)
    sb.end(B)
    S.append(sb)
    return S


def m_canopy(cfg=None, Is=None, rise=0.60, rc=20.0, dIs=64.0, foot='loop', top_k=0.62, apex=None):
    """V + I in one stroke: the V's hairline rises, turns over as the canopy and descends as the I."""
    c = dict(DEF); c.update(cfg or {})
    C, B, cp = c['C'], c['ball'], c['cap_p']
    S = [v_left(c, C - 14)]
    pr = phi_right(c)
    dr = _dir(pr)
    y1 = C * rise
    x1 = dr[0] / dr[1] * y1
    Is = (x1 + dIs) if Is is None else Is
    top = C if apex is None else apex
    sb = SB(0, 0, pr, p=0.0)
    sb.until_y(y1, p=0.0)
    sb.to(Is - rc, top, 0, p=0.0, k=top_k)
    sb.turn_to(rc, -90, p=0.4, direction=-1)
    sb.line(Is, top - rc - 40, p=cp)
    rf = 24.0
    sb.line(Is, rf, p=cp)
    sb.arc(rf, -90, p=0.3)
    if foot == 'loop':
        sb.arc(19, -90, p=0.0)
        sb.arc(19, -90, p=0.0)
        sb.line(sb.x + 34, sb.y, p=0.0)
        sb.end(B * 0.9)
    elif foot == 'under':      # sweep back left under the V's point, curl up, ball
        sb.line(-34, 0, p=0.0)
        sb.arc(18, -160, p=0.0)
        sb.end(B * 0.9)
    elif foot == 'ball':
        sb.arc(16, -70, p=0.0)
        sb.end(B * 0.9)
    S.append(sb)
    return S


def m_vi(cfg=None, rise=0.62, dIs=52.0, rc=16.0, apex=None, end='taper', hook=True, lean=None, k=0.62,
         stem_bottom=0.0):
    """V + I ligature, the canopy gesture compressed: shaded V arm, hairline rising, tight turn, clean I stem."""
    c = dict(DEF); c.update(cfg or {})
    if lean is not None:
        c['v_lean'] = lean
    C, B, cp = c['C'], c['ball'], c['cap_p']
    S = [v_left(c, C - 14, entry='hook' if hook else 'clean')]
    pr = phi_right(c)
    dr = _dir(pr)
    y1 = C * rise
    x1 = dr[0] / dr[1] * y1
    Is = x1 + dIs
    top = C if apex is None else apex
    sb = SB(0, 0, pr, p=0.0)
    sb.until_y(y1, p=0.0)
    sb.to(Is - rc, top, 0, p=0.0, k=k)
    sb.turn_to(rc, -90, p=0.45, direction=-1)
    sb.line(Is, top - rc - 36, p=cp)
    if end == 'taper':
        sb.line(Is, stem_bottom + 30, p=cp)
        sb.line(Is, stem_bottom, p=0.35)
    elif end == 'blunt':
        sb.line(Is, stem_bottom, p=cp)
    elif end == 'exit':
        sb.line(Is, stem_bottom + 14, p=cp)
        sb.arc(14, 70, p=0.0)
        sb.fwd(18, p=0.0)
    S.append(sb)
    return S


def m_jewel(cfg=None):
    """The V's hairline arm loops back over the shaded arm, enclosing a single drop-shaped counter."""
    c = dict(DEF); c.update(cfg or {})
    C, B = c['C'], c['ball']
    S = [v_left(c, C - 40, entry='clean')]
    sb = SB(0, 0, phi_right(c), p=0.0)
    sb.until_y(C - 70, p=0.0)
    sb.to(sb.x - 40, C, 180, p=0.0, k=0.6)
    sb.to(sb.x - 120, C - 110, -95, p=0.25, k=0.6)
    sb.end(B)
    S.append(sb)
    return S


def m_footwrap(cfg=None):
    """V and I side by side, the I's foot loop sweeping back under the V's point."""
    c = dict(DEF); c.update(cfg or {})
    C, B, cp = c['C'], c['ball'], c['cap_p']
    S = [v_left(c, C - 14)]
    sb = SB(0, 0, phi_right(c), p=0.0)
    sb.until_y(C - 34, p=0.0)
    sb.arc(13, 205, p=0.35)
    sb.end(B)
    S.append(sb)
    Is = 150.0
    sb = SB(Is - 60, C - 46, 56, p=0.0, ball0=B)
    sb.to(Is - 22, C, 0, p=0.0, k=0.58)
    sb.turn_to(22, -90, p=0.85 * cp, direction=-1)
    sb.line(Is, 26, p=cp)
    sb.arc(26, -90, p=0.25)
    sb.line(-30, 0, p=0.0)
    sb.arc(16, -150, p=0.0)
    sb.end(B * 0.9)
    S.append(sb)
    return S


def v_left2(c, H, r=15.0, lead=16.0, ramp=None, fade=None, hook=True, fade_ease=None):
    """Shaded V arm: hairline hook, C1 pressure ramp into a parallel shade, C1 taper into a crisp vee."""
    t = math.tan(math.radians(c['slant']))
    cp, B = c['cap_p'], c['ball']
    phi_l = _norm(final_to_upright(c['v_lean'], t) + 180)
    dl = _dir(phi_l)
    Lt = (dl[0] / dl[1] * H, H)
    fade = c.get('v_fade', 46.0) if fade is None else fade
    ramp = c.get('v_ramp', 44.0) if ramp is None else ramp
    p0 = c.get('v_hook_p', 0.28)
    if hook:
        S0 = hook_start(Lt, phi_l, r, 64, cw=True)
        d = _dir(64)
        sb = SB(S0[0] - d[0] * lead, S0[1] - d[1] * lead, 64, p=p0, ball0=B)
        sb.line(*S0, p=p0)
        sb.turn_to(r, phi_l, p=p0, direction=-1)
    else:
        sb = SB(Lt[0] - dl[0] * 8, Lt[1] - dl[1] * 8, phi_l, p=0.0)
        sb.line(*Lt, p=p0)
    sb.fwd(ramp, p=cp, ease='ramp')
    sb.line(dl[0] / dl[1] * fade, fade, p=cp)
    sb.line(0, 0, p=0.0, ease=c.get('v_fade_ease', 'taper'))
    return sb


def m_vi2(cfg=None, rise=0.56, dIs=50.0, rc=18.0, end='taper', hook=True, k=0.66, bend=0.0, i_end_len=70.0,
          top_dy=0.0):
    """Refined VI ligature. bend: lateral bow (upright units) of the hairline as a compound curve."""
    c = dict(DEF); c.update(cfg or {})
    C, B, cp = c['C'], c['ball'], c['cap_p']
    S = [v_left2(c, C - 14, hook=hook)]
    pr = phi_right(c)
    dr = _dir(pr)
    y1 = C * rise
    x1 = dr[0] / dr[1] * y1
    Is = x1 + dIs
    top = C + top_dy
    sb = SB(0, 0, pr, p=0.0)
    if bend:
        # compound hairline: leaves the point steeper, bows, then eases into the turn
        sb.to(x1 + bend, y1, pr + 6, p=0.0, k=0.5)
    else:
        sb.until_y(y1, p=0.0)
    sb.to(Is - rc, top, 0, p=0.0, k=k)
    sb.turn_to(rc, -90, p=0.45, direction=-1)
    sb.line(Is, top - rc - 34, p=cp)
    if end == 'taper':
        sb.line(Is, i_end_len, p=cp)
        sb.line(Is, 0, p=0.0, ease=2.2)
    elif end == 'blunt':
        sb.line(Is, 0, p=cp)
    elif end == 'kick':     # the nib releases into a short hairline kick to the left (foot of the signature I)
        sb.line(Is, 26, p=cp)
        sb.arc(24, -60, p=0.15)
        sb.end(B * 0.85)
    S.append(sb)
    return S
