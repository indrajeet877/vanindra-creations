import mstudy, mono
its = [
 ('A rise.60 dIs64 loop', mono.m_canopy({}, rise=.6), {}),
 ('B rise.60 dIs34 loop', mono.m_canopy({}, rise=.6, dIs=34), {}),
 ('C rise.42 dIs64 loop', mono.m_canopy({}, rise=.42), {}),
 ('D rise.60 dIs64 under', mono.m_canopy({}, rise=.6, foot='under'), {}),
 ('E Is=60 (I lands near V)', mono.m_canopy({}, rise=.5, Is=58, foot='under'), {}),
 ('F rise.75 rc30 ball', mono.m_canopy({}, rise=.75, rc=30, foot='ball'), {}),
 ('G rise.5 dIs90 loop', mono.m_canopy({}, rise=.5, dIs=90), {}),
 ('H rise.6 dIs50 apex+20', mono.m_canopy({}, rise=.6, dIs=50, apex=272, foot='ball'), {}),
]
mstudy.study(its, 'mstudy')
