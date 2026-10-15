import mstudy, sig
pk = dict(hair=7, shade=26)
def M(**kw):
    return sig.mark_strokes(kw)[0]
its = [
 ('a current (dIs50 k.66 turn18)', M(), {'_pen': pk}),
 ('b dIs70 k.62 turn22 rise.62', M(m_dIs=70, m_k=.62, m_turn=22, m_rise=.62), {'_pen': pk}),
 ('c dIs88 k.58 turn26 rise.6', M(m_dIs=88, m_k=.58, m_turn=26, m_rise=.6), {'_pen': pk}),
 ('d dIs88 + lift14 (=wordmark)', M(m_dIs=88, m_k=.58, m_turn=26, m_rise=.6), {'_pen': pk}),
 ('e dIs104 k.56 turn28 rise.6', M(m_dIs=104, m_k=.56, m_turn=28, m_rise=.6), {'_pen': pk}),
 ('f small c', M(m_dIs=88, m_k=.58, m_turn=26, m_rise=.6), {'_pen': dict(hair=13, shade=36)}),
]
mstudy.study(its, 'mstudy5', cols=3)
