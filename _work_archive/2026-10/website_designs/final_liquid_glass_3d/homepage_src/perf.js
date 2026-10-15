const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http=require('http'),fs=require('fs'),path=require('path');
const GL=['--use-angle=swiftshader','--enable-unsafe-swiftshader'];
function server(dir){return new Promise(res=>{const s=http.createServer((req,r)=>{let p=decodeURIComponent(req.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';fs.readFile(path.join(dir,p),(e,d)=>{if(e){r.writeHead(404);return r.end()}r.end(d)})}).listen(0,()=>res(s))})}
const frameStats=(f)=>{f=f.slice(1);const s=f.slice().sort((a,b)=>a-b);const sum=f.reduce((a,b)=>a+b,0);return {frames:f.length,avgFps:+(1000*f.length/sum).toFixed(1),p95:+s[Math.floor(s.length*.95)].toFixed(1),worst:+s[s.length-1].toFixed(1),over33:f.filter(x=>x>34).length,over50:f.filter(x=>x>50).length}};
(async()=>{
  const which=process.argv[2]; const FORCE=process.argv[3]==='force'; const dir=path.join(__dirname,'var',which);
  const s=await server(dir); const url='http://127.0.0.1:'+s.address().port+'/index.html';
  const out={page:which};
  // ---- mobile: 390x844, CPU x4, scroll the whole page
  { const b=await chromium.launch({args:GL}); const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:3});
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/,r=>r.abort()); const p=await ctx.newPage();
    await p.addInitScript((F)=>{sessionStorage.setItem('vi_intro','1');localStorage.setItem('vi_intro',String(Date.now()));if(F)window.__fxForceGL=true;window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(Math.round(e.duration)))).observe({type:'longtask',buffered:true});},FORCE);
    await p.goto(url,{waitUntil:'load'}); await p.waitForTimeout(3000);
    const c=await ctx.newCDPSession(p); await c.send('Emulation.setCPUThrottlingRate',{rate:4});
    await p.evaluate(()=>{window.__lt=[]});
    const r=await p.evaluate(()=>new Promise(res=>{const f=[];let last=performance.now();const H=document.documentElement.scrollHeight-innerHeight;let y=0;(function step(t){f.push(t-last);last=t;y+=24;window.scrollTo(0,y);if(y<H)requestAnimationFrame(step);else res(f)})(last)}));
    out.mobileScroll=frameStats(r); out.mobileLongTasks=await p.evaluate(()=>window.__lt);
    await c.send('Emulation.setCPUThrottlingRate',{rate:1}); await b.close(); }
  // ---- desktop 1440x900: hero fps idle + pointer, loops pause off-screen / hidden
  { const b=await chromium.launch({args:GL}); const ctx=await b.newContext({viewport:{width:1440,height:900}});
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/,r=>r.abort()); const p=await ctx.newPage();
    await p.addInitScript((F)=>{sessionStorage.setItem('vi_intro','1');localStorage.setItem('vi_intro',String(Date.now()));if(F)window.__fxForceGL=true},FORCE);
    await p.goto(url,{waitUntil:'load'}); await p.waitForTimeout(7000);
    const fps=()=>p.evaluate(()=>new Promise(res=>{const f=[];let last=performance.now();const t0=last;(function step(t){f.push(t-last);last=t;if(t-t0<3000)requestAnimationFrame(step);else res(f)})(last)}));
    out.heroIdle=frameStats(await fps());
    const mv=(async()=>{for(let i=0;i<40;i++){await p.mouse.move(400+i*16,600+Math.sin(i/4)*120);}})();
    out.heroPointer=frameStats(await fps()); await mv;
    out.halo=await p.evaluate(()=>window.FX&&FX.haloInfo?FX.haloInfo():null);
    if(!(await p.evaluate(()=>!!window.FX))){await b.close();console.log(JSON.stringify(out,null,1));s.close();return;}
    // off-screen
    await p.mouse.move(1430,890); await p.evaluate(()=>window.scrollTo(0,2600)); await p.waitForTimeout(2500);
    const a=await p.evaluate(()=>[FX.haloInfo().frames,FX.running()]); await p.waitForTimeout(2000);
    const bq=await p.evaluate(()=>[FX.haloInfo().frames,FX.running(),FX.haloInfo().visible]);
    out.offscreen={haloFramesIn2s:bq[0]-a[0],loopRunning:bq[1],haloVisible:bq[2]};
    // hidden tab (back at the hero)
    await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(1500);
    await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'))});
    await p.waitForTimeout(500); const h1=await p.evaluate(()=>[FX.haloInfo().frames,FX.running()]); await p.waitForTimeout(2000); const h2=await p.evaluate(()=>[FX.haloInfo().frames,FX.running()]);
    out.hidden={haloFramesIn2s:h2[0]-h1[0],loopRunning:h2[1]};
    await b.close(); }
  console.log(JSON.stringify(out,null,1)); s.close();
})();
