"""Exact stroke construction: lines, circular arcs, ellipse arcs, tangent connectives.

A stroke is built by a turtle (SB) in upright y-up space. Every segment is an exact cubic:
  line        : handles at 1/3
  circle arc  : split into <=90 deg pieces, handle = r * 4/3 * tan(phi/4)
  ellipse arc : affine image of the circle arc (exact same construction)
  hermite     : tangent-intersection rule (only for free flourish curves)
The turtle keeps current point + tangent so continuity (G1) is guaranteed by construction.
Each segment carries pressure at its start and end (p0, p1).
"""
import math

D2R = math.pi / 180.0


def _dir(a):
    return (math.cos(a * D2R), math.sin(a * D2R))


class SB:
    def __init__(self, x, y, ang, p=0.0, ball0=0.0):
        self.x, self.y, self.ang, self.p = float(x), float(y), float(ang), float(p)
        self.segs = []
        self.ball0, self.ball1 = ball0, 0.0
        self.pen = None

    # ------------------------------------------------------------------ primitives
    def _add(self, c1, c2, x, y, ang, p, ease=None):
        p = self.p if p is None else p
        self.segs.append(((self.x, self.y), c1, c2, (x, y), self.p, p, ease))
        self.x, self.y, self.ang, self.p = x, y, ang, p
        return self

    def line(self, x, y, p=None, ease=None):
        a = math.atan2(y - self.y, x - self.x) / D2R
        dx, dy = (x - self.x) / 3, (y - self.y) / 3
        return self._add((self.x + dx, self.y + dy), (x - dx, y - dy), x, y, a, p, ease)

    def fwd(self, L, p=None, ease=None):
        d = _dir(self.ang)
        return self.line(self.x + d[0] * L, self.y + d[1] * L, p, ease)

    def until_y(self, y, p=None):
        """Straight on along the current tangent until height y."""
        d = _dir(self.ang)
        t = (y - self.y) / d[1]
        return self.line(self.x + d[0] * t, self.y + d[1] * t, p)

    def arc(self, r, sweep, p=None, ease=None):
        """Circular arc, radius r, turning left (sweep>0, CCW) or right (sweep<0)."""
        p_end = self.p if p is None else p
        p_start = self.p
        n = max(1, int(math.ceil(abs(sweep) / 90.0 - 1e-9)))
        step = sweep / n
        sgn = 1 if sweep > 0 else -1
        # centre is to the left (CCW) / right (CW) of the tangent
        nx, ny = _dir(self.ang + 90 * sgn)
        cx, cy = self.x + nx * r, self.y + ny * r
        for i in range(n):
            a0 = self.ang
            a1 = a0 + step
            h = r * 4.0 / 3.0 * math.tan(abs(step) * D2R / 4)
            # point at end
            pa = math.atan2(self.y - cy, self.x - cx) / D2R + step
            x1, y1 = cx + r * math.cos(pa * D2R), cy + r * math.sin(pa * D2R)
            d0, d1 = _dir(a0), _dir(a1)
            pp = p_start + (p_end - p_start) * (i + 1) / n
            self._add((self.x + d0[0] * h, self.y + d0[1] * h), (x1 - d1[0] * h, y1 - d1[1] * h), x1, y1, a1, pp, ease)
        return self

    def turn_to(self, r, ang, p=None, direction=None):
        """Arc of radius r until the tangent equals ang. direction: +1 CCW, -1 CW, None = shortest."""
        d = (ang - self.ang + 180) % 360 - 180
        if direction == 1 and d < 0:
            d += 360
        if direction == -1 and d > 0:
            d -= 360
        if abs(d) < 1e-9:
            return self
        return self.arc(r, d, p)

    def ellipse(self, cx, cy, rx, ry, t1, p=None, ccw=True):
        """Follow the ellipse (cx,cy,rx,ry) from the current point to parametric angle t1 (deg)."""
        t0 = math.atan2((self.y - cy) / ry, (self.x - cx) / rx) / D2R
        if ccw:
            while t1 <= t0 + 1e-9:
                t1 += 360
        else:
            while t1 >= t0 - 1e-9:
                t1 -= 360
        sweep = t1 - t0
        n = max(1, int(math.ceil(abs(sweep) / 90.0 - 1e-9)))
        step = sweep / n
        p_start, p_end = self.p, (self.p if p is None else p)
        for i in range(n):
            a0, a1 = t0 + step * i, t0 + step * (i + 1)
            h = 4.0 / 3.0 * math.tan(abs(step) * D2R / 4) * (1 if step > 0 else -1)
            P0 = (cx + rx * math.cos(a0 * D2R), cy + ry * math.sin(a0 * D2R))
            P3 = (cx + rx * math.cos(a1 * D2R), cy + ry * math.sin(a1 * D2R))
            T0 = (-rx * math.sin(a0 * D2R), ry * math.cos(a0 * D2R))
            T1 = (-rx * math.sin(a1 * D2R), ry * math.cos(a1 * D2R))
            c1 = (P0[0] + T0[0] * h, P0[1] + T0[1] * h)
            c2 = (P3[0] - T1[0] * h, P3[1] - T1[1] * h)
            ang = math.atan2(T1[1] * (1 if step > 0 else -1), T1[0] * (1 if step > 0 else -1)) / D2R
            pp = p_start + (p_end - p_start) * (i + 1) / n
            self.x, self.y = P0
            self._add(c1, c2, P3[0], P3[1], ang, pp)
        return self

    def to(self, x, y, ang, p=None, k=0.55, k1=None):
        """Free hermite curve to (x, y) arriving with tangent ang (tangent-intersection tension)."""
        d0, d1 = _dir(self.ang), _dir(ang)
        dx, dy = x - self.x, y - self.y
        chord = math.hypot(dx, dy)
        det = d0[0] * (-d1[1]) - d0[1] * (-d1[0])
        h0 = h1 = chord * 0.36
        if abs(det) > 1e-6:
            s = (dx * (-d1[1]) - dy * (-d1[0])) / det
            u = (d0[0] * dy - d0[1] * dx) / det
            if 1e-6 < s < 3 * chord and 1e-6 < u < 3 * chord:
                h0, h1 = k * s, (k if k1 is None else k1) * u
        return self._add((self.x + d0[0] * h0, self.y + d0[1] * h0), (x - d1[0] * h1, y - d1[1] * h1), x, y, ang, p)

    def end(self, ball=0.0):
        self.ball1 = ball
        return self


def internal_tangent(c1, r1, ccw1, c2, r2, ccw2):
    """Direction (deg) and tangent points of the line leaving circle 1 and arriving on circle 2.
    ccw1/ccw2: travel sense on each circle (True = counter-clockwise)."""
    s1 = 1 if ccw1 else -1   # centre on the left of travel if ccw
    s2 = 1 if ccw2 else -1
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    # unknown direction a: n = left normal; (c1 - P1).n = s1*r1 ; (c2 - P2).n = s2*r2 ; P2 - P1 parallel to dir
    # => (c2 - c1).n = s2*r2 - s1*r1
    k = s2 * r2 - s1 * r1
    D = math.hypot(dx, dy)
    base = math.atan2(dy, dx) / D2R
    # (c2-c1).n = D cos(base - (a+90)) = k
    best = None
    for sgn in (1, -1):
        a = base - 90 - sgn * math.acos(max(-1, min(1, k / D))) / D2R
        dd = _dir(a)
        nl = _dir(a + 90)
        P1 = (c1[0] - s1 * r1 * nl[0], c1[1] - s1 * r1 * nl[1])
        P2 = (c2[0] - s2 * r2 * nl[0], c2[1] - s2 * r2 * nl[1])
        if (P2[0] - P1[0]) * dd[0] + (P2[1] - P1[1]) * dd[1] > 0:
            best = (a, P1, P2)
            break
    return best
