// One Dot context renderer (same layout as toolkit render.js context, but separate files per ground)
// node ctx.js out.png avatar_large.svg avatar_small.svg favicon.svg header_on_emerald.svg header_on_ivory.svg
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const uri = (f) => 'data:image/svg+xml;base64,' + Buffer.from(fs.readFileSync(f, 'utf8')).toString('base64');
(async () => {
  const [out, big, smallf, fav, hE, hI] = process.argv.slice(2);
  const html = `<div style="padding:20px;display:grid;gap:20px;font:14px sans-serif">
      <div style="display:flex;gap:20px;align-items:center;background:#fff;padding:16px;border-radius:8px">
        <div style="width:150px;height:150px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #fff,0 0 0 5px #d62976"><img src="${uri(big)}" style="width:100%;height:100%"></div>
        <div style="width:110px;height:110px;border-radius:50%;overflow:hidden"><img src="${uri(big)}" style="width:100%;height:100%"></div>
        <div style="width:56px;height:56px;border-radius:50%;overflow:hidden"><img src="${uri(smallf)}" style="width:100%;height:100%"></div>
        <div style="width:32px;height:32px;border-radius:50%;overflow:hidden"><img src="${uri(smallf)}" style="width:100%;height:100%"></div>
        <div style="display:flex;align-items:center;gap:8px;background:#f1f3f4;padding:8px 12px;border-radius:8px 8px 0 0"><img src="${uri(fav)}" width="16" height="16"><span>VanIndra Creations</span></div>
      </div>
      <div style="background:#0B2A20;padding:14px 24px;display:flex;align-items:center;justify-content:space-between"><img src="${uri(hE)}" style="height:52px"><span style="color:#F6F1E7;opacity:.6">Portfolio · Services · Packages</span></div>
      <div style="background:#F6F1E7;padding:14px 24px;display:flex;align-items:center;justify-content:space-between"><img src="${uri(hI)}" style="height:52px"><span style="color:#0B2A20;opacity:.6">Portfolio · Services · Packages</span></div>
    </div>`;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 400 }, deviceScaleFactor: 1 });
  await p.setContent(`<!doctype html><html><body style="margin:0;background:#8f8f8f">${html}</body></html>`, { waitUntil: 'load' });
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
