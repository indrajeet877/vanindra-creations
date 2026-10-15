import mstudy, sig
pk = dict(hair=7, shade=26)
def M(**kw):
    base = dict(m_dIs=78, m_k=.6, m_turn=24, m_rise=.6, v_fade=46, i_tail=50)
    base.update(kw)
    return sig.mark_strokes(base)[0]
its = [
 ('a turn_p .32 ramp46 taper', M(), {'_pen': pk}),
 ('b turn_p .6 ramp30 soft', M(i_turn_p=.6, i_ramp=30, v_ramp=30, v_fade_ease='taper_soft', i_ease='taper_soft'), {'_pen': pk}),
 ('c turn_p .75 ramp24 soft, fade56', M(i_turn_p=.75, i_ramp=24, v_ramp=26, v_fade=56, i_tail=58, v_fade_ease='taper_soft', i_ease='taper_soft', v_hook_p=.4), {'_pen': pk}),
]
mstudy.study(its, 'mstudy7', cols=3, size=440)
