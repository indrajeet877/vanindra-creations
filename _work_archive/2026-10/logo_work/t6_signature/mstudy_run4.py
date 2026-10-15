import mstudy, mono
pk = dict(hair=6.5, shade=25)
its = [
 ('a taper ease', mono.m_vi2({}), {'_pen': pk}),
 ('b fade 70 / I 90', mono.m_vi2({}, i_end_len=90), {'_pen': pk}),
 ('c heavy', mono.m_vi2({}), {'_pen': dict(hair=10, shade=32)}),
 ('d wordmark weight', mono.m_vi2({}), {}),
]
mstudy.study(its, 'mstudy4')
