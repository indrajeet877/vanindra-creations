"""Small exact-geometry helpers for the Hook Mark (all straight-edged, computed)."""
import math, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import pathops
import vtype as vt

PAL = vt.PALETTE
EM, IV, GO, GL, WH = PAL['emerald'], PAL['ivory'], PAL['gold'], PAL['gold_lt'], PAL['white']


def V(x, y):
    return (float(x), float(y))

def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, s): return (a[0] * s, a[1] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def norm(a):
    l = math.hypot(*a); return (a[0] / l, a[1] / l)
def perp(a):  # rotate +90 in y-down coords (clockwise visually)
    return (-a[1], a[0])
def unit(deg):  # angle measured from +x, counter-clockwise visually (y-down -> negate y)
    r = math.radians(deg); return (math.cos(r), -math.sin(r))


def isect(p, d, q, e):
    """Intersection of line p + t d and q + s e."""
    den = d[0] * e[1] - d[1] * e[0]
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return add(p, mul(d, t))


def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def U(*ps):
    return vt.union(*ps)


def D(a, b):
    return vt.difference(a, b)


def I(a, b):
    return vt.intersection(a, b)


def bbox(p):
    return vt.bounds(p)


def fit(p, box, pad=0.0, align='center'):
    """Scale+translate path p so it fits centred in box=(x,y,w,h)."""
    x0, y0, x1, y1 = vt.bounds(p)
    w, h = x1 - x0, y1 - y0
    bx, by, bw, bh = box
    s = min((bw - 2 * pad) / w, (bh - 2 * pad) / h)
    tx = bx + (bw - w * s) / 2 - x0 * s
    ty = by + (bh - h * s) / 2 - y0 * s
    return vt.transform(p, s, 0, 0, s, tx, ty), s, tx, ty


def tf(p, s, tx, ty):
    return vt.transform(p, s, 0, 0, s, tx, ty)


def d(p):
    return vt.to_d(p)


def pathel(p, fill):
    return f'<path d="{vt.to_d(p)}" fill="{fill}"/>'


def write(path, w, h, body, bg=None, title='VanIndra Creations'):
    s = vt.svg_doc(w, h, body, bg=bg, title=title)
    # round coordinates to keep files small
    import re
    s = re.sub(r'(-?\d+\.\d{3,})', lambda m: f'{float(m.group(1)):.2f}'.rstrip('0').rstrip('.'), s)
    open(path, 'w').write(s)
    return path
