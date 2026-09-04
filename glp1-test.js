/**
 * Checks for the GLP-1 guidance landing page.
 *   node glp1-test.js
 *
 * Three things matter here: the page is safe to put behind paid advertising,
 * the popup fires on time, and both forms actually deliver a lead.
 */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const DIR = __dirname;

let pass = 0, fail = 0;
const is = (c, m, extra = '') => { c ? pass++ : fail++;
  console.log('  ' + (c ? 'PASS  ' : 'FAIL  ') + m + (extra ? '  ' + extra : '')); };

let posted = [];
const server = http.createServer((q, r) => {
  const u = q.url.split('?')[0];
  if (u === '/api/lead') {
    let b = ''; q.on('data', c => b += c);
    return q.on('end', () => { try { posted.push(JSON.parse(b)); } catch (e) {}
      r.writeHead(200, {'Content-Type':'application/json'}); r.end('{"ok":true}'); });
  }
  const f = u === '/' ? 'index.html' : (u === '/thank-you' ? 'thank-you.html' : u.slice(1));
  const p = path.join(DIR, f);
  if (fs.existsSync(p) && fs.statSync(p).isFile()) {
    r.writeHead(200, {'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});
    return r.end(fs.readFileSync(p));
  }
  r.writeHead(404); r.end('nf');
});

const SPY = `
  window.dataLayer = window.dataLayer || [];
  window.__events = [];
  const orig = window.dataLayer.push.bind(window.dataLayer);
  window.dataLayer.push = function(o){ window.__events.push(o); return orig(o); };
`;

(async () => {
  await new Promise(r => server.listen(8290, r));
  const browser = await chromium.launch();
  const base = 'http://127.0.0.1:8290';
  const html = fs.readFileSync(path.join(DIR, 'index.html'), 'utf8');
  const visible = html.slice(html.indexOf('<body>'));

  // ── what must not appear ─────────────────────────────────────────────────
  console.log('\n  ad-safety scan');
  const banned = {
    'compound names': /\b(Retatrutide|Semaglutide|Tirzepatide|Ozempic|Wegovy|Zepbound|Liraglutide|Mounjaro|Saxenda)\b/i,
    'purchase language': /\b(add to cart|buy now|checkout|order now|shop now)\b/i,
    'prices': /\$\s?\d/,
    'discounts': /\b\d+%\s*(off|discount)\b/i,
    'stock or vials': /\b(vials?|in stock|out of stock)\b/i,
    // The claim shape, not the phrase. Disclaimers that point people TO an
    // independent professional are wanted; claiming we supply one is not.
    'provider claim': /\b(?:we|our)\s+(?:connect|match|pair|work with|partner with|have)\b[^.]{0,50}\b(?:licensed|provider|clinician|physician|prescriber)|our\s+(?:licensed\s+)?(?:providers|clinicians|doctors|physicians|prescribers)|\b(?:matched|connected)\s+(?:you\s+)?with\s+a\b|\bwe\s+prescribe\b/i,
    'guaranteed outcome': /\b(guaranteed|you will lose|proven to (cure|treat)|clinically proven)\b/i,
    'dosing guidance': /\b(mg per week|once-weekly|titration|inject)\b/i,
  };
  for (const [label, re] of Object.entries(banned)) {
    const m = visible.match(re);
    is(!m, 'no ' + label, m ? '-> found "' + m[0] + '"' : '');
  }
  is(/(informational purposes|educational information) only/i.test(visible),
     'educational-information disclaimer present');
  is(/licensed healthcare professional/i.test(visible),
     'directs people to an independent healthcare professional');
  is(/does not provide medical advice/i.test(visible), 'states it is not medical advice');

  // No phone numbers anywhere in the copy. The form still *collects* one —
  // api/lead.js rejects a payload without it — but the page publishes none.
  const numbers = visible.replace(/<script[\s\S]*?<\/script>/gi, '')
                         .match(/\+\d[\d ()\-.]{7,}|\btel:/gi);
  is(!numbers, 'no phone number published in the copy',
     numbers ? '-> found "' + numbers[0].trim() + '"' : '');

  const ctx = await browser.newContext({ viewport: { width: 1440, height: 950 } });
  await ctx.addInitScript(SPY);
  const p = await ctx.newPage();
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  // ── the design ───────────────────────────────────────────────────────────
  console.log('\n  design and positioning');
  await p.goto(base + '/');
  await p.waitForTimeout(900);
  const h1 = (await p.$eval('h1', e => e.textContent)).replace(/\s+/g, ' ').trim();
  is(/GLP-1/i.test(h1), 'headline leads on GLP-1', '-> "' + h1 + '"');
  // Three lines is the deliberate setting for this copy: holding it to two
  // would mean dropping the type below the presence the layout needs. What
  // matters is that it does not run away.
  const h1Lines = await p.$eval('h1', e =>
    Math.round(e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight)));
  is(h1Lines <= 3, 'headline stays within three lines at 1440px', '-> ' + h1Lines + ' lines');
  is(await p.$eval('.card', e => e.getBoundingClientRect().top < 700),
     'lead form is above the fold, beside the headline');
  is((await p.$$('.tr')).length === 4, 'four-item trust strip');
  is((await p.$$('.gi')).length === 4, 'four-column GLP-1 explainer');
  is((await p.$$('.step')).length === 4, 'four-step how-it-works');
  is((await p.$$('.q')).length >= 4, 'FAQ present', '-> ' + (await p.$$('.q')).length + ' questions');
  is(!!(await p.$('.band')), 'dark closing CTA band present');
  is(await p.$eval('.built__art img', e => e.naturalWidth > 0), 'the lifestyle photograph loads');
  is(await p.$eval('.built__art img', e => e.getAttribute('src').startsWith('data:image/')),
     'photograph is inlined, no external file');
  // the reference's columns must not collapse into unreadable slivers
  const giW = await p.$$eval('.gi', ns => ns.map(n => Math.round(n.getBoundingClientRect().width)));
  is(Math.min(...giW) >= 150, 'explainer columns are wide enough to read', '-> ' + giW.join(', ') + 'px');

  // brand kit, not the reference's
  console.log('\n  brand kit');
  const cta = await p.$eval('.hdr .btn', e => getComputedStyle(e).backgroundImage);
  is(/200, 82, 7|168, 63, 6|143, 54, 4/.test(cta), 'CTAs use the brand orange', '-> ' + cta.slice(0, 54) + '…');
  is(await p.$eval('body', e => /Poppins/.test(getComputedStyle(e).fontFamily)), 'Poppins throughout');
  is(await p.$eval('.brand__logo', e => e.getAttribute('src').startsWith('data:image/png')),
     'brand logo is inlined, no external file');
  is(await p.$eval('h1 em', e => getComputedStyle(e).color) === 'rgb(21, 115, 214)',
     'GLP-1 is highlighted in the brand blue, not the reference teal');

  // ── popup at five seconds ────────────────────────────────────────────────
  console.log('\n  popup timing');
  is(!(await p.$eval('#ov', e => e.classList.contains('open'))), 'closed at 0.9s');
  await p.waitForTimeout(2700);
  is(!(await p.$eval('#ov', e => e.classList.contains('open'))), 'still closed at 3.6s');
  await p.waitForSelector('#ov.open', { timeout: 4000 });
  is(true, 'opens by 5s');
  const ev = await p.evaluate(() => window.__events);
  is(ev.some(e => e.event === 'popup_open'), 'popup open is tracked');
  // the honeypot is also an input; count only the fields a person sees
  is((await p.$$('#popwiz .pane')).length === 5, 'popup carries the same five-step form');
  await p.click('#ovX'); await p.waitForTimeout(400);
  is(!(await p.$eval('#ov', e => e.classList.contains('open'))), 'closes on the X');

  // It must come back on every landing, including a refresh after a dismissal.
  // Nothing is stored between page loads, so there is no "seen it" flag to go
  // stale — but that is exactly the kind of thing a later edit reintroduces.
  for (const landing of ['refresh after dismissing it', 'a second refresh']) {
    await p.reload();
    await p.waitForSelector('#ov.open', { timeout: 6500 }).catch(() => {});
    is(await p.$eval('#ov', e => e.classList.contains('open')),
       'popup returns on ' + landing);
    await p.click('#ovX'); await p.waitForTimeout(350);
  }
  // and it fires even if the visitor has started the hero form
  await p.reload(); await p.waitForTimeout(500);
  await p.click('.opt[data-val="GLP-1 and appetite"]');
  await p.waitForSelector('#ov.open', { timeout: 6500 }).catch(() => {});
  is(await p.$eval('#ov', e => e.classList.contains('open')),
     'popup fires even with the hero form in progress');
  await p.click('#ovX'); await p.waitForTimeout(350);

  // ── walking the questions ────────────────────────────────────────────────
  // The hero walk takes longer than five seconds, so the popup now lands on top
  // of it partway through — which is the requested behaviour, not a fault. Auto
  // dismiss it so the walk can carry on testing the hero form underneath.
  const autoClosePopup = () => p.evaluate(() => {
    if (window.__popCloser) return;
    window.__popCloser = new MutationObserver(() => {
      const ov = document.getElementById('ov');
      if (ov && ov.classList.contains('open')) document.getElementById('ovX').click();
    });
    window.__popCloser.observe(document.getElementById('ov'), { attributes: true });
  });
  const stopAutoClose = () => p.evaluate(() => {
    if (window.__popCloser) { window.__popCloser.disconnect(); window.__popCloser = null; }
  });

  console.log('\n  the five-step form');
  await p.goto(base + '/');
  await p.waitForTimeout(800);
  await p.reload();
  await p.waitForTimeout(800);
  await autoClosePopup();
  is(await p.$eval('#step', e => /1 of 5/.test(e.textContent)), 'opens on step 1 of 5');
  is(await p.$eval('#back', e => e.hidden), 'no Back button on the first step');

  await p.click('.opt[data-val="GLP-1 and weight management"]');
  await p.waitForTimeout(420);
  is(await p.$eval('#step', e => /2 of 5/.test(e.textContent)), 'answering advances a step');
  is((await p.$$eval('#chips .chip', ns => ns.map(n => n.textContent))).length === 1,
     'the answer is shown back as a chip');
  is(!(await p.$eval('#back', e => e.hidden)), 'Back appears from step 2');
  const w2 = await p.$eval('#bar', e => e.style.width);
  is(w2 === '40%', 'progress bar tracks the step', '-> ' + w2);

  await p.click('#back'); await p.waitForTimeout(300);
  is(await p.$eval('#step', e => /1 of 5/.test(e.textContent)), 'Back returns to the previous step');
  is(await p.$eval('.opt[data-val="GLP-1 and weight management"]', e => e.classList.contains('sel')),
     'and the earlier answer is still selected');

  await p.click('.opt[data-val="GLP-1 and weight management"]'); await p.waitForTimeout(400);
  await p.click('.opt[data-val="United States"]');               await p.waitForTimeout(400);
  await p.click('.opt[data-val="Just starting to look into it"]'); await p.waitForTimeout(400);
  await p.click('.opt[data-val="English"]');                     await p.waitForTimeout(450);
  is(await p.$eval('#step', e => /5 of 5/.test(e.textContent)), 'four answers reach the contact step');
  is((await p.$$('#chips .chip')).length === 4, 'all four answers are chipped');
  for (const id of ['#fname', '#lname', '#email', '#phone', '#consent']) {
    is(!!(await p.$(id)), 'contact step has ' + id.slice(1));
  }
  // The optional messaging-number field was removed on request. The required
  // Phone Number stays, because api/lead.js 422s a payload without one.
  is(!(await p.$('#alt')), 'the optional messaging-number field is gone');

  // ── validation ───────────────────────────────────────────────────────────
  console.log('\n  validation');
  await p.click('#btn'); await p.waitForTimeout(300);
  is(await p.$eval('#fname', e => e.getAttribute('aria-invalid')) === 'true', 'empty first name is rejected');
  is(posted.length === 0, 'nothing posted on an invalid submit');
  await p.fill('#fname', 'Zeerak');
  await p.fill('#email', 'not-an-email');
  await p.fill('#phone', '123');
  await p.click('#btn'); await p.waitForTimeout(300);
  is(await p.$eval('#email', e => e.getAttribute('aria-invalid')) === 'true', 'bad email is rejected');
  is(await p.$eval('#phone', e => e.getAttribute('aria-invalid')) === 'true', 'short phone is rejected');
  await p.fill('#email', 'zeerak.test@example.com');
  await p.fill('#phone', '+1 831 471 5559');
  await p.click('#btn'); await p.waitForTimeout(300);
  is(!(await p.$eval('#consent-e', e => e.hidden)), 'unticked consent blocks the submit');
  is(posted.length === 0, 'still nothing posted');

  // ── the happy path ───────────────────────────────────────────────────────
  console.log('\n  lead capture');
  await p.fill('#lname', 'Khan');
  await p.check('#consent');
  await p.click('#btn');
  await p.waitForURL(/thank-you/, { timeout: 8000 }).catch(() => {});
  await p.waitForTimeout(800);
  is(posted.length === 1, 'exactly one lead posted', '-> ' + posted.length);
  const lead = posted[0] || {};
  is(lead.name === 'Zeerak Khan', 'first and last name are joined', '-> ' + lead.name);
  is(!!lead.email && !!lead.phone, 'email and phone reached the API');
  is(lead.language === 'en', 'the language answer sets the payload language', '-> ' + lead.language);
  is(lead.source === 'glp1_lp', 'tagged as the GLP-1 variant', '-> ' + lead.source);
  is('utm_source' in lead && 'utm_campaign' in lead, 'UTM fields included for attribution');
  is(/thank-you/.test(p.url()), 'redirects to the thank-you page', '-> ' + new URL(p.url()).pathname);
  const dl = await p.evaluate(() => (window.dataLayer || []).map(e => e && e.event).filter(Boolean));
  is(dl.filter(e => e === 'generate_lead').length === 1, 'conversion fires exactly once', '-> ' + dl.filter(e => e === 'generate_lead').length);
  const recap = await p.$eval('body', b => b.innerText);
  is(/Zeerak/.test(recap), 'thank-you page greets them by name');
  is(/weight management/i.test(recap), 'and recaps what they asked about');

  // ── the popup form delivers too ──────────────────────────────────────────
  console.log('\n  popup form');
  posted = [];
  const ctx2 = await browser.newContext({ viewport: { width: 1440, height: 950 } });
  await ctx2.addInitScript(SPY);
  const p2 = await ctx2.newPage();
  await p2.goto(base + '/?utm_source=google&utm_campaign=glp1-test');
  await p2.waitForSelector('#ov.open', { timeout: 9000 });
  await p2.click('#popwiz .opt[data-val="GLP-1 and appetite"]');   await p2.waitForTimeout(400);
  await p2.click('#popwiz .opt[data-val="Costa Rica"]');           await p2.waitForTimeout(400);
  await p2.click('#popwiz .opt[data-val="Not sure yet"]');         await p2.waitForTimeout(400);
  await p2.click('#popwiz .opt[data-val="Espa\u00f1ol"]');            await p2.waitForTimeout(450);
  await p2.fill('#popfname', 'Ana');
  await p2.fill('#poplname', 'Rodríguez');
  await p2.fill('#popemail', 'ana@example.com');
  await p2.fill('#popphone', '+506 8404 6973');
  await p2.check('#popconsent');
  await p2.click('#popbtn');
  await p2.waitForURL(/thank-you/, { timeout: 8000 }).catch(() => {});
  await p2.waitForTimeout(700);
  is(posted.length === 1, 'popup form posts a lead too', '-> ' + posted.length);
  is((posted[0] || {}).utm_campaign === 'glp1-test', 'campaign attribution carried through',
     '-> ' + (posted[0] || {}).utm_campaign);
  is((posted[0] || {}).language === 'es', 'the Spanish answer sets the payload language',
     '-> ' + (posted[0] || {}).language);
  await ctx2.close();

  // ── Spanish ──────────────────────────────────────────────────────────────
  console.log('\n  Spanish');
  await p.goto(base + '/?lang=es');
  await p.waitForTimeout(800);
  await autoClosePopup();
  const esH1 = (await p.$eval('h1', e => e.textContent)).replace(/\s+/g, ' ').trim();
  is(/GLP-1/.test(esH1), 'still leads on GLP-1', '-> "' + esH1 + '"');
  is(/[áéíóúñ¿]/i.test(await p.$eval('.hero__sub', e => e.textContent)), 'body copy is translated');
  is(await p.$eval('.pane__q', e => /[¿áéíóú]/i.test(e.textContent)), 'the first question is translated',
     '-> ' + await p.$eval('.pane__q', e => e.textContent));
  is(await p.$eval('#step', e => /Paso/.test(e.textContent)), 'the step counter is translated',
     '-> ' + await p.$eval('#step', e => e.textContent));

  // ── layout ───────────────────────────────────────────────────────────────
  console.log('\n  layout');
  await p.goto(base + '/');
  await autoClosePopup();
  for (const w of [320, 390, 768, 1024, 1440, 1920]) {
    await p.setViewportSize({ width: w, height: 900 });
    await p.waitForTimeout(240);
    const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    is(over === 0, w + 'px — no horizontal overflow', over ? '-> ' + over + 'px' : '');
  }
  // Every section must be reachable on a phone. The primary nav is hidden
  // below 1000px, so a scrollable strip takes over — and it has to actually
  // scroll, or the last links are unreachable.
  await p.setViewportSize({ width: 390, height: 844 });
  await p.waitForTimeout(280);
  const nav = await p.evaluate(() => {
    const primary = document.querySelector('.nav');
    const strip = document.querySelector('.navwrap');
    const inner = strip && strip.querySelector('.navwrap__in');
    return {
      primaryHidden: primary ? getComputedStyle(primary).display === 'none' : true,
      stripShown: !!strip && getComputedStyle(strip).display !== 'none',
      links: inner ? inner.querySelectorAll('a').length : 0,
      scrolls: inner ? inner.scrollWidth > inner.clientWidth + 1 : false,
      cta: !!document.querySelector('.hdr [data-cta="header"]')
    };
  });
  is(nav.primaryHidden && nav.stripShown, 'the mobile nav strip replaces the primary nav');
  is(nav.links === 5, 'all five sections are in the strip', '-> ' + nav.links);
  is(nav.scrolls, 'the strip scrolls horizontally rather than clipping');
  is(nav.cta, 'the header CTA is present at 390px');

  // A sticky header hides whatever an anchor jumps to unless the target
  // reserves room for it.
  const anchors = await p.evaluate(() => {
    const h = Math.round(document.querySelector('.hdr').getBoundingClientRect().height);
    return ['how', 'about', 'expect', 'faq', 'contact', 'lead'].map(id => {
      const n = document.getElementById(id);
      return { id, ok: n && parseFloat(getComputedStyle(n).scrollMarginTop) >= h };
    });
  });
  is(anchors.every(a => a.ok), 'every anchor clears the sticky header',
     '-> ' + anchors.filter(a => !a.ok).map(a => '#' + a.id).join(' '));

  // Content must not sit against the screen edge.
  const gutter = await p.$$eval('.hero h1, .hero .eyebrow-pill, .sec .h2',
    ns => Math.min(...ns.map(n => Math.round(n.getBoundingClientRect().left))));
  is(gutter >= 14, 'copy keeps a gutter from the screen edge at 390px', '-> ' + gutter + 'px');

  await p.waitForTimeout(120);
  // honeypots are deliberately invisible and are not tap targets
  const small = await p.$$eval('a, button, input', els => els
    .filter(e => e.getClientRects().length && e.getAttribute('aria-hidden') !== 'true')
    .map(e => ({ t: (e.textContent || e.placeholder || '').trim().slice(0, 20),
                 h: Math.round(e.getBoundingClientRect().height) }))
    .filter(x => x.h < 24));
  is(small.length === 0, 'every control meets WCAG 2.5.8 at 390px',
     small.length ? '-> ' + JSON.stringify(small.slice(0, 3)) : '');

  is(errs.filter(e => !/Failed to load resource|ERR_TUNNEL/.test(e)).length === 0, 'no console errors',
     errs.filter(e => !/Failed to load resource|ERR_TUNNEL/.test(e)).join(' | '));

  console.log('\n  ' + pass + ' passed, ' + fail + ' failed\n');
  await browser.close(); server.close();
  process.exit(fail ? 1 : 0);
})();
