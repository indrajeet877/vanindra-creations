import sys, os
from PIL import Image, ImageDraw, ImageFont
deck = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
titles = ["Cover", "Sound familiar?", "Why views stall", "Why views don't become business", "The fix: you record, we do the rest", "Every leak has a fix", "Proof: real accounts", "Start free", "Packages", "Team + how joining works", "After you join", "One next step"]
def sheet(src_dir, out, heading):
    TW, TH, G, LBL, TOP = 900, 506, 24, 46, 110
    W = 3 * TW + 4 * G; H = TOP + 4 * (TH + LBL) + 5 * G
    c = Image.new('RGB', (W, H), (238, 235, 227)); d = ImageDraw.Draw(c)
    fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 46)
    fl = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 26)
    d.text((W / 2, TOP / 2 + 6), heading, font=fb, fill=(10, 30, 23), anchor='mm')
    for i in range(12):
        im = Image.open(os.path.join(src_dir, '%02d.png' % (i + 1))).convert('RGB').resize((TW, TH), Image.LANCZOS)
        x = G + (i % 3) * (TW + G); y = TOP + G + (i // 3) * (TH + LBL + G)
        c.paste(im, (x, y))
        d.text((x + TW / 2, y + TH + LBL / 2 + 2), '%02d  %s' % (i + 1, titles[i]), font=fl, fill=(47, 63, 56), anchor='mm')
    c.save(out, optimize=True); print(out, c.size, os.path.getsize(out) // 1024, 'KB')
sheet(os.path.join(deck, 'slides'), os.path.join(deck, 'contact_sheet.png'), 'VanIndra Creations — Client Pitch Deck (12 slides, EN)')
sheet(os.path.join(deck, 'work', 'hi'), os.path.join(deck, 'work', 'contact_sheet_hinglish.png'), 'VanIndra Creations — Client Pitch Deck (12 slides, Hinglish)')
