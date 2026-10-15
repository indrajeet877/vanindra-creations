import mstudy, mono
pk = dict(hair=6.5, shade=25)
its = [
 ('a taper', mono.m_vi2({}), {'_pen': pk}),
 ('b taper bend', mono.m_vi2({}, bend=-10), {'_pen': pk}),
 ('c kick', mono.m_vi2({}, end='kick'), {'_pen': pk}),
 ('d blunt', mono.m_vi2({}, end='blunt'), {'_pen': pk}),
 ('e taper rise.68 dIs58', mono.m_vi2({}, rise=.68, dIs=58), {'_pen': pk}),
 ('f taper top+18 rc24', mono.m_vi2({}, top_dy=18, rc=24), {'_pen': pk}),
 ('g kick, no hook', mono.m_vi2({}, end='kick', hook=False), {'_pen': pk}),
 ('h taper heavy small', mono.m_vi2({}), {'_pen': dict(hair=10, shade=32)}),
]
mstudy.study(its, 'mstudy3')
