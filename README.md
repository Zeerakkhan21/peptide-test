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
| Form | Four questions, then details | Four questions, then details |
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
  licensed providers." That claim is **not** made here. The page never says we
  supply, employ or match anyone with a clinician. The test checks the *shape*
  of that claim rather than the words, so the disclaimers can still direct
  people to an independent licensed healthcare professional — which they do,
  in the FAQ and the footer.
- **No promised outcome and no dosing guidance.** Where the copy discusses
  weight management it is hedged throughout: "may support", "for some people",
  "results and suitability vary by individual".

GLP-1 itself is described as **a naturally occurring hormone** — appetite,
digestion, blood sugar. That is physiology, and it is factual.

Two things the copy does say, deliberately, and worth knowing before you run
traffic: that certain **prescription medications** work through GLP-1-related
pathways and may form part of a clinician-directed plan, and that such
medications **may support weight loss for some people when appropriately
prescribed**. Both are accurate and hedged. Both also set an expectation that a
lead may be looking for a route to a prescription, which is not something this
business supplies — worth deciding how the follow-up handles that before the
first leads arrive.

## The popup

Opens **five seconds** after every landing — first visit, refresh, or a return
through the Back button. Dismissing it does not stop it coming back on the next
page load: nothing is stored between loads, so there is no "already seen this"
flag to go stale. Escape, the X and a click on the backdrop all close it, and
focus is trapped inside it while it is open.

It fires even when the visitor has already started the hero form. That is
deliberate and was asked for, but it does mean a dialog can land on top of a
half-answered question. The occurrence is tracked as `popup_over_form`, so you
can see in GTM how often it actually happens before deciding whether to hold it
back. To hold it back, add `|| engaged` to the guard at the top of `openPop` in
`build.py`.

The timing is in `CFG` at the top of `build.py`:

```python
"popupMs": 5000,
```

Change it there and re-run the build. The popup carries the same five-step form
as the hero card, so a visitor can convert from either.

---

## The lead form

Five steps — four questions, then contact details — matching the flow on the
main landing page. It appears twice, in the card beside the headline and in the
popup, each keeping its own answers and tagged with where the submission came
from (`hero` or `popup`) so you can see which one earns its place.

The four questions qualify the lead without touching health status, which is not
a targetable or storable attribute for advertising purposes:

1. What would you like to understand better?
2. Where are you based?
3. Where are you in the process?
4. Which language should we reply in?

Answers appear back as chips as you go, Back returns to any earlier step with
the selection intact, and the progress bar and step counter track position.
The contact step asks first name, last name (optional), email, phone and a
consent checkbox. First name, email, phone and consent are required.

**The page publishes no phone numbers** — not in the footer, not in the contact
section. The form still *collects* one, because `api/lead.js` validates the
field and returns 422 without it, so removing it would reject every lead. A
test asserts both halves of that: no published number, and the input still
there.

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
| `popup_over_form` | popup opened while the hero form was in progress |
| `form_start` | first answer given |
| `form_step` | each question answered, with the answer |
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

89 assertions: the ad-safety scan described above, the structural pieces of the
reference layout, that the brand kit is applied rather than the reference's own
colours, the popup firing between 3.6 and 5 seconds and returning on
every refresh, a full walk through all five steps including Back and the answer
chips, field and consent validation, complete submissions from both the hero
form and the popup reaching the API with the right name, language, `source` and
UTM fields, the redirect and the single conversion, the personalised thank-you
page, Spanish rendering down to the step counter, six viewports from 320px to
1920px, the mobile behaviour described below, tap target sizes and console
cleanliness.

---

## On a phone

The primary nav is hidden below 1000px, so a horizontally scrollable strip sits
under the header carrying all five section links — without it, every section
below the hero was unreachable except by scrolling. The header CTA stays visible
at every width and drops to a shorter label under 420px, where the logo, the
language toggle and a seventeen-character button cannot share one line.

Anchor targets carry `scroll-margin-top: 92px`. The header is sticky and 75px
tall, so without that reservation every in-page jump landed underneath it.

Three containers used the `padding` shorthand, which was resetting the
horizontal padding `.wrap` supplies and putting copy flush against the screen
edge — invisible on desktop, where the 1180px max-width leaves a margin anyway.
They use `padding-block` now. "GLP-1" is set `nowrap` in the headline; its
hyphen is a legal wrap point and a 320px screen was breaking it as
"Explore GLP-" / "1 Options."

Four tests cover this: the nav strip appears and scrolls, every anchor clears
the header, copy keeps its gutter at 390px, and no viewport from 320px to
1920px scrolls horizontally.

---

## The photograph

The "Built around you" panel carries a lifestyle photograph, inlined as a data
URI so the page stays self-contained.

**Confirm you hold a licence for it before this goes live.** It came from the
reference design supplied to me, and I have no way to check its provenance. If
it is stock imagery belonging to someone else, replace it: put your own file in
the repository, point the `PHOTO` line at the top of `build.py` at it, and
re-run the build. The panel crops to 5:4 and covers, so any reasonably
proportioned image works.

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
