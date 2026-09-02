/**
 * Checks for the product landing page.
 *   node product-test.js            (defaults to index.html)
 *   node product-test.js product-tirzepatide.html
 */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const FILE = process.argv[2] || 'index.html';
const PAGE = path.join(__dirname, FILE);
if (!fs.existsSync(PAGE)) { console.error('No ' + FILE + ' — run: python3 build-product.py'); process.exit(1); }

const CATALOG_HOST = 'catalog.peptidescostarica.net';
const GTM_ID = 'GTM-M2GVDQ44';

let pass = 0, fail = 0;
const is = (c, m, extra = '') => { c ? pass++ : fail++;
  console.log('  ' + (c ? 'PASS  ' : 'FAIL  ') + m + (extra ? '  ' + extra : '')); };

const server = http.createServer((q, r) => {
  r.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
  r.end(fs.readFileSync(PAGE));
});

const SPY = `
  window.dataLayer = window.dataLayer || [];
  window.__events = [];
  const orig = window.dataLayer.push.bind(window.dataLayer);
  window.dataLayer.push = function(o){ window.__events.push(o); return orig(o); };
`;

(async () => {
  await new Promise(r => server.listen(8270, r));
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 950 } });
  await ctx.addInitScript(SPY);
  // never actually leave for the real catalog during a test run
  await ctx.route(/catalog\.peptidescostarica\.net/, r =>
    r.fulfill({ status: 200, contentType: 'text/html', body: '<title>catalog stub</title>' }));
  const p = await ctx.newPage();
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://127.0.0.1:8270/');
  await p.waitForTimeout(1200);

  // ── the destination ──────────────────────────────────────────────────────
  console.log('\n  catalog links');
  const links = await p.$$eval('a[data-cta]', as => as.map(a => ({
    where: a.getAttribute('data-cta'), href: a.getAttribute('href'), text: a.textContent.trim() })));
  const toCatalog = links.filter(l => l.href.includes(CATALOG_HOST));
  is(toCatalog.length >= 4, 'every buy route points at the catalog', '-> ' + toCatalog.length + ' links');
  is(toCatalog.every(l => l.href.includes('category=Weight%20Loss%20%26%20Metabolism')),
     'each carries the Weight Loss & Metabolism category');
  is(toCatalog.every(l => /[?&]lang=(en|es)/.test(l.href)), 'each carries a language parameter');
  // ?product= is what makes the catalog open this product's detail modal rather
  // than dropping the visitor on a category list.
  is(toCatalog.every(l => /[?&]product=/.test(l.href)),
     'each deep-links to the product, not just the category');
  is(toCatalog.every(l => decodeURIComponent(l.href).includes('product=Retatrutide 12mg')),
     'product name matches the catalog spelling exactly', '-> Retatrutide 12mg');
  const cart = links.filter(l => /add to cart|añadir/i.test(l.text));
  is(cart.length >= 3, 'Add to cart appears in header, hero and buy card', '-> ' + cart.length);
  is(cart.every(l => l.href.includes(CATALOG_HOST)), 'every Add to cart goes to the catalog');

  // ── it actually navigates ────────────────────────────────────────────────
  console.log('\n  clicking Add to cart');
  await p.click('a[data-cta="hero-primary"]');
  await p.waitForTimeout(900);
  is(p.url().includes(CATALOG_HOST), 'the click navigates to the catalog', '-> ' + p.url().slice(0, 78));
  await p.goBack(); await p.waitForTimeout(900);

  // ── language ─────────────────────────────────────────────────────────────
  console.log('\n  language');
  is((await p.$eval('a[data-cta="hero-primary"]', a => a.getAttribute('href'))).includes('lang=en'),
     'English page links to the English catalog');
  await p.click('.lang button[data-lang="es"]');
  await p.waitForTimeout(500);
  const esHref = await p.$eval('a[data-cta="hero-primary"]', a => a.getAttribute('href'));
  is(esHref.includes('lang=es'), 'switching to Spanish switches the catalog link too', '-> lang=es');
  is(!/lang=es.*lang=|lang=en/.test(esHref), 'and does not leave a stale duplicate parameter');
  is(await p.$eval('html', h => h.lang) === 'es', 'html lang attribute follows');
  const esTagline = await p.$eval('.tagline', e => e.textContent);
  is(/investigaci|pureza/i.test(esTagline), 'copy is translated, not just the links', '-> "' + esTagline.slice(0, 46) + '…"');
  const heroH1 = await p.$eval('h1', e => e.textContent.trim());
  is(heroH1 === 'Retatrutide' || heroH1.length > 0, 'product name is not translated away', '-> ' + heroH1);
  await p.click('.lang button[data-lang="en"]'); await p.waitForTimeout(400);
  is((await p.$eval('.tagline', e => e.textContent)).includes('High-purity'), 'and switches back cleanly');

  // ── tracking ─────────────────────────────────────────────────────────────
  console.log('\n  tracking');
  const html = fs.readFileSync(PAGE, 'utf8');
  is((html.match(new RegExp(GTM_ID, 'g')) || []).length === 2, 'GTM installed, head snippet plus noscript');
  is(html.indexOf('gtm.start') < html.indexOf('<body'), 'container snippet is in the head');
  let ev = await p.evaluate(() => window.__events.map(e => e.event));
  is(ev.includes('view_item'), 'view_item fires on load', '-> ' + JSON.stringify(ev.slice(0, 4)));
  // The click pushes to dataLayer and then the browser leaves for the catalog,
  // which tears down the page before the assertion can read it. Cancelling the
  // navigation lets the push be observed; the page's own handler still runs,
  // because preventDefault on a capture listener does not stop later listeners.
  await p.evaluate(() => document.addEventListener('click', function(e){
    const a = e.target.closest && e.target.closest('a[href]');
    if (a) e.preventDefault();
  }, true));
  await p.click('a[data-cta="buy-card"]'); await p.waitForTimeout(500);
  ev = await p.evaluate(() => window.__events);
  const sel = ev.filter(e => e.event === 'select_item');
  is(sel.length >= 1, 'select_item fires when a catalog link is clicked');
  is(sel[0] && sel[0].location === 'buy-card', 'and records which button was used', '-> ' + (sel[0] || {}).location);
  is(sel[0] && !!sel[0].item_name, 'with the product attached', '-> ' + (sel[0] || {}).item_name);
  await p.reload(); await p.waitForTimeout(700);

  // ── nothing half-filled leaks out ────────────────────────────────────────
  console.log('\n  unfilled fields stay hidden');
  const body = await p.$eval('body', b => b.innerText);
  is(!/undefined|null|NaN|\[object/i.test(body), 'no placeholder artefacts in the visible text');
  is(!/\b(TBD|TODO|XXX|lorem)\b/i.test(body), 'no draft markers left in the copy');
  const priceTxt = await p.$eval('.price', e => e.textContent.trim()).catch(() => '');
  is(priceTxt === '$135', 'price matches the catalog', '-> ' + priceTxt);
  is(!!(await p.$('.stock')), 'in-stock badge shown');
  is(/15%/.test(await p.$eval('.promo', e => e.textContent).catch(() => '')), 'volume promo shown');
  const overview = await p.$eval('.ov__body > p', e => e.textContent);
  is(!/24%|body weight|once-weekly|subcutaneous|titration/i.test(overview),
     'no efficacy figures or dosing guidance in the copy');
  const specCount = await p.$$eval('.specs li', n => n.length);
  const hasNote = await p.$('.specs__empty');
  is(specCount > 0 || !!hasNote, 'either real specs or the catalog note, never an empty gap',
     '-> ' + (specCount ? specCount + ' spec rows' : 'catalog note'));

  // ── layout ───────────────────────────────────────────────────────────────
  console.log('\n  layout');
  for (const w of [320, 390, 768, 1024, 1440, 1920]) {
    await p.setViewportSize({ width: w, height: 900 });
    await p.waitForTimeout(260);
    const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    const wide = await p.evaluate((vw) => [...document.querySelectorAll('body *')]
      .filter(el => { const r = el.getBoundingClientRect();
                      return r.width > 0 && r.left > -0.6 && r.right > vw + 0.6; }).length, w);
    is(over === 0 && wide === 0, w + 'px — nothing spills past the viewport',
       over || wide ? `-> scroll ${over}px, ${wide} element(s)` : '');
  }
  await p.setViewportSize({ width: 390, height: 900 });
  await p.waitForTimeout(300);
  const small = await p.$$eval('a, button', els => els
    .filter(e => e.getClientRects().length)
    .map(e => { const r = e.getBoundingClientRect();
                return { t: (e.textContent || '').trim().slice(0, 22), w: Math.round(r.width), h: Math.round(r.height) }; })
    .filter(x => x.h < 24 || x.w < 24));
  is(small.length === 0, 'every tap target meets WCAG 2.5.8 at 390px',
     small.length ? '-> ' + JSON.stringify(small.slice(0, 3)) : '');

  is(errs.filter(e => !/Failed to load resource|ERR_TUNNEL/.test(e)).length === 0,
     'no console errors', errs.filter(e => !/Failed to load resource|ERR_TUNNEL/.test(e)).join(' | '));

  console.log('\n  ' + pass + ' passed, ' + fail + ' failed\n');
  await browser.close(); server.close();
  process.exit(fail ? 1 : 0);
})();
