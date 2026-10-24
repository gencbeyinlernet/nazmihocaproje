const fs = require('fs'), http = require('http'), path = require('path');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const root = path.join(__dirname, '..');
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/nazmihocaproje\//, '/');
  let file = path.join(root, pathname);
  if (!file.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
  try {
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    res.setHeader('Content-Type', ({ '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg' })[path.extname(file)] || 'text/plain');
    res.end(fs.readFileSync(file));
  } catch { res.writeHead(404); res.end(); }
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}/nazmihocaproje/`;
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, args: ['--no-sandbox'] });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'no-preference' });
    const p = await context.newPage(), errors = [], missing = [];
    p.on('pageerror', e => errors.push(e.message));
    p.on('response', r => { if (r.status() >= 400) missing.push(r.url()); });
    await p.clock.install();
    const current = () => p.locator('[data-slide-count]').innerText();
    await p.goto(base);
    await p.clock.runFor(15000);
    assert.equal(await current(), '1 / 3', 'No automatic movement before consent');
    await p.check('#terms-check'); await p.click('#terms-accept');
    await p.clock.runFor(7100); assert.equal(await current(), '2 / 3');
    const left = await p.locator('#class-sidebar').boundingBox(), rail = await p.locator('#discovery-rail').boundingBox(), center = await p.locator('.topic-carousel').boundingBox();
    assert(left.x + left.width <= center.x && center.x + center.width <= rail.x);
    assert.equal(rail.x + rail.width, 1440);
    assert.equal(await p.locator('#discovery-rail').evaluate(e => e.firstElementChild.className), 'question-invite');
    await p.click('[data-slide-prev]'); assert.equal(await current(), '1 / 3');
    await p.clock.runFor(15000); assert.equal(await current(), '1 / 3', 'Manual browsing stops automatic movement');
    await p.click('[data-slide-to="2"]'); assert.equal(await current(), '3 / 3');
    await p.click('[data-slide-next]'); assert.equal(await current(), '1 / 3');
    await p.keyboard.press('ArrowLeft'); assert.equal(await current(), '3 / 3');
    await p.click('[data-slide-to="0"]');
    await p.click('[data-slide-auto]'); await p.mouse.move(0, 0);
    await p.clock.runFor(7100); assert.equal(await current(), '2 / 3');
    await p.locator('.topic-carousel').hover(); await p.clock.runFor(15000); assert.equal(await current(), '2 / 3');
    await p.mouse.move(0, 0); await p.clock.runFor(7100); assert.equal(await current(), '3 / 3');
    await p.click('#open-question-area');
    assert(await p.locator('#question-dialog').isVisible()); assert(await p.locator('#ask-form').isVisible());
    assert(await p.locator('#ask-form [type=submit]').isDisabled());
    await p.clock.runFor(15000); assert.equal(await current(), '3 / 3', 'Modal pauses the slideshow');
    await p.keyboard.press('Escape');
    await p.waitForFunction(() => document.activeElement.id === 'open-question-area');
    await p.clock.runFor(7100); assert.equal(await current(), '1 / 3');
    await p.emulateMedia({ reducedMotion: 'reduce' });
    await p.waitForFunction(() => document.querySelector('.topic-carousel').dataset.autoplay === 'false');
    await p.clock.runFor(15000); assert.equal(await current(), '1 / 3');
    assert.equal(await p.locator('.topic-carousel').getAttribute('data-autoplay'), 'false');
    await p.goto(base + 'siniflar/5-sinif/');
    assert.equal(await p.locator('.spotlight-slide').count(), 3);
    assert.equal(await p.locator('.topic-carousel [aria-current=true]').count(), 1);
    await p.click('[data-slide-to="1"]');
    assert((await p.locator('.spotlight-slide:not([hidden]) .primary-start').getAttribute('href')).endsWith('#icerik=birligin-anlami'));
    await p.locator('.spotlight-slide:not([hidden]) .primary-start').click();
    assert(await p.locator('#start-story').isVisible());
    await p.goto(base + 'siniflar/6-sinif/');
    assert.equal(await p.locator('.spotlight-slide').count(), 2);
    await p.locator('.spotlight-slide:not([hidden]) .primary-start').click(); assert(await p.locator('#learning-dialog').isVisible());
    await p.goto(base + 'siniflar/7-sinif/'); assert.equal(await p.locator('.topic-carousel').count(), 0);
    await p.goto(base + 'siniflar/9-sinif/');
    assert((await p.locator('.spotlight-badge').first().innerText()).startsWith('9. sınıf'));
    assert.equal(await p.locator('.spotlight-slide img').count(), 0, 'No unrelated grade-five images on high school topics');
    await p.fill('#topic-search', await p.locator('.spotlight-slide h3').first().innerText());
    assert.equal(await p.locator('.spotlight-slide').count(), 1);
    assert.equal(await p.locator('.spotlight-controls').count(), 0, 'Single slide has no needless controls');
    await p.goto(base + 'universite/');
    await p.locator('.spotlight-slide:not([hidden]) [data-university]').click();
    assert(await p.locator('.academic-reading').isVisible());
    await p.setViewportSize({ width: 390, height: 844 }); await p.goto(base);
    assert(await p.locator('#class-nav-trigger').isVisible());
    assert(!await p.locator('.quick-menu').evaluate(e => e.open));
    await p.locator('.quick-menu > summary').click(); assert(await p.locator('.quick-menu nav').isVisible());
    const track = p.locator('.spotlight-track');
    await track.dispatchEvent('pointerdown', { pointerId: 1, pointerType: 'touch', isPrimary: true, clientX: 290, clientY: 400 });
    await track.dispatchEvent('pointerup', { pointerId: 1, pointerType: 'touch', isPrimary: true, clientX: 100, clientY: 410 });
    assert.equal(await current(), '2 / 3');
    await p.click('[data-slide-next]'); assert.equal(await current(), '3 / 3', 'Buttons keep working after a swipe');
    await p.click('#open-question-area');
    for (let i = 0; i < 20; i++) { await p.keyboard.press('Tab'); assert(await p.evaluate(() => !!document.activeElement.closest('#question-dialog'))); }
    await p.click('#close-question-area');
    for (const width of [320, 390, 768, 1100, 1280, 1440]) {
      await p.setViewportSize({ width, height: 900 });
      for (const route of ['', 'ortaokul/', 'lise/', 'universite/', 'siniflar/5-sinif/', 'siniflar/9-sinif/', 'sahne-atolyesi/', 'metin-atolyesi/', 'indir/']) {
        await p.goto(base + route);
        assert(!await p.evaluate(() => document.documentElement.scrollWidth > innerWidth), `Overflow ${width} ${route}`);
        assert(await p.locator('.question-invite .button').isVisible());
      }
    }
    assert.deepEqual(errors, []); assert.deepEqual(missing, []);
    console.log('PASS: left/center/right layout, top-right question dialog and focus, contextual slides, 7-second autoplay, manual arrows/dots/keyboard/swipe, pause on hover/modal/consent/reduced motion, single/empty slide cases, and 6 responsive widths.');
  } finally { await browser.close(); server.close(); }
})().catch(e => { console.error(e); server.close(); process.exit(1); });
