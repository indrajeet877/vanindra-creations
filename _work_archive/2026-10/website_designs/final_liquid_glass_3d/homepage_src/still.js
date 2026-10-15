const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});p.on('pageerror',e=>console.log('ERR',e.message));
for(const d of ['','1']){await p.goto('file://'+__dirname+'/proto/still.html?dark='+d);await p.waitForTimeout(300);await p.screenshot({path:__dirname+'/still_'+(d?'dark':'light')+'.png',omitBackground:true});}
await b.close();})();
