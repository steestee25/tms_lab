const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const f of process.argv.slice(2)){const p=await b.newPage({deviceScaleFactor:3,viewport:{width:900,height:500}});
await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(300);
const s=await p.evaluate(()=>({w:document.body.offsetWidth,h:document.body.offsetHeight}));
await p.setViewportSize({width:s.w,height:s.h});await p.screenshot({path:f.replace('.html','.png')});console.log(f,s);}
await b.close();})();
