// shoot.mjs — screenshot every iteration at desktop + phone × light + dark.
// Uses the live site's Playwright install and the machine's Chrome, so this
// folder stays dependency-free. Run from the repo root:
//   node sites/_playground/design-iterations/shoot.mjs [01-cursor ...]
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(here, '../../astro-starlight-terminal1/package.json');
const { chromium } = createRequire(site)('@playwright/test');

const only = process.argv.slice(2);
const files = fs
  .readdirSync(here)
  .filter((f) => /^\d\d-.*\.html$/.test(f))
  .filter((f) => only.length === 0 || only.some((o) => f.startsWith(o)));
fs.mkdirSync(path.join(here, 'shots'), { recursive: true });

const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--no-sandbox'] });
for (const f of files) {
  const name = f.replace(/\.html$/, '');
  const url = 'file://' + path.join(here, f);
  for (const scheme of ['dark', 'light']) {
    for (const [w, h] of [[1440, 900], [400, 860]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(here, 'shots', `${name}-${w}-${scheme}.png`), fullPage: true });
      if (w === 1440) await page.screenshot({ path: path.join(here, 'shots', `${name}-${w}-${scheme}-hero.png`) });
      await ctx.close();
    }
  }
  console.log('shot', name);
}
await browser.close();
