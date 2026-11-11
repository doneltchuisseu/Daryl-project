const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = '/home/user/Daryl-project/livrables/creatives/';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    await p.goto('file://' + dir + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: dir + f.replace('.html', '.png') });
    console.log('png', f.replace('.html', '.png'));
  }
  await b.close();
})();
