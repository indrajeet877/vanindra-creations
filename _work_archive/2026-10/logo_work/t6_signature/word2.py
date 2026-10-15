"""'VanIndra' signature built with exact construction (lines, arcs, ellipse arcs, tangent connectives).
Upright y-up design space, x-height X = 100. The Pen shears everything to one slant afterwards.
"""
import math
from geo import SB, internal_tangent, _dir

X = 100.0
DEF = dict(
    slant=18.0,
    C=252.0,        # capital height
    A=212.0,        # d ascender
    U=70.0,         # stem unit (stem to stem, inside and between letters)
    RU=12.0,        # underturn radius
    RO=11.0,        # overturn radius
    rx=31.0,        # bowl half width
    cap_p=1.15,     # capital shade multiplier
    ball=5.0,       # terminal ball radius
    v_lean=-8.0,    # final-frame lean of the V's shaded arm (deg from vertical, negative = backslash)
    v_open=38.0,    # final-frame angle between the V arms
    v_entry='hook', # 'hook' | 'clean' | 'loop'
    v_arm='crook',  # 'crook' | 'flick' | 'canopy'
    i_top='hook',   # 'hook' | 'wave'
    i_foot='loop',  # 'loop' | 'plain'
    r_form='arm',
    end='tail',     # 'tail' | 'paraph'
    gap_nI=104.0,   # n stem 2 -> I stem
)


def final_to_upright(angle_from_vertical, t):
    """Direction (deg, upright frame) of a line that leans angle_from_vertical in the final (sheared) frame."""
    a = math.radians(90 - angle_from_vertical)
    fx, fy = math.cos(a), math.sin(a)
    return math.degrees(math.atan2(fy, fx - fy * t))


def hook_start(T, phi, r, start_heading, cw=True):
    """Start point of an arc (radius r) that ends at T with heading phi, having started with start_heading."""
    s = -1 if cw else 1
    n = _dir(phi + 90 * s)
    cx, cy = T[0] + n[0] * r, T[1] + n[1] * r
    m = _dir(start_heading + 90 * s)
    return (cx - m[0] * r, cy - m[1] * r)


def join(sb, s, t, c, top=X, rb=None, rt=None):
    """From the bottom of stem s (heading down at y = RU) to the top of stem t (heading down)."""
    rb = c['RU'] if rb is None else rb
    rt = c['RO'] if rt is None else rt
    a, P1, P2 = internal_tangent((s + rb, rb), rb, True, (t - rt, top - rt), rt, False)
    sb.turn_to(rb, a, p=0.0, direction=1)
    sb.line(*P2, p=0.0)
    sb.turn_to(rt, -90, p=0.25, direction=-1)
    return sb


def connect_from_heading(sb, ra, c2, r2, ccw2=False, p=0.0):
    """From the current point (any heading): CCW arc radius ra, tangent line, then onto circle c2 (r2)."""
    n = _dir(sb.ang + 90)
    c1 = (sb.x + n[0] * ra, sb.y + n[1] * ra)
    a, P1, P2 = internal_tangent(c1, ra, True, c2, r2, ccw2)
    sb.turn_to(ra, a, p=p, direction=1)
    sb.line(*P2, p=p)
    return sb


def bowl(cx, rx, top, c, t0=38.0, tuck=0.0):
    """CCW ellipse bowl starting at parametric angle t0 (top right), ending at its right extreme heading up."""
    ry = X / 2
    x0, y0 = cx + rx * math.cos(math.radians(t0)), ry + ry * math.sin(math.radians(t0))
    tang = math.degrees(math.atan2(ry * math.cos(math.radians(t0)), -rx * math.sin(math.radians(t0))))
    sb = SB(x0, y0, tang, p=0.0)
    sb.ellipse(cx, ry, rx, ry, 90, p=0.1)
    sb.ellipse(cx, ry, rx, ry, 180, p=1.0)
    sb.ellipse(cx, ry, rx, ry, 270, p=0.3)
    sb.ellipse(cx, ry, rx, ry, 360, p=0.0)
    sb.line(cx + rx, top - tuck, p=0.0)
    return sb


def stem(x, top, c, p_top=1.0, ramp=0.0, bottom=None):
    if ramp <= 0:      # full-pressure start: the round top sits exactly on the given height
        sb = SB(x, top - 9.0, -90, p=1.0)
        sb.line(x, c['RU'] if bottom is None else bottom, p=1.0)
        return sb
    sb = SB(x, top, -90, p=p_top)
    sb.line(x, top - ramp, p=1.0, ease='ramp')
    sb.line(x, c['RU'] if bottom is None else bottom, p=1.0)
    return sb


def arch_into(s, t, c, yb=56.0, y0=9.0):
    """Retrace up stem s from inside its foot, branch with an elliptical arch, descend as stem t."""
    sb = SB(s, y0, 90, p=0.0)
    sb.line(s, yb, p=0.0)
    hw = (t - s) / 2
    sb.ellipse(s + hw, yb, hw, X - yb, 90, p=0.1, ccw=False)
    sb.ellipse(s + hw, yb, hw, X - yb, 0, p=0.6, ccw=False)
    sb.line(t, c['RU'], p=1.0)
    return sb


def build(cfg=None):
    c = dict(DEF)
    if cfg:
        c.update(cfg)
    C, A, U, RU, RO, rx, cp, B = c['C'], c['A'], c['U'], c['RU'], c['RO'], c['rx'], c['cap_p'], c['ball']
    t = math.tan(math.radians(c['slant']))
    S = []

    # ======================================================== V (point at 0,0)
    H = C - 14
    phi_l = final_to_upright(c['v_lean'], t) + 180       # heading DOWN the left arm
    phi_l = (phi_l + 180) % 360 - 180
    # top of left arm
    dl = _dir(phi_l)
    Lt = (dl[0] / dl[1] * H, H)                           # point on the arm line at height H
    phi_r = final_to_upright(c['v_lean'] + c['v_open'], t)  # heading UP the right arm
    if c['v_entry'] == 'hook':
        r = 15.0
        S0 = hook_start(Lt, phi_l, r, 64, cw=True)
        d64 = _dir(64)
        sb = SB(S0[0] - d64[0] * 16, S0[1] - d64[1] * 16, 64, p=0.0, ball0=B)
        sb.line(*S0, p=0.0)
        sb.turn_to(r, phi_l, p=0.3, direction=-1)
        sb.fwd(46, p=cp)
    elif c['v_entry'] == 'clean':
        sb = SB(Lt[0] - dl[0] * 12, Lt[1] - dl[1] * 12, phi_l, p=0.05)
        sb.line(*Lt, p=0.8 * cp)
    else:  # loop entry: a closed oval loop that starts on the arm and drops into the shade
        r = 15.0
        S0 = hook_start(Lt, phi_l, r, 40, cw=True)
        sb = SB(S0[0] + 34, S0[1] - 46, 170, p=0.0)
        sb.to(S0[0] - 36, S0[1] - 4, 90, p=0.0, k=0.62)
        sb.to(S0[0], S0[1], 40, p=0.0, k=0.62)
        sb.turn_to(r, phi_l, p=0.3, direction=-1)
        sb.fwd(46, p=cp)
    sb.line(dl[0] / dl[1] * 16, 16, p=cp)
    sb.line(0, 0, p=0.3)
    S.append(sb)
    # right arm
    dr = _dir(phi_r)
    if c['v_arm'] in ('crook', 'flick'):
        sb = SB(0, 0, phi_r, p=0.0)
        sb.until_y(C - 34, p=0.0)
        if c['v_arm'] == 'crook':
            sb.arc(13, 205, p=0.35)
            sb.end(B)
        else:
            sb.to(sb.x + 30, C, -10, p=0.0, k=0.6)
            sb.end(B * 0.8)
        S.append(sb)

    # ======================================================== a n
    ya = 50.0
    xarm = dr[0] / dr[1] * ya
    a1 = xarm + 40 + rx                     # bowl centre
    sa = a1 + rx                            # a stem
    S.append(bowl(a1, rx, X, c))
    n1, n2 = sa + U, sa + 2 * U
    sb = stem(sa, X, c)
    join(sb, sa, n1, c)
    sb.line(n1, 14, p=1.0)
    sb.line(n1, 0, p=0.45)
    S.append(sb)
    sb = arch_into(n1, n2, c)
    a_exit, _, _ = internal_tangent((n2 + RU, RU), RU, True, (n2 + U - RO, X - RO), RO, False)
    sb.turn_to(RU, a_exit, p=0.0, direction=1)
    sb.fwd(30, p=0.0)
    S.append(sb)

    # ======================================================== I
    Is = n2 + c['gap_nI']
    m1 = Is + 74.0
    m2 = m1 + U
    if c['v_arm'] == 'canopy':
        sb = SB(0, 0, phi_r, p=0.0)
        sb.until_y(C * c.get('can_rise', 0.72), p=0.0)
        rt = c.get('can_turn', 24.0)
        ap = C + c.get('can_apex', 0.0)
        if c.get('can_apex', 0.0):
            xm = (sb.x + Is) / 2 + c.get('can_shift', 0.0)
            sb.to(xm, ap, 0, p=0.0, k=c.get('can_k', 0.6))
            sb.to(Is - rt, C, -c.get('can_fall', 6.0), p=0.0, k=0.55)
            sb.turn_to(rt, -90, p=0.4, direction=-1)
        else:
            sb.to(Is - rt, C, 0, p=0.0, k=c.get('can_k', 0.6))
            sb.turn_to(rt, -90, p=0.4, direction=-1)
    elif c['i_top'] == 'hook':
        sb = SB(Is - 66, C - 46, 56, p=0.0, ball0=B)
        sb.to(Is - 22, C, 0, p=0.0, k=0.58)
        sb.turn_to(22, -90, p=0.85 * cp, direction=-1)
    else:  # 'wave': a calm cap stroke from the left that dips before the stem
        sb = SB(Is - 92, C - 30, 40, p=0.0, ball0=B)
        sb.to(Is - 50, C - 6, -6, p=0.0, k=0.6)
        sb.to(Is - 18, C, 4, p=0.0, k=0.6)
        sb.turn_to(18, -90, p=0.85 * cp, direction=-1)
    sb.line(Is, C - 70, p=cp)
    rf = 24.0
    sb.line(Is, rf, p=cp)
    if c['i_foot'] == 'loop':
        sb.arc(rf, -90, p=0.3)           # heading west at the baseline
        sb.arc(19, -90, p=0.0)           # up the left side of the loop
        sb.arc(19, -90, p=0.0)           # over the top, heading east
        sb.line(sb.x + 24, sb.y, p=0.0)  # across the stem
        connect_from_heading(sb, 20, (m1 - RO, X - RO), RO)
        sb.turn_to(RO, -90, p=0.25, direction=-1)
        sb.line(m1, 14, p=1.0)
        sb.line(m1, 0, p=0.45)
        S.append(sb)
    else:
        sb.arc(rf, -90, p=0.3)
        sb.arc(14, -60, p=0.0)
        sb.end(B * 0.8)
        S.append(sb)
        sb = SB(m1 - 46, 22, 50, p=0.0)
        connect_from_heading(sb, 18, (m1 - RO, X - RO), RO)
        sb.turn_to(RO, -90, p=0.25, direction=-1)
        sb.line(m1, 0, p=1.0)
        S.append(sb)

    # ======================================================== n d
    dcx = m2 + 44 + rx
    ds = dcx + rx
    sb = arch_into(m1, m2, c)
    sb.turn_to(RU, 52, p=0.0, direction=1)
    # hug: run up the bowl's left side and over its top (hidden inside the bowl) to the bowl start
    t_hit = 208.0
    hx, hy = dcx + rx * math.cos(math.radians(t_hit)), 50 + 50 * math.sin(math.radians(t_hit))
    htan = math.degrees(math.atan2(-50 * math.cos(math.radians(t_hit)), rx * math.sin(math.radians(t_hit))))
    sb.to(hx, hy, htan, p=0.0, k=0.55)
    sb.ellipse(dcx, 50, rx, 50, 38, p=0.0, ccw=False)
    S.append(sb)
    S.append(bowl(dcx, rx, A, c))
    sb = stem(ds, A, c, ramp=70)
    rs = ds + U
    join(sb, ds, rs, c)
    sb.line(rs, 14, p=1.0)
    sb.line(rs, 0, p=0.45)
    S.append(sb)

    # ======================================================== r a
    sb = SB(rs, 0, 90, p=0.0)
    sb.line(rs, 58, p=0.0)
    sb.ellipse(rs + 20, 58, 20, X - 58, 90, p=0.0, ccw=False)
    sb.arc(12, -55, p=0.2)
    sb.end(B * 0.95)
    S.append(sb)
    a2 = rs + 54 + rx
    sa2 = a2 + rx
    S.append(bowl(a2, rx, X, c))
    sb = stem(sa2, X, c)
    if c['end'] == 'tail':
        sb.turn_to(RU, a_exit, p=0.0, direction=1)
        sb.fwd(34, p=0.0)
    else:
        sb.turn_to(RU, a_exit, p=0.0, direction=1)
        sb.fwd(40, p=0.0)
        sb.arc(14, 160, p=0.0)
        sb.to(m1, -40, 180, p=0.05, k=0.5)
        sb.to(Is - 40, -34, 172, p=0.0)
    S.append(sb)
    return S, c
