"""Brute-force enumeration of symmetric, non-degenerate kolam lines on small V dot sets."""
import math, sys, itertools, json
sys.path.insert(0, '.')
from kolam import *

def mirror_name(n):
    return n.replace('L', '#').replace('R', 'L').replace('#', 'R')

def canon(seq):
    n = len(seq)
    rots = [tuple(seq[i:] + seq[:i]) for i in range(n)]
    rev = [(a, -s) for a, s in reversed(seq)]
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)

def symmetric(seq):
    m = [(mirror_name(a), -s) for a, s in seq]
    return canon(m) == canon(seq)

def seg_point_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-12)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def arcs_overlap(a1, s1, a2, s2):
    # normalise to ccw intervals [start, start+len]
    def iv(a, s):
        if s < 0: a, s = a + s, -s
        return a % TAU, s
    x0, l0 = iv(a1, s1); x1, l1 = iv(a2, s2)
    for k in (-1, 0, 1):
        lo = max(x0, x1 + k * TAU); hi = min(x0 + l0, x1 + k * TAU + l1)
        if hi - lo > 1e-3:
            return True
    return False

def valid(D, seq, r, clear=0.85):
    visits = [(D[a], r, s) for a, s in seq]
    try:
        segs = build(visits)
    except ValueError:
        return None
    arcs = {}
    names = [a for a, s in seq]
    # map arc segments to dot names
    ai = 0
    lines = []
    for sg in segs:
        if sg[0] == 'A':
            arcs.setdefault(sg[1], []).append((sg[3], sg[4]))
        else:
            lines.append(sg)
    for c, lst in arcs.items():
        for i in range(len(lst)):
            if abs(lst[i][1]) > 1.9 * math.pi:
                return None
            for j in range(i + 1, len(lst)):
                if arcs_overlap(*lst[i], *lst[j]):
                    return None
    for (_, p0, p1) in lines:
        for name, c in D.items():
            if math.hypot(p0[0]-c[0], p0[1]-c[1]) < r * 1.01 or math.hypot(p1[0]-c[0], p1[1]-c[1]) < r * 1.01:
                continue
            if seg_point_dist(c, p0, p1) < r * clear:
                return None
    # every dot visited
    if set(names) != set(D):
        return None
    return segs

def enum(D, maxlen, r, first='L2'):
    names = list(D)
    found = {}
    for n in range(3, maxlen + 1):
        for rest in itertools.product(names, repeat=n - 1):
            seqn = (first,) + rest
            if any(seqn[i] == seqn[(i + 1) % n] for i in range(n)):
                continue
            if any(seqn.count(x) > 2 for x in names) or set(seqn) != set(names):
                continue
            for dirs in itertools.product((1, -1), repeat=n - 1):
                seq = [(first, 1)] + list(zip(rest, dirs))
                c = canon(seq)
                if c in found:
                    continue
                if not symmetric(seq):
                    continue
                segs = valid(D, seq, r)
                if segs is None:
                    continue
                found[c] = seq
    return found

if __name__ == '__main__':
    out = {}
    D3 = {'L2': (-1, 2), 'B': (0, 0), 'R2': (1, 2)}
    f3 = enum(D3, 6, 0.38)
    D5 = {'L2': (-1, 2), 'L1': (-0.5, 1), 'B': (0, 0), 'R1': (0.5, 1), 'R2': (1, 2)}
    f5 = enum(D5, 8, 0.34)
    print(len(f3), len(f5))
    json.dump({'d3': [list(map(list, v)) for v in f3.values()], 'd5': [list(map(list, v)) for v in f5.values()]}, open('enum.json', 'w'))
