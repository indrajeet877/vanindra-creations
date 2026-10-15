import base64, re, sys, os
W='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/web3'
H=W+'/final_home/_work/'
src=open(W+'/base_liquid_glass/index.html').read()
def once(s, old, new):
    assert s.count(old)==1, ('anchor count', old[:60], s.count(old))
    return s.replace(old,new)
css=open(H+'fx.css').read()
def b64(n): return 'data:image/webp;base64,'+base64.b64encode(open(H+'still_%s.webp'%n,'rb').read()).decode()
boot=open(H+'boot.html').read().strip()
intro=open(H+'intro.html').read().strip()
lenis=open(W+'/vendor/lenis.min.js').read().replace('//# sourceMappingURL=lenis.min.js.map','').strip()
glass=open(H+'glass.js').read().strip()
fx=open(H+'fx.js').read().strip()
# the dark stills sit in a small style block at the end of <body> (Dark Studio Mode needs JS anyway), off the render-blocking head CSS
dark='<style id="fx-stills">.gl3d-back::before{background-image:url("%s")}.gl3d::before{background-image:url("%s")}'%(b64('back_light'),b64('front_light'))+'body.dark-studio .gl3d-back::before{background-image:url("%s")}body.dark-studio .gl3d::before{background-image:url("%s")}</style>'%(b64('back_dark'),b64('front_dark'))
s=src
s=once(s,"<script>document.documentElement.classList.add('js')</script>","<script>document.documentElement.classList.add('js')</script>\n"+boot)
s=once(s,"</style>\n</head>","</style>\n<style id=\"fx-css\">\n"+css+"\n</style>\n</head>")
s=once(s,"<body>\n","<body>\n"+intro+"\n")
s=once(s,'<div class="phone-wrap rv" id="iphone3D" style="--d:.08s">\n        <div class="phone" id="phoneBody">','<div class="phone-wrap rv" id="iphone3D" style="--d:.08s">\n        <div class="gl3d-back" aria-hidden="true"></div>\n        <div class="gl3d" aria-hidden="true"><canvas></canvas></div>\n        <div class="phone" id="phoneBody">')
tail=dark+"\n<script>/* Lenis 1.1 smooth scroll · MIT License · darkroom.engineering */\n"+lenis+"\n</script>\n<script>\n"+glass+"\n"+fx+"\n</script>\n</body>"
s=once(s,"</body>",tail)
assert not re.search(r'guggy|sahil|indrajeet',s,re.I)
open(W+'/final_home/index.html','w').write(s)
js=sum(len(m) for m in re.findall(r'<script[^>]*>([\s\S]*?)</script>',s))
print('index.html', len(s.encode()), 'bytes; inline JS', js, 'bytes')
