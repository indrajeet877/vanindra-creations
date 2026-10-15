import sys, json, itertools, math; sys.path.insert(0, '.')
from kolam import *
from kenum import canon, symmetric, valid

def gen(D, maxlen, r, need_all=True):
    names = list(D)
    found = {}
    for n in range(3, maxlen + 1):
        for rest in itertools.product(names, repeat=n - 1):
            seqn = ('L2',) + rest
            if any(seqn[i] == seqn[(i + 1) % n] for i in range(n)):
                continue
            if any(seqn.count(x) > 2 for x in names) or (need_all and set(seqn) != set(names)):
                continue
            # quick symmetry pre-check on multiset
            mir = {'L2':'R2','R2':'L2','L1':'R1','R1':'L1','B':'B','C':'C'}
            if sorted(mir[x] for x in seqn) != sorted(seqn):
                continue
            for dirs in itertools.product((1, -1), repeat=n - 1):
                seq = [('L2', 1)] + list(zip(rest, dirs))
                c = canon(seq)
                if c in found or not symmetric(seq):
                    continue
                if valid(D, seq, r) is None:
                    continue
                found[c] = seq
    return found

D4 = {'L2': (-1, 2), 'R2': (1, 2), 'C': (0, 0.95), 'B': (0, 0)}
f4 = gen(D4, 7, 0.3)
D6 = {'L2': (-1, 2), 'L1': (-0.55, 1.1), 'C': (0, 0.8), 'B': (0, 0), 'R1': (0.55, 1.1), 'R2': (1, 2)}
f6 = gen(D6, 8, 0.27)
print(len(f4), len(f6))
json.dump({'d4': [list(map(list, v)) for v in f4.values()], 'd6': [list(map(list, v)) for v in f6.values()],
           'D4': D4, 'D6': D6}, open('enum2.json', 'w'))
