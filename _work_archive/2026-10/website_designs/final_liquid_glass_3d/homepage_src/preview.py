from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/web3/final_home/'
d=Image.open(D+'shot_desktop_fold.png').convert('RGB').resize((960,600),Image.LANCZOS)
m=Image.open(D+'shot_mobile_fold.png').convert('RGB')
m=m.resize((390,844))
W,H=40+960+48+390+40, 110+844+40
bg=Image.new('RGB',(W,H),(236,234,228))
def card(im,x,y,r):
    sh=Image.new('RGBA',(im.size[0]+60,im.size[1]+60),(0,0,0,0)); dd=ImageDraw.Draw(sh)
    dd.rounded_rectangle((30,40,30+im.size[0],40+im.size[1]),r,fill=(9,36,27,70)); sh=sh.filter(ImageFilter.GaussianBlur(14))
    bg.paste(sh,(x-30,y-30),sh)
    mask=Image.new('L',im.size,0); ImageDraw.Draw(mask).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),r,fill=255)
    bg.paste(im,(x,y),mask)
card(d,40,110+122,18); card(m,40+960+48,110,34)
dr=ImageDraw.Draw(bg)
try:
    f1=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22); f2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
except Exception:
    f1=f2=ImageFont.load_default()
dr.text((40,36),'Final homepage · Liquid Glass + 3D glass orbit, magic cursor, cinematic motion',font=f1,fill=(10,30,23))
dr.text((40,70),'Desktop 1440×900 (scaled to 960) and mobile 390×844, first screen. No GPU here, so the glass shows as its pre-rendered still (the live WebGL version matches it and moves).',font=f2,fill=(86,102,95))
bg.save(D+'preview.png')
print(bg.size)
