import sys, math; sys.path.insert(0,'.')
from kolam import *
from explore2 import V, seq_of
D2 = V(2, 0.5, 1.0)
for spec, r in [('L2+ L1- B+ R1- R2+ R1- B+ L1-', 0.30)]:
    segs = build(seq_of(D2, spec, r))
    for s in segs:
        if s[0]=='A': print('A c=%s r=%.2f a0=%.1f span=%.1f' % (s[1], s[2], math.degrees(s[3]), math.degrees(s[4])))
        else: print('L', tuple(round(v,3) for v in s[1]), tuple(round(v,3) for v in s[2]))
