"""explore.png: every variation explored, grouped by what it taught."""
import sys, base64, subprocess
sys.path.insert(0,'.')
from extras import uri_file, compose
panels=[
 ('work/explore1.png','1 · Hinge built from stock skeletons (E1–E9)',
  'Double hinge (n|I|n) reads "Varhdra": an I that shares a stem with the following n is an h. Sans voices read "Vanlndra". Only a serif capital I, with its symmetric head, can carry the idea. Single hinge only, drawn serif.'),
 ('work/study2.png','2 · Custom drawing, shoulder landing on the I (H1–H5)',
  'Every landing height and angle still reads "VarIndra": the straight shared stem groups with the I, so the n loses its leg and the arch reads as an r ear.'),
 ('work/hinge3.png','3 · Structural fixes (K1–K6)',
  'Trunk, narrow-I, flick-foot all fail in one colour. K6 (complete n, I in gold rising from its leg) finally reads "VanIndra", so the n must stay whole and the I must sit behind it.'),
 ('work/hinge4.png','4 · The answer: the I rises behind the shoulder (B1–B5)',
  'A hairline cut that follows the n\'s shoulder lets the n read whole in front while the I continues through its right leg. Works in one colour; gold on dark is the signature. Chosen: I at ~784, cut 16 (display) / 46 (small).'),
 ('work/avatar4.png','5 · Avatar studies',
  'The hinge glyph alone (n + rising I) is the profile picture. Ivory n + soft-gold I on emerald reads down to 16 px; mono needs the small cut.'),
 ('work/stack_study.png','6 · Stacked lockup studies',
  'Small centred "Creations" (left) is the hotel-sign trope; the near-equal two-line block (right, chosen) reads as one name and leaves no hole under "Indra".'),
]
cells=''.join(f'''<figure style="margin:0;background:#fff;border-radius:6px;padding:14px 14px 12px;box-sizing:border-box">
<div style="font:600 17px/1.2 Helvetica,Arial,sans-serif;color:#0B2A20;margin-bottom:8px">{t}</div>
<div style="height:{h}px;display:flex;align-items:center;justify-content:center;background:#f6f1e7;overflow:hidden"><img src="{uri_file(f,'image/png')}" style="max-width:100%;max-height:{h}px"></div>
<figcaption style="font:13.5px/1.4 Helvetica,Arial,sans-serif;color:#333;margin-top:9px">{c}</figcaption></figure>'''
 for (f,t,c),h in zip(panels,[560,560,560,560,250,250]))
html=f'''<!doctype html><html><body style="margin:0;background:#8f8f8f">
<div style="padding:22px;width:1600px;box-sizing:border-box">
<div style="font:700 26px Helvetica,Arial,sans-serif;color:#fff;margin:0 0 4px">R3 · The Hinge — exploration (28 variations, 6 studies)</div>
<div style="font:15px Helvetica,Arial,sans-serif;color:#f1f1f1;margin:0 0 16px">Question: can the n of Van and the I of Indra be one stroke, and still read "VanIndra" at a glance?</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{cells}</div></div></body></html>'''
compose(html,'explore.png',1600,1800)
print('ok')
