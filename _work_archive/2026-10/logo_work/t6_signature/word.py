"""Skeleton of the 'VanIndra' signature, built from grid nodes (upright space, x-height X=100).

Construction rules (copperplate logic, applied everywhere):
  * every downstroke is parallel to the slant axis (vertical here, sheared later)
  * underturn radius RU and overturn radius RO are constants
  * stem-to-stem unit U is constant inside and between letters
  * bowls are true ellipses (rx, X/2) that start at their top-right and run counter-clockwise
  * connectives are S-curves with horizontal tangents at both turns
"""
from pen import N, St

X = 100.0
DEF = dict(
    C=262.0,         # capital height
    A=214.0,         # d ascender
    U=48.0,          # stem unit
    rx=30.0,         # bowl half-width
    RU=16.0,         # underturn radius
    RO=14.0,         # overturn radius
    cap_p=1.15,      # capital shade multiplier
    ball=5.2,        # terminal ball radius
    v_entry='hook',  # 'hook' | 'clean' | 'loop'
    v_arm='curl',    # 'curl' | 'flick' | 'canopy'
    i_top='hook',    # 'hook' | 'loop'
    i_foot='loop',   # 'loop' | 'plain'
    d_top='cusp',    # 'cusp' | 'curl'
    r_form='arm',    # 'arm' | 'join'
    end='tail',      # 'tail' | 'paraph'
    gap_VI=104.0,    # n2 stem -> I stem
)


def bowl(cx, rx, p_left=1.0):
    return [N(cx + rx * 0.72, X - 9, 156, p=0.0), N(cx, X, 180, p=0.1), N(cx - rx, X / 2, -90, p=p_left),
            N(cx, 0, 0, p=0.25), N(cx + rx, X / 2, 90, p=0.0)]


def underturn(s, c):
    return [N(s, c['RU'] + 2, -90), N(s + c['RU'], 0, 0, p=0.25, k=0.58)]


def overturn_into(t, c, top=X):
    return [N(t - c['RO'], top, 0, p=0.1), N(t, top - c['RO'], -90)]


def build(cfg=None):
    c = dict(DEF)
    if cfg:
        c.update(cfg)
    C, A, U, rx, RU, RO, cp, B = c['C'], c['A'], c['U'], c['rx'], c['RU'], c['RO'], c['cap_p'], c['ball']
    S = []
    # ================================================================ V  (point at x = 0)
    arm_top = 84.0
    if c['v_entry'] == 'hook':
        S.append(St([N(-130, C - 42, 64, p=0), N(-108, C - 2, 4, p=0, k=0.6), N(-92, C - 24, -68, p=0.95 * cp),
                     N(-46, C * 0.48, -69, p=cp), N(-4, 14, -70, p=cp), N(0, 0, -71, p=0.3)], ball0=B))
    elif c['v_entry'] == 'clean':
        S.append(St([N(-100, C, -66, p=0.0), N(-84, C - 40, -68, p=cp), N(-46, C * 0.48, -69, p=cp),
                     N(-4, 14, -70, p=cp), N(0, 0, -71, p=0.3)]))
    elif c['v_entry'] == 'loop':
        S.append(St([N(-74, C - 64, 170, p=0), N(-138, C - 40, 110, p=0), N(-128, C - 2, 30, p=0),
                     N(-102, C - 8, -40, p=0.2), N(-90, C - 30, -68, p=0.95 * cp), N(-46, C * 0.48, -69, p=cp),
                     N(-4, 14, -70, p=cp), N(0, 0, -71, p=0.3)]))
    if c['v_arm'] == 'curl':
        S.append(St([N(0, 0, 64, p=0), N(arm_top - 10, C - 60, 76, p=0), N(arm_top, C - 6, 90, p=0),
                     N(arm_top - 12, C + 8, 180, p=0), N(arm_top - 22, C - 6, -88, p=0.35)], ball1=B))
    elif c['v_arm'] == 'flick':
        S.append(St([N(0, 0, 64, p=0), N(arm_top - 10, C - 60, 76, p=0), N(arm_top + 4, C - 4, 60, p=0),
                     N(arm_top + 24, C + 2, -4, p=0)], ball1=B * 0.8))
    # ================================================================ a n
    a1 = 92.0
    st = a1 + rx
    S.append(St(bowl(a1, rx) + [N(st, X, 90, p=0)]))
    n1, n2 = st + U, st + 2 * U
    S.append(St([N(st, X, -90, p=0.25), N(st, X - 26, -90)] + underturn(st, c) + overturn_into(n1, c) + [N(n1, 0, -90)]))

    def arch(s, t):
        return [N(s, 0, 90, p=0), N(s, X * 0.55, 90, p=0), N(s + (t - s) / 2, X, 0, p=0.1), N(t, X - 24, -90)]

    Is = n2 + c['gap_VI']
    m1 = Is + 58.0
    m2 = m1 + U
    S.append(St(arch(n1, n2) + underturn(n2, c) + [N(n2 + 40, 40, 54, p=0)]))
    # ================================================================ I
    if c['v_arm'] == 'canopy':
        top = [N(0, 0, 64, p=0), N(arm_top - 14, C - 70, 74, p=0), N(arm_top + 20, C - 4, 30, p=0),
               N(arm_top + 70, C + 4, 0, p=0), N(Is - 20, C - 2, -6, p=0), N(Is, C - 26, -86, p=0.85 * cp)]
        b0 = 0
    elif c['i_top'] == 'hook':
        top = [N(Is - 74, C - 44, 62, p=0), N(Is - 46, C - 2, 16, p=0), N(Is - 18, C, -8, p=0),
               N(Is, C - 24, -86, p=0.85 * cp)]
        b0 = B
    else:  # 'loop'
        top = [N(Is - 26, C - 70, 165, p=0), N(Is - 92, C - 44, 100, p=0), N(Is - 66, C, 6, p=0),
               N(Is - 18, C - 1, -10, p=0), N(Is, C - 26, -86, p=0.85 * cp)]
        b0 = 0
    stem = [N(Is, C - 74, -90, p=cp), N(Is, 38, -90, p=cp)]
    if c['i_foot'] == 'loop':
        foot = [N(Is - 18, 0, 180, p=0.3), N(Is - 42, 22, 90, p=0), N(Is - 22, 44, 0, p=0, k=0.6)]
        S.append(St(top + stem + foot + overturn_into(m1, c) + [N(m1, 0, -90)], ball0=b0))
    else:
        foot = [N(Is - 18, 0, 180, p=0.3), N(Is - 36, 14, 120, p=0)]
        S.append(St(top + stem + foot, ball0=b0, ball1=B * 0.8))
        S.append(St([N(m1 - 34, 34, 56, p=0)] + overturn_into(m1, c) + [N(m1, 0, -90)]))
    # ================================================================ n d
    d_c = m2 + 34 + rx
    ds = d_c + rx
    S.append(St(arch(m1, m2) + underturn(m2, c) + [N(d_c - rx, X / 2, 90, p=0), N(d_c, X, 0, p=0),
                                                    N(d_c + rx * 0.72, X - 9, -22, p=0)]))
    if c['d_top'] == 'cusp':
        S.append(St(bowl(d_c, rx) + [N(ds, A, 90, p=0)]))
        dl = St([N(ds, A, -90, p=0.25), N(ds, A - 34, -90)] + underturn(ds, c))
    else:  # curl: ascender rises and curls back over the bowl, finishing in a ball
        S.append(St(bowl(d_c, rx) + [N(ds, A - 20, 90, p=0), N(ds - 16, A + 10, 180, p=0),
                                     N(ds - 30, A - 6, -90, p=0.3)], ball1=B))
        dl = St([N(ds, A - 20, -90, p=0.5), N(ds, A - 50, -90)] + underturn(ds, c))
    S.append(dl)
    # ================================================================ r a
    rs = ds + U
    a2 = rs + 34 + rx + 10
    st2 = a2 + rx
    dl += overturn_into(rs, c) + [N(rs, 0, -90)]
    if c['r_form'] == 'arm':
        S.append(St([N(rs, 0, 90, p=0), N(rs, X * 0.6, 90, p=0), N(rs + 20, X, 6, p=0),
                     N(rs + 36, X - 8, -50, p=0.25)], ball1=B * 0.95))
        S.append(St(bowl(a2, rx) + [N(st2, X, 90, p=0)]))
    else:  # 'join': the r arm runs on into the start of the a
        S.append(St([N(rs, 0, 90, p=0), N(rs, X * 0.6, 90, p=0), N(rs + 22, X, 6, p=0),
                     N(a2 + rx * 0.72, X - 9, -14, p=0)]))
        S.append(St(bowl(a2, rx) + [N(st2, X, 90, p=0)]))
    if c['end'] == 'tail':
        S.append(St([N(st2, X, -90, p=0.25), N(st2, X - 26, -90)] + underturn(st2, c) + [N(st2 + 44, 42, 52, p=0)]))
    else:  # paraph: exit swings up, turns and returns as a calm line under the word
        S.append(St([N(st2, X, -90)] + underturn(st2, c) + [N(st2 + 50, 46, 62, p=0), N(st2 + 54, 72, 110, p=0),
                                                            N(st2 + 36, 64, -125, p=0.05),
                                                            N(st2 - 40, -34, 194, p=0.0), N(m1, -44, 180, p=0.0),
                                                            N(Is - 40, -38, 170, p=0)]))
    return S
