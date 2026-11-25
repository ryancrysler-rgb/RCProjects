const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}}); const p = await b.newPage();
  await p.setViewportSize({width:816,height:1056});
  await p.goto('file://' + process.argv[2], {waitUntil:'networkidle'}); await p.waitForTimeout(800);
  await p.pdf({ path: process.argv[3], width:'8.5in', height:'11in', printBackground:true });
  if (process.argv[4]) await p.screenshot({path:process.argv[4], fullPage:true});
  await b.close(); })();
