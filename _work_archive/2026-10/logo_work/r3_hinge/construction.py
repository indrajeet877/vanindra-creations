import sys; sys.path.insert(0,'.')
from build import *
from extras import compose, uri_svg
from glyphkit import rect
p=pd
np_,ip_,hw=g_hinge(p)
# locate shared stem
x0=22+p.fe; xl=x0+p.S+p.cw; xr=xl+p.S
s=0.62; ox=380; base=760
def Y(v): return base - v*s
def Xx(v): return ox + v*s
lines=[(0,'baseline 0'),(p.X,'x-height 490'),(p.C,'cap height 700 (V)'),(p.A,'ascender 724 (d)'),(p.Itop,'rising I 784')]
body=''
for v,t in lines:
    body+=f'<line x1="40" x2="1160" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#c9bfa9" stroke-width="1" stroke-dasharray="{"0" if v in (0,p.X) else "5 5"}"/>'
    dy = 14 if v==p.C else -6
    body+=f'<text x="40" y="{Y(v)+dy:.1f}" text-anchor="start" font-family="Helvetica,Arial" font-size="13" fill="#7a705c">{t}</text>'
body+=f'<path d="{D_(np_,s,ox,base)}" fill="{EM}"/><path d="{D_(ip_,s,ox,base)}" fill="{GD}"/>'
# full I stem ghost (passes through the n's leg)
body+=f'<rect x="{Xx(xl):.1f}" y="{Y(p.Itop):.1f}" width="{(xr-xl)*s:.1f}" height="{p.Itop*s:.1f}" fill="none" stroke="{GD}" stroke-width="1.6" stroke-dasharray="6 4"/>'
# annotations
def note(x,y,tx,ty,text,anchor='start'):
    return (f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="#0B2A20" stroke-width="1"/><circle cx="{x}" cy="{y}" r="3" fill="#0B2A20"/>'
            f'<text x="{tx+(6 if anchor=="start" else -6)}" y="{ty+4}" text-anchor="{anchor}" font-family="Helvetica,Arial" font-size="15" fill="#0B2A20">{text}</text>')
body+=note(Xx(xl)+20, Y(p.Itop-120), 830, Y(p.Itop-60), 'I of Indra rises behind: the sky')
body+=note(Xx(x0)+30, Y(p.X*0.4), 300, Y(p.X*0.4)-40, 'n of Van in front: the forest','end')
body+=note(Xx(xl)+8, Y(p.X*0.97)+2, 830, Y(p.X*0.82), 'cut follows the shoulder (16 u / 46 u small)')
body+=note(Xx((xl+xr)/2), Y(p.X*0.25), 830, Y(p.X*0.25), 'one stroke: leg of n = stem of I')
svgtxt=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="820" viewBox="0 0 1200 820"><rect width="1200" height="820" fill="{IV}"/>{body}'+ \
       f'<text x="40" y="52" font-family="Helvetica,Arial" font-size="22" font-weight="700" fill="{EM}">The Hinge: construction</text>' + \
       f'<text x="40" y="78" font-family="Helvetica,Arial" font-size="14" fill="#5a5345">Drawn type: stems 82 (lc) / 90 (caps), hairline 24, arch top 29, bracketed slab serifs, wedge heads. Units: 1000-unit grid.</text></svg>'
open('work/construction.svg','w').write(svgtxt)
compose(f'<!doctype html><html><body style="margin:0"><img src="{uri_svg(svgtxt)}"></body></html>','construction.png',1200,820)
print('ok')
