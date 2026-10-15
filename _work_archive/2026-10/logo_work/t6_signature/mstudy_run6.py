import mstudy, sig
pk = dict(hair=7, shade=26)
def M(**kw):
    base = dict(m_dIs=78, m_k=.6, m_turn=24, m_rise=.6)
    base.update(kw)
    return sig.mark_strokes(base)[0]
its = [
 ('a fade30 e1.2, I taper36', M(v_fade=30, v_fade_ease=1.2, i_tail=36, i_ease=1.2), {'_pen': pk}),
 ('b fade30, I blunt', M(v_fade=30, v_fade_ease=1.2, m_foot='blunt'), {'_pen': pk}),
 ('c fade40 e1.5, I taper44 e1.5', M(v_fade=40, v_fade_ease=1.5, i_tail=44, i_ease=1.5), {'_pen': pk}),
 ('d fade22 e1, I taper26', M(v_fade=22, v_fade_ease=1.0, i_tail=26, i_ease=1.0), {'_pen': pk}),
 ('e = a, wordmark weight', M(v_fade=30, v_fade_ease=1.2, i_tail=36, i_ease=1.2), {}),
 ('f = a, small weight', M(v_fade=30, v_fade_ease=1.2, i_tail=36, i_ease=1.2), {'_pen': dict(hair=13, shade=36)}),
]
mstudy.study(its, 'mstudy6', cols=3)
