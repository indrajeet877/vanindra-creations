"""construction.png: how the staircase, the shared slab, the knife cut and the Devanagari join are built."""
import sys
sys.path.insert(0, '.')
from build import *
from extras import compose, uri_svg
from deva import g_na, g_i_matra, headline, danda

LINE = '#c9bfa9'


def svg_panel(w, h, inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'


def P_(path, s, ox, base, col):
    return f'<path d="{rnd(to_svg_d(path, s, ox, base))}" fill="{col}"/>'


def guide(y, x0, x1, label, dash=True, right=False):
    tx = x1 - 4 if right else x0
    anchor = 'end' if right else 'start'
    return (f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}" stroke-width="1" {"stroke-dasharray=\'5 5\'" if dash else ""}/>'
            f'<text x="{tx}" y="{y-5:.1f}" text-anchor="{anchor}" font-family="Helvetica,Arial" font-size="12" fill="#8a7f68">{label}</text>')


def note(x, y, tx, ty, text, anchor='start'):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#0B2A20" stroke-width="1"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#0B2A20"/>'
            f'<text x="{tx + (6 if anchor == "start" else -6):.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">{text}</text>')


# ---------------- panel A: the staircase
s = 0.235; ox = 60; base1 = 250          # line-1 baseline in px
st = ST; L = st['L']
base2 = base1 + L * s
Y = lambda v, b=base1: b - v * s
Xx = lambda v: ox + v * s
xl, xr = st['stem']
a = ''
a += guide(Y(pd.C), 40, 760, 'cap 700', right=True)
a += guide(Y(pd.X), 40, 760, 'x-height 490', right=True)
a += guide(Y(0), 40, 760, 'line 1 baseline', dash=False, right=True)
a += guide(Y(pd.X, base2), 40, 760, '', right=True)
a += guide(Y(0, base2), 40, 760, 'line 2 baseline', dash=False, right=False)
a += P_(st['van'], s, ox, base1, EM) + P_(st['I'], s, ox, base1, GD) + P_(st['indra'], s, ox, base1, EM)
cxs = Xx((xl + xr) / 2)
a += note(cxs, Y(pd.X * 0.4), 640, Y(pd.X * 0.25), 'the n of Van: its right leg keeps going down…')
a += note(cxs, Y(-L * 0.55), 300, Y(-L * 0.55), '…and becomes the I of Indra (gold)', 'end')
a += note(Xx(xl - pd.ie), Y(pd.it / 2), 300, Y(-L * 0.2), 'one slab, two serifs: the n\'s foot + the I\'s head', 'end')

a += '<text x="40" y="30" font-family="Helvetica,Arial" font-size="13" fill="#5b5b55">Nothing hides: both letters stay whole, so the name reads at 21 px cap height. Line spacing = ascender 724 − slab 21 = 703, so the I is exactly ascender-tall.</text>'
panelA = svg_panel(1000, 450, a)

# ---------------- panel B: the Devanagari join (to be verified)
d = DV_P
sb = 0.27; ob = 40; bb = 290
na, na_end, xd_na = g_na(d, 200)
im = g_i_matra(d, 0, xd_na - 6)
hl_ = headline(d, -20, na_end + 20)
b = ''
b += P_(U(na, hl_), sb, ob, bb, EM) + P_(im, sb, ob, bb, GD)
b += note(ob + 40 * sb, bb - (d.HB + d.hl + d.rise * 0.6) * sb, 270, 60, 'ि  i-sign: stem + arch', 'start')
b += note(ob + (xd_na + 40) * sb, bb - d.HB * 0.3 * sb, 270, 230, 'न  n', 'start')
b += ('<text x="20" y="400" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">Hindi writes the same join as one sign, नि ("ni"):</text>'
      '<text x="20" y="420" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">the i-sign is a stem whose arch rides over the n.</text>'
      '<text x="20" y="440" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">Both arches are drawn with the same pen.</text>'
      '<text x="20" y="468" font-family="Helvetica,Arial" font-size="12" fill="#a14b2a">Devanagari: to be verified by the team before any use.</text>')
panelB = svg_panel(500, 490, b)

# ---------------- panel C: the knife cut
pk = P(**DISPLAY)
glyphs = [g_a(pk), g_r(pk), g_s(pk), g_t(pk), g_C(pk), g_e(pk)]
c = ''; x = 0; sc = 0.15; base = 140
for g, adv in glyphs:
    c += P_(g, sc, 20 + x * sc, base, EM); x += adv + 40
c += ('<text x="20" y="200" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">Every free stroke end is the same straight knife cut, rising about 20°.</text>'
      '<text x="20" y="220" font-family="Helvetica,Arial" font-size="14" fill="#0B2A20">No ball terminals, no beaks; the Devanagari ends the same way.</text>')
panelC = svg_panel(500, 300, c)

# ---------------- panel D: optical cuts
dd = ''
for i, (p_, lab) in enumerate([(pd, 'display cut — artwork ≥ 64 px tall: hairline 24, stem 82'),
                               (ps, 'small cut — headers, Reel credit, avatar: hairline 34, stem 90')]):
    stx = staircase(p_)
    dd += P_(stx['van'], 0.085, 20, 80 + i * 150, EM) + P_(stx['I'], 0.085, 20, 80 + i * 150, GD) + P_(stx['indra'], 0.085, 20, 80 + i * 150, EM)
    dd += f'<text x="290" y="{70 + i * 150}" font-family="Helvetica,Arial" font-size="13" fill="#0B2A20">{lab}</text>'
panelD = svg_panel(1000, 300, dd)

html = f'''<!doctype html><html><body style="margin:0;background:{IV};width:1600px">
<div style="padding:28px 36px 10px;font:700 24px Helvetica,Arial;color:{EM}">The Hinge: construction</div>
<div style="padding:0 36px 14px;font:15px Helvetica,Arial;color:#3a3a35">One stroke, two letters: the n that ends Van is the I that begins Indra. Two lines, nothing hidden, so it reads at every size.</div>
<div style="display:flex;gap:20px;padding:0 36px">
  <div style="background:#fff;border-radius:8px;padding:8px"><img src="{uri_svg(panelA)}"></div>
  <div style="background:#fff;border-radius:8px;padding:8px"><img src="{uri_svg(panelB)}"></div>
</div>
<div style="display:flex;gap:20px;padding:20px 36px 30px">
  <div style="background:#fff;border-radius:8px;padding:8px"><img src="{uri_svg(panelD)}"></div>
  <div style="background:#fff;border-radius:8px;padding:8px"><img src="{uri_svg(panelC)}"></div>
</div></body></html>'''
compose(html, 'construction.png', 1600, 1000)
print('construction ok')
