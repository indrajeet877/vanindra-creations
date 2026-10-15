"""F1 polish: the global (Latin) avatar letter.
Judges: the old global avatar was a plain wedge under a full-bleed bar (a dropdown caret / nabla / coat hanger).
Redrawn with the va's DNA so it is the system's letter, the Latin sibling of the va mark:
- the same line, overhanging the letter by the same amount as the va mark (no longer full-bleed, so the circle crop
  never turns it into a chord);
- the left arm is the alphabet's leaf (hairline where it leaves the line, swelling to the foot) with the va's shoulder;
- a sharp point below;
- the right arm rises from the point into a short danda stub that hangs from the line, as the va's loop rises into
  its danda. So the counter is not a triangle: its right side is vertical (the danda), which kills the nabla.
Units: line top y=0, baseline y=100."""
from r3geo import *

VS = dict(H=100.0, b=9.5, S=13.0, W=74.0, ys=40.0, h=10.0, P=None, o=1.5,
          t0=6.0, ko1=7.0, ko2=4.0, ki1=1.0, ki2=-9.0, uo1=0.28, uo2=0.70, ui1=0.30, ui2=0.75,
          ovl=3.0, ovr=3.0)


def v_stub(**kw):
    p = dict(VS); p.update(kw)
    H, b, S, W, ys, h, o = p['H'], p['b'], p['S'], p['W'], p['ys'], p['h'], p['o']
    P = p['P'] or (W * 0.40, H + o)
    xs = W - S
    # right arm: outer edge from P to the stub's outer foot corner (W, ys); inner edge offset by h (up-left)
    dx, dy = W - P[0], ys - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L                     # left normal of travel P -> (W, ys): points up-left (into counter)
    if nx > 0:
        nx, ny = -nx, -ny
    Pi, Ri = (P[0] + nx * h, P[1] + ny * h), (W + nx * h, ys + ny * h)
    yi = line_y(Pi, Ri, xs)                      # where the arm's inner edge meets the stub's inner edge
    right = poly([P, (W, ys), (W, 0.0), (xs, 0.0), (xs, yi), Pi])
    # left arm: the leaf (outer bows out = the shoulder), cut by the right arm's inner edge
    lf = dict(t0=p['t0'], ko1=p['ko1'], ko2=p['ko2'], ki1=p['ki1'], ki2=p['ki2'], uo1=p['uo1'], uo2=p['uo2'],
              ui1=p['ui1'], ui2=p['ui2'])
    outer, inner = leaf_chord((0.0, 0.0), P, **lf)
    t = c_isect_line(*inner, Pi, Ri)
    (a0, a1, a2, Q), _ = csplit(*inner, t)
    O0, c1o, c2o, _ = outer
    left = path_from([('M', *O0), ('C', *c1o, *c2o, *P), ('L', *Q), ('C', *a2, *a1, *a0)])
    g = U(left, right)
    g = I(g, rect(-20, 0, W + 5, H + o + 1))
    xmin = bbox(g)[0]
    g = U(g, rect(xmin - p['ovl'], 0, W + p['ovr'], b))
    return norm(g), p
