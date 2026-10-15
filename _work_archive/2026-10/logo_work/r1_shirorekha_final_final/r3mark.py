"""The va / V mark: one leaf (the bowl) + one hairline return + one danda, all hung from one headline.
Bar top y=0, baseline y=H=100. Leaf edges are single cubic Beziers defined by tangent angles + handle lengths."""
from r3geo import *

MARK = dict(H=100, b=9.5, S=13.0, h=8.0, xs=58.0, px=31.0, py=88.0, yj=0.50,
            leaf=dict(t0=4.0, ko1=7.0, ko2=6.0, ki1=-3.0, ki2=-16.0),
            ovl=3.0, ovr=3.0, notch=None)


def _dir_down(angle_from_vertical_deg):
    a = math.radians(angle_from_vertical_deg)
    return (math.sin(a), math.cos(a))


def _dir_below_h(angle_below_horizontal_deg):
    a = math.radians(angle_below_horizontal_deg)
    return (math.cos(a), math.sin(a))


def leaf_curves(b, px, py, t0, ao0, ho0, bo, ho1, ai0, hi0, bi, hi1):
    O0 = (0.0, 0.0)
    P = (px, py)
    L = math.hypot(px, py)
    d0 = _dir_down(ao0)
    d1 = _dir_below_h(bo)
    outer = (O0, (O0[0] + d0[0] * ho0 * L, O0[1] + d0[1] * ho0 * L), (P[0] - d1[0] * ho1 * L, P[1] - d1[1] * ho1 * L), P)
    xb = c_x_at_y(*outer, b)
    I0 = (xb + t0, float(b))
    Li = math.hypot(P[0] - I0[0], P[1] - I0[1])
    e0 = _dir_down(ai0)
    e1 = _dir_below_h(bi)
    inner = (I0, (I0[0] + e0[0] * hi0 * Li, I0[1] + e0[1] * hi0 * Li), (P[0] - e1[0] * hi1 * Li, P[1] - e1[1] * hi1 * Li), P)
    return outer, inner


def leaf_bowl(p, xs, yj_abs):
    b, h = p['b'], p['h']
    lf = dict(LEAF); lf.update(p['leaf'])
    outer, inner = leaf_chord((0.0, 0.0), (p['px'], p['py']), **lf)
    O0, c1o, c2o, P = outer
    J = (xs, yj_abs)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L          # up-left normal for an up-right chord
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_y(Pi, Ji, xs))
    t = c_isect_line(*inner, Pi, Ji)
    (a0, a1, a2, Q), _ = csplit(*inner, t)
    cmds = [('M', *O0), ('C', *c1o, *c2o, *P), ('L', *J), ('L', xs + 1.0, J[1]), ('L', xs + 1.0, J2[1]), ('L', *J2),
            ('L', *Q), ('C', *a2, *a1, *a0), ('L', a0[0], 0.0)]
    shape = path_from(cmds)
    xmin, _ = c_extreme_x(*outer)
    return shape, dict(P=P, Q=Q, I0=a0, J=J, J2=J2, outer=outer, inner=inner, xmin=xmin)


def va_mark(**kw):
    p = dict(MARK)
    p.update(kw)
    H, b, S, h, xs = p['H'], p['b'], p['S'], p['h'], p['xs']
    bowl, info = leaf_bowl(p, xs, p['yj'] * H)
    xL = info['xmin'] - p['ovl']
    x1 = xs + S + p['ovr']
    stem = rect(xs, 0, xs + S, H)
    bar = rect(xL, 0, x1, b)
    if p.get('gap'):
        gp = p['gap']
        # the leaf stops short of the line: cut a level slot of height gp under the bar across the leaf
        bowl = D(bowl, rect(xL - 10, 0, xs - 0.01, b + gp))
        if p.get('top_cut', 0):
            bowl = D(bowl, poly([(xL - 10, b + gp), (info['I0'][0] + 30, b + gp), (xL - 10, b + gp + p['top_cut'])]))
    g = U(bowl, stem, bar)
    if p.get('notch'):
        n = p['notch']
        I0 = info['I0']
        g = D(g, poly([(I0[0] - 0.3, b - n * 0.6), (I0[0] + n * 1.2, b - n * 0.6), (I0[0] + n * 0.1, b + n * 0.9)]))
    g = I(g, rect(xL - 5, 0, x1 + 5, max(H, p['py']) + 0.01))
    info.update(xL=xL, x1=x1, p=p)
    return g, info


SMALL = dict(b=13.5, S=17.0, h=11.5, xs=57.0, px=29.0, py=86.0, leaf=dict(t0=7.0, ko1=7.0, ko2=6.0, ki1=-5.0, ki2=-18.0))


# ------------------------------------------------------------------ loop variant (rounder, closer to a true va loop)
LOOP = dict(H=100, b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0,
            a=7.0,            # outward bulge of the left side (handle offset)
            bx=24.0, by=86.0, # lowest point of the bowl (outer)
            kb=10.0,          # half-width of the round bottom handles (0 -> sharp point)
            tb=0.0,           # bottom tangent angle in degrees (0 = level)
            yj=0.47, phi=38.0, kj=14.0,     # where/how the outer return meets the danda
            t0=4.5,           # leaf width at the bar
            qx=29.0, qy=73.0, kq=6.0,      # counter bottom
            hj=9.0,           # vertical thickness of the return where it meets the danda
            ai=8.0)           # inner left edge bulge


def loop_bowl(p):
    xs, b = p['xs'], p['b']
    O0 = (0.0, 0.0)
    B = (p['bx'], p['by'])
    tb = math.radians(p['tb'])
    tx, ty = math.cos(tb), math.sin(tb)            # tangent at B travelling right (and down for tb>0 -> we use up)
    J = (xs, p['yj'] * p['H'])
    ph = math.radians(p['phi'])
    o_c1 = (O0[0] - p['a'], B[1] * 0.40)
    o_c2 = (B[0] - p['kb'] * tx, B[1] - p['kb'] * (-ty))
    o_c3 = (B[0] + p['kb'] * tx, B[1] + p['kb'] * (-ty))
    o_c4 = (J[0] - p['kj'] * math.cos(ph), J[1] + p['kj'] * math.sin(ph))
    J2 = (xs, J[1] - p['hj'])
    Q = (p['qx'], p['qy'])
    i_c1 = (J2[0] - p['kj'] * 0.8 * math.cos(ph), J2[1] + p['kj'] * 0.8 * math.sin(ph))
    i_c2 = (Q[0] + p['kq'] * 1.0, Q[1] - p['kq'] * 0.3)
    I0 = (O0[0] + p['t0'] + 0.0, b)
    i_c3 = (Q[0] - p['kq'] * 0.6, Q[1] - p['kq'] * 1.2)
    i_c4 = (I0[0] - p['ai'] * 0.2, I0[1] + (Q[1] - I0[1]) * 0.45)
    cmds = [('M', *O0), ('C', *o_c1, *o_c2, *B), ('C', *o_c3, *o_c4, *J), ('L', xs + 1, J[1]), ('L', xs + 1, J2[1]),
            ('L', *J2), ('C', *i_c1, *i_c2, *Q), ('C', *i_c3, *i_c4, *I0), ('L', I0[0], 0.0)]
    shape = path_from(cmds)
    xmin, _ = c_extreme_x(O0, o_c1, o_c2, B)
    return shape, dict(xmin=xmin, B=B, Q=Q, J=J, J2=J2, I0=I0)


def va_loop(**kw):
    p = dict(LOOP); p.update(kw)
    H, b, S, xs = p['H'], p['b'], p['S'], p['xs']
    bowl, info = loop_bowl(p)
    xL = info['xmin'] - p['ovl']
    x1 = xs + S + p['ovr']
    g = U(bowl, rect(xs, 0, xs + S, H), rect(xL, 0, x1, b))
    g = I(g, rect(xL - 5, 0, x1 + 5, H + 0.01))
    info.update(xL=xL, x1=x1, p=p)
    return g, info


# ------------------------------------------------------------------ true-loop va: the leaf-loop hangs from the danda
TLOOP = dict(H=100, b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0,
             top=(3.0, 26.0),      # the loop's top-left point (where the leaf starts)
             jt=20.0,              # where the loop's top hairline meets the danda (y)
             P=(26.0, 87.0),       # tip
             yj=0.50, h=7.5, ht=5.5,
             leaf=dict(t0=4.0, ko1=8.0, ko2=7.0, ki1=-1.0, ki2=-15.0))


def va_trueloop(**kw):
    p = dict(TLOOP); p.update(kw)
    H, b, S, xs, h = p['H'], p['b'], p['S'], p['xs'], p['h']
    O0 = p['top']
    P = p['P']
    lf = dict(LEAF); lf.update(p['leaf'])
    outer, inner = leaf_chord(O0, P, **lf)
    J = (xs, p['yj'] * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_y(Pi, Ji, xs))
    t = c_isect_line(*inner, Pi, Ji)
    # top hairline: from the loop's top-left up/right to the danda; lower edge from inner start
    T1 = (xs, p['jt'])                       # upper edge meets danda
    T0 = O0                                  # upper edge starts at the leaf's outer top
    # lower edge: offset down by ht
    ddx, ddy = T1[0] - T0[0], T1[1] - T0[1]
    LL = math.hypot(ddx, ddy)
    mx, my = -ddy / LL, ddx / LL             # normal pointing down for a rightward line
    if my < 0: mx, my = -mx, -my
    B0, B1 = (T0[0] + mx * p['ht'], T0[1] + my * p['ht']), (T1[0] + mx * p['ht'], T1[1] + my * p['ht'])
    # where the inner leaf edge meets the lower edge of the top hairline
    t_top = c_isect_line(*inner, B0, B1, from_end=False)
    (a0, a1, a2, Qt), rest = csplit(*inner, t_top)
    # re-split the remaining part at the return stroke
    r0, r1, r2, r3 = rest
    t2 = c_isect_line(r0, r1, r2, r3, Pi, Ji)
    (b0, b1, b2, Q), _ = csplit(r0, r1, r2, r3, t2)
    Bj = (xs, line_y(B0, B1, xs))
    _, c1o, c2o, _ = outer
    outer_path = path_from([('M', *O0), ('L', *T1), ('L', xs + 1, T1[1]), ('L', xs + 1, J[1]), ('L', *J), ('L', *P),
                            ('C', *c2o, *c1o, *O0)])
    counter = path_from([('M', *Qt), ('L', *Bj), ('L', *J2), ('L', *Q), ('C', *b2, *b1, *b0)])
    loop = D(outer_path, counter)
    xmin, _ = c_extreme_x(*outer)
    xL = min(xmin, O0[0]) - p['ovl']
    x1 = xs + S + p['ovr']
    g = U(loop, rect(xs, 0, xs + S, H), rect(xL, 0, x1, b))
    return g, dict(xL=xL, x1=x1, p=p)


# ------------------------------------------------------------------ calligraphic one-stroke loop (the way va is written)
CLOOP = dict(H=100, b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0,
             jt=22.0, ht=4.5,                  # loop leaves the danda at y=jt; top stroke thickness
             P=(25.0, 88.0),                   # pointed tip
             yj=0.52, h=8.0,                   # return stroke meets the danda at yj*H, thickness h
             o1=(-16.0, 0.0), o2=(-6.0, 0.62), # outer cubic controls: o1 = (x, dy from jt) ; o2 = (x, frac of the way down to P)
             i1=(-6.0, 0.0), i2=(6.0, 0.70),   # inner cubic controls (same convention, relative to the inner start)
             gap=None)


def va_cloop(**kw):
    p = dict(CLOOP); p.update(kw)
    H, b, S, xs, h = p['H'], p['b'], p['S'], p['xs'], p['h']
    T1 = (xs, p['jt'])
    P = p['P']
    o1 = (p['o1'][0], T1[1] + p['o1'][1])
    o2 = (p['o2'][0], T1[1] + (P[1] - T1[1]) * p['o2'][1])
    outer = (T1, o1, o2, P)
    Bj = (xs, p['jt'] + p['ht'])
    i1 = (p['i1'][0], Bj[1] + p['i1'][1])
    i2 = (p['i2'][0], Bj[1] + (P[1] - Bj[1]) * p['i2'][1])
    inner = (Bj, i1, i2, P)
    J = (xs, p['yj'] * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_y(Pi, Ji, xs))
    t = c_isect_line(*inner, Pi, Ji)
    (a0, a1, a2, Q), _ = csplit(*inner, t)
    shape = path_from([('M', *T1), ('C', *o1, *o2, *P), ('L', *J), ('L', xs + 1, J[1]), ('L', xs + 1, T1[1])])
    counter = path_from([('M', *Bj), ('C', *a1, *a2, *Q), ('L', *J2), ('L', xs + 1, J2[1]), ('L', xs + 1, Bj[1])])
    loop = D(shape, counter)
    xmin, _ = c_extreme_x(*outer)
    xL = xmin - p['ovl']
    x1 = xs + S + p['ovr']
    g = U(loop, rect(xs, 0, xs + S, H), rect(xL, 0, x1, b))
    return g, dict(xL=xL, x1=x1, p=p, xmin=xmin, counter=counter, P=P, J=J, T1=T1)
