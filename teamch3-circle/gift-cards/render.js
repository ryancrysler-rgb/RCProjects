const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.cwd()+'/gift-card-template.html');await p.waitForTimeout(700);
await p.pdf({path:process.argv[2]||'gift-card.pdf',width:'8.5in',height:'11in',printBackground:true});
const o=await p.evaluate(()=>{const i=document.querySelector('.in');return i.scrollHeight-i.clientHeight});console.log('overflow',o);await b.close()})();
