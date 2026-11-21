const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage();let bad=[];
for(const [h,o] of jobs){await p.goto('file://'+h);await p.waitForTimeout(250);
 const ov=await p.evaluate(()=>[...document.querySelectorAll('[data-overflow]')].map(x=>x.querySelector('h1').textContent));if(ov.length)bad.push(o+': '+ov);
 await p.pdf({path:o,width:'8.5in',height:'11in',printBackground:true});}
console.log(jobs.length,'PDFs');if(bad.length)console.log('OVERFLOW:\n'+bad.join('\n'));await b.close()})();
