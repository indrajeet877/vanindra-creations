import mstudy, mono
pk = dict(hair=8, shade=30)
its = [
 ('a rise.62 dIs52 taper', mono.m_vi({}, ), {'_pen': pk}),
 ('b rise.5 dIs40 taper', mono.m_vi({}, rise=.5, dIs=40), {'_pen': pk}),
 ('c rise.72 dIs62 rc22', mono.m_vi({}, rise=.72, dIs=62, rc=22), {'_pen': pk}),
 ('d apex+16 dIs46', mono.m_vi({}, rise=.6, dIs=46, apex=268), {'_pen': pk}),
 ('e no hook, blunt', mono.m_vi({}, hook=False, end='blunt'), {'_pen': pk}),
 ('f lean -14', mono.m_vi({}, lean=-14, dIs=48), {'_pen': pk}),
 ('g exit', mono.m_vi({}, end='exit'), {'_pen': pk}),
 ('h wordmark weight', mono.m_vi({}), {}),
]
mstudy.study(its, 'mstudy2')
