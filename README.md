# Peptides Costa Rica — GLP-1 Lead Generation Page

A GLP-1 education and lead-capture landing page. The layout follows a supplied
reference design; the colour, type and logo are the Peptides Costa Rica brand
kit.

The purpose is to test whether a broad, informational GLP-1 page converts better
and clears paid-advertising review more easily than a page that names and sells
a specific compound.

---

## Quick start

Open `index.html` in a browser. No build step, no dependencies.

To deploy on Vercel: push this repository, import it as a new project, leave
every build setting empty. `api/lead.js` becomes a serverless function at
`/api/lead` automatically.

---

## What makes this variant different

The layout follows a supplied reference design; the colour, type and logo are
the Peptides Costa Rica brand kit, so the page reads as ours rather than as the
reference.

| | Product page | This page |
| --- | --- | --- |
| Headline | A named compound | Explore GLP-1 Options |
| Primary CTA | Request Information | Get Free Guidance |
| Conversion goal | Enquiry about a product | Lead capture |
| Form | Four questions, then details | Name, email, phone |
| Prices, discounts, stock | Shown | None |
| Compound names | Named | None |
| Lead `source` | `adwords_lp` | `glp1_lp` |

Structure, top to bottom: header with nav and CTA · split hero with the lead
form beside the headline · four-item trust strip · "Understanding GLP-1" with
four explainer columns · a personalised-approach section · a four-step
how-it-works with a confidentiality card · FAQ · dark closing CTA band · footer.

### What the page deliberately does not say

Every one of these is enforced by a test in `glp1-test.js`, so a later copy edit
cannot quietly reintroduce one:

- **No compound names.** Not Retatrutide, Semaglutide, Tirzepatide, Ozempic,
  Wegovy or Zepbound.
- **No purchase language.** No cart, checkout, buy, prices, discounts, stock or
  vial counts. There is not a single `$` on the page.
- **No provider claim.** The reference design is built on "we connect you with
  licensed providers." That claim is **not** made here — there is no mention of
  licensed providers, clinicians, prescribers or consultations, and the FAQ
  states plainly that this is not medical advice and that we do not diagnose,
  treat or prescribe.
- **No promised outcome and no dosing guidance.**

GLP-1 is described throughout as **the hormone the body produces** — appetite
signalling, gastric emptying, the insulin response. That is physiology, and it
is factual. It is not a claim about any product.

## The popup

Opens **five seconds** after landing. It opens once per visit and never after a
submission. Escape, the X and a click on the backdrop all close it, and focus is
trapped inside it while it is open.

The timing is in `CFG` at the top of `build.py`:

```python
"popupMs": 5000,
```

Change it there and re-run the build. The popup carries the same three fields as
the hero card, so a visitor can convert from either.

---

## The lead form

Three fields — name, email and phone — in two places: the card beside the
headline, and the popup. Both post the same payload, tagged with where the
submission came from (`hero` or `popup`) so you can see which one earns its
place.

On submit the page POSTs eight fields to `/api/lead`, which forwards
server-side to the Lead API. The upstream host and any API key never reach the
browser. `source` is `glp1_lp`, so these leads are distinguishable from the
product page's in your CRM without any extra configuration.

A confirmed lead redirects to `/thank-you`, where the conversion fires — once,
guarded against refreshes and direct visits. See the main landing page
repository for the full explanation of that guard.

---

## Tracking

Google Tag Manager container **GTM-M2GVDQ44**, the same one as the other pages.

| Event | When |
| --- | --- |
| `page_view_lp` | page load, tagged with the variant |
| `popup_open` | popup opens, tagged with what triggered it |
| `lead_validation_error` | submit blocked by a field error |
| `lead_submit_attempt` | submit pressed |
| `lead_submit_success` | Lead API accepted, redirecting |
| `generate_lead` | **the conversion**, on the thank-you page |

Build your conversion trigger on `generate_lead`. To compare the two pages, split
on the `source` field: `glp1_lp` against `adwords_lp`.

Leave `ads.conversionId` and `ads.conversionLabel` empty in `index.html` if you
are firing the Google Ads conversion from GTM — filling both would count every
lead twice.

---

## Language

Bilingual. English is written into the markup; Spanish lives in the `ES` object
in the script block, keyed to the `data-i18n` attributes. The toggle is in the
header, `?lang=es` forces it, and the browser's language is the default.

---

## Testing

```bash
npm i -D playwright && npx playwright install chromium
node glp1-test.js
```

53 assertions: the ad-safety scan described above, the structural pieces of the
reference layout, that the brand kit is applied rather than the reference's own
colours, the popup firing between 3.6 and 5 seconds, field validation, full
submissions from both the hero form and the popup reaching the API with the
right `source` and UTM fields, the redirect and the single conversion, Spanish
rendering including form placeholders, six viewports from 320px to 1920px, tap
target sizes and console cleanliness.

---

## Editing the page

`index.html` is generated. Edit `build.py` and re-run it:

```bash
python3 build.py
```

Copy lives in two places in that file: English in the markup template, Spanish
in the `ES` dictionary keyed to the same `data-i18n` attributes. The script
scans its own output for banned terms before writing, so a copy change cannot
silently produce an unadvertisable page.

`brand.py` holds the logo lockups, favicon set, colour tokens and GTM snippets,
lifted from the main site. Update it there if the branding changes.

---

## What gets deployed

`.vercelignore` keeps the README and the test suite off the deployment:

```
index.html
thank-you.html
api/lead.js
vercel.json
favicon.ico
.gitignore
```

`build.py` and `brand.py` are ignored — the generated page ships, the generator
does not.

`api/lead.js` contains the upstream Lead API host and is deliberately **not**
ignored — Vercel compiles anything under `/api` into a serverless function and
never serves its source. Worth confirming once after the first deploy:

```bash
curl -s https://<your-deployment>.vercel.app/api/lead.js | head -5
```

JSON or a 404 is correct. JavaScript source is not.
