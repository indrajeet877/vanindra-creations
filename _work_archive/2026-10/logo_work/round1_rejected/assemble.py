"""Assemble the logo review page from symbols.json and the template."""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYMS = json.load(open(os.path.join(HERE, 'symbols.json')))
OUT = sys.argv[1]


def data_uri(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def use(key, cls='', w=None, h=None, label=None):
    s = SYMS[key]
    size = f' width="{w}" height="{h}"' if w else ''
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 {s["w"]} {s["h"]}"{size}{aria}><use href="#{key}"/></svg>'


DIRS = [
    {
        'k': 'A', 'name': 'Maison',
        'idea': 'A Bodoni capital V inside a slim arch. The arch is a 9:16 Reel frame and the doorway of an Indian palace; the gold diamond above the V completes "Vi". The wordmark is set in Bodoni, with CREATIONS spaced out between two gold rules.',
        'dp': 'A_icon_small', 'dp_ground': 'on-emerald',
        'good': ['Has a story the team can tell in one sentence: the frame we create in, and the doorway clients walk through.',
                 'Bodoni is the typeface of fashion and luxury publishing, so it signals premium pricing instantly.',
                 'Gold appears only as a small diamond and two rules, which is elegant without any 3D effects.'],
        'watch': ['The fine hairlines need the dedicated small version for anything under 48 px (shown in the size test).',
                  'Needs clear space around the arch; don\'t squeeze it into tight corners.'],
    },
    {
        'k': 'B', 'name': 'Editorial',
        'idea': 'VanIndra set in Cormorant Garamond with Creations in gold italic, like a magazine masthead. The seal carries a single serif V inside a double ring.',
        'dp': 'B_icon_small', 'dp_ground': 'on-ivory',
        'good': ['The most readable of the three at every size, from a pitch-deck cover to a 16 px tab icon.',
                 'Mixed case keeps the brand spelling VanIndra exactly as written everywhere else.',
                 'Warm and graceful, which suits family, lifestyle and festive creators.'],
        'watch': ['A V inside a circle is a familiar shape, so the icon alone is less ownable than A.',
                  'The italic Creations is best kept in gold or a lighter tone, never in a second loud colour.'],
    },
    {
        'k': 'C', 'name': 'Frame',
        'idea': 'A Didone V set inside a rounded 9:16 frame, the shape of a phone screen. The wordmark is geometric Jost with wide letter-spacing.',
        'dp': 'C_icon_small', 'dp_ground': 'on-emerald',
        'good': ['Says "short-form video studio" before anyone reads a word.',
                 'Makes a strong app icon and favicon; the frame survives any size.',
                 'Modern and international, which fits B2B and global (USD) clients.'],
        'watch': ['Cooler and more corporate than A or B, with less warmth for family and lifestyle creators.',
                  'Rounded phone frames are common in tech; the Didone V carries most of the personality.'],
    },
]


def section(d, reel_uri):
    k = d['k']
    sizes = ''.join(use(f'{k}_icon_small', w=px, h=px, label=f'{px} pixel icon') for px in (16, 24, 32, 48))
    good = ''.join(f'<li>{x}</li>' for x in d['good'])
    watch = ''.join(f'<li>{x}</li>' for x in d['watch'])
    return f'''
  <section class="dir" aria-labelledby="dir-{k}">
    <div class="dir-head"><span class="dir-letter">{k}</span><h2 id="dir-{k}">{d['name']}</h2><p>{d['idea']}</p></div>
    <div class="grounds">
      <div class="ground on-ivory">{use(f'{k}_horizontal', 'lockup', label=f'Direction {k} horizontal logo on ivory')}</div>
      <div class="ground on-emerald">{use(f'{k}_horizontal', 'lockup', label=f'Direction {k} horizontal logo on emerald')}</div>
    </div>
    <div class="uses">
      <div class="use"><span class="cap">Website header</span>
        <div class="site-bar on-emerald">{use(f'{k}_horizontal', label='Logo in the website header')}<div class="navs"><span></span><span></span><span></span><span class="cta"></span></div></div>
      </div>
      <div class="use"><span class="cap">Instagram profile</span>
        <div class="ig"><div class="dp {d['dp_ground']}">{use(d['dp'], label='Instagram profile picture')}</div><div class="meta"><b>vanindracreations</b><span>Content studio · Reels &amp; strategy</span></div></div>
      </div>
      <div class="use"><span class="cap">Browser tab &amp; size test</span>
        <div class="tab on-ivory">{use(f'{k}_icon_small', w=16, h=16, label='Browser tab icon')}<span>VanIndra Creations</span></div>
        <div class="sizes on-ivory" style="padding:10px;border-radius:3px;">{sizes}</div>
      </div>
      <div class="use"><span class="cap">Reel watermark</span>
        <div class="reel"><img src="{reel_uri}" alt="Reel cover from @vandanay2012 with the watermark in the corner" loading="lazy"><div class="wm">{use(f'{k}_icon_small', 'i')}<b>VANINDRA</b></div></div>
      </div>
    </div>
    <div class="stackrow">
      <div class="ground on-ivory">{use(f'{k}_stacked', 'stack', label=f'Direction {k} stacked logo on ivory')}</div>
      <div class="ground on-emerald">{use(f'{k}_stacked', 'stack', label=f'Direction {k} stacked logo on emerald')}</div>
    </div>
    <div class="facts"><div><h3>Why it works</h3><ul>{good}</ul></div><div><h3>Watch-outs</h3><ul>{watch}</ul></div></div>
  </section>'''


tpl = open(os.path.join(HERE, 'review_template.html')).read()
symbols = ''.join(f'<symbol id="{k}" viewBox="0 0 {v["w"]} {v["h"]}">{v["body"]}</symbol>' for k, v in SYMS.items())
reel = data_uri(os.path.join(HERE, 'reel_small.jpg'))
crest = data_uri(os.path.join(HERE, 'crest_small.jpg'))
html = tpl.replace('{{SYMBOLS}}', symbols).replace('{{CREST}}', crest)
html = html.replace('{{DIRECTIONS}}', ''.join(section(d, reel) for d in DIRS))


def macro(m):
    key, px, ground = m.group(1), m.group(2), m.group(3)
    return f'<span class="on-{ground}" style="display:inline-block;line-height:0;vertical-align:middle;border-radius:3px;">{use(key, w=px, h=px)}</span>'


html = re.sub(r'\[\[([A-Za-z_]+):(\d+):(\w+)\]\]', macro, html)
open(OUT, 'w').write(html)
print(len(html) // 1024, 'KB')
