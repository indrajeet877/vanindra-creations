"""reel_tag.png, header.png, global.png compositions (HTML -> Playwright)."""
import sys, base64, subprocess, os
sys.path.insert(0,'.')
from build import *
S_='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
def uri_svg(svgtext): return 'data:image/svg+xml;base64,'+base64.b64encode(svgtext.encode()).decode()
def uri_file(path, mime): return f'data:{mime};base64,'+base64.b64encode(open(path,'rb').read()).decode()
def label(text, size, color, weight=500, tracking=0.0):
    t=vt.text_path(text, family='manrope', weight=weight, size=size, tracking=tracking)
    b=t.bounds; w=b[2]-b[0]
    y0=-size*0.74; h=size*1.0    # fixed em box (cap 0.74 + descender 0.26): every label scales identically
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+2:.1f}" height="{h:.1f}" viewBox="{b[0]-1:.1f} {y0:.1f} {w+2:.1f} {h:.1f}" overflow="visible"><path d="{t.d}" fill="{color}"/></svg>'
def compose(html, out, w, h):
    open('work/_tmp.html','w').write(html)
    subprocess.run(['node','compose.js','work/_tmp.html',out,str(w),str(h)],check=True)

# ---------------- REEL TAG
reel='/home/user/vanindra-creations/assets/portfolio/reel_DZSZW2ey529.jpg'
wm_em=wordmark_svg(WMS, EM, GD, pad=0)
wm_iv=wordmark_svg(WMS, IV, GL, pad=0)
def reel_html(pos='tl', ink='em'):
    wm = wm_em if ink=='em' else wm_iv
    col = EM if ink=='em' else IV
    lab = label('Edit by', 30, col, 600, 0.02)
    place = {'tl':'left:28px;top:98px','bl':'left:28px;bottom:136px','tr':'right:28px;top:98px'}[pos]
    return f'''<!doctype html><html><body style="margin:0;width:540px;height:960px;overflow:hidden;background:#000">
<img src="{uri_file(reel,'image/jpeg')}" style="position:absolute;left:0;top:0;width:540px;height:960px;object-fit:cover">
<div style="position:absolute;{place};display:flex;flex-direction:column;align-items:flex-start;gap:4px">
  <img src="{uri_svg(lab)}" style="height:9.5px;display:block;margin-left:2px">
  <img src="{uri_svg(wm)}" style="height:24px;display:block">
</div></body></html>'''
compose(reel_html('tl','em'),'reel_tag.png',540,960)

# ---------------- HEADER
nav = [label(t, 30, EM, 500) for t in ['Work','Services','Pricing','About']]
cta = label('Book a free call', 30, IV, 600)
navhtml=''.join(f'<img src="{uri_svg(n)}" style="height:13.5px">' for n in nav)
burger='<svg width="22" height="14" viewBox="0 0 22 14"><rect y="1" width="22" height="1.6" fill="#0B2A20"/><rect y="11" width="14" height="1.6" fill="#0B2A20" x="8"/></svg>'
cap1=label('Desktop header 1440 × 120 · wordmark (small cut) at 36 px tall', 26, '#5b5b55', 500)
cap2=label('Phone header 390 × 64 · wordmark (small cut) at 26 px tall', 26, '#5b5b55', 500)
hdr=f'''<!doctype html><html><body style="margin:0;width:1440px;height:330px;background:#E7E4DC;font-family:sans-serif">
<div style="position:absolute;left:0;top:0;width:1440px;height:120px;background:{IV};display:flex;align-items:center;justify-content:space-between;padding:0 64px;box-sizing:border-box;border-bottom:1px solid #e3dccd">
  <img src="{uri_svg(wordmark_svg(WMS, EM, EM, pad=0))}" style="height:36px;display:block">
  <div style="display:flex;align-items:center;gap:40px">{navhtml}
    <div style="background:{EM};border-radius:999px;padding:13px 22px;display:flex"><img src="{uri_svg(cta)}" style="height:13.5px"></div></div>
</div>
<img src="{uri_svg(cap1)}" style="position:absolute;left:64px;top:136px;height:12px">
<div style="position:absolute;left:64px;top:170px;width:390px;height:64px;background:{IV};display:flex;align-items:center;justify-content:space-between;padding:0 18px;box-sizing:border-box;border-radius:10px 10px 0 0;box-shadow:0 0 0 1px #d8d1c2">
  <img src="{uri_svg(wordmark_svg(WMS, EM, EM, pad=0))}" style="height:26px;display:block">{burger}
</div>
<div style="position:absolute;left:64px;top:234px;width:390px;height:66px;background:#fff;box-shadow:0 0 0 1px #d8d1c2;border-radius:0 0 10px 10px"></div>
<img src="{uri_svg(cap2)}" style="position:absolute;left:480px;top:196px;height:12px">
<div style="position:absolute;left:880px;top:170px;width:496px;height:64px;background:{EM};display:flex;align-items:center;padding:0 18px;box-sizing:border-box;border-radius:10px">
  <img src="{uri_svg(wordmark_svg(WMS, IV, GL, pad=0))}" style="height:26px;display:block"></div>
</body></html>'''
compose(hdr,'header.png',1440,330)

# ---------------- GLOBAL
subprocess.run(['node','../toolkit/render.js','png','global.svg','global.png','1600'],check=True)
print('extras done')
