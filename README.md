# Peptides Costa Rica — Product Pages

A standalone, self-contained product landing page for Retatrutide 12mg. Every
call to action sends the visitor to the product in the live catalog.

The page carries no external image or CSS files: the logo lockups and the whole
favicon set are base64 data URIs inside the HTML. Deploying is a matter of
uploading two files.

This repository is independent of the main lead-generation landing page. It
shares the brand kit, but nothing else.

---

## Quick start

Open `index.html` in a browser. Nothing to install, no server needed.

To deploy on Vercel: push this repository, import it as a new project, and leave
every build setting empty. There is no build step. The page is live at the
project root within a minute.

Netlify, Cloudflare Pages, S3 and plain shared hosting all work the same way —
point them at the repository root with no build command.

---

## Where the buttons go

All four purchase routes — the header button, the hero button, the buy card and
the sticky bar on mobile — go to:

```
https://catalog.peptidescostarica.net/catalog
    ?category=Weight%20Loss%20%26%20Metabolism
    &lang=en
    &product=Retatrutide%2012mg
```

`product` is the parameter that matters. The catalog reads it and opens that
product's own detail modal, matching on the product name (case-insensitive) or
its id — so a click lands the visitor on the real product card with the
catalog's ADD TO CART button in front of them, rather than on a category list
they have to search through.

`productName` in the config must match the catalog's spelling exactly:
`Retatrutide 12mg`, not `Retatrutide 12MG`.

`lang` is rewritten to follow the language toggle, so an English reader is not
dropped onto the Spanish catalog.

### Why the button cannot fill the cart itself

The catalog's cart is held in the application's own state, keyed to a visitor id
the catalog issues. Nothing served from another domain can write to it, and the
catalog exposes no URL that adds an item — the only parameters it reads are
`product`, `lang` and `token`. "Click here, arrive with the vial already in your
cart" is therefore not achievable from outside the catalog as it stands.

Opening the product modal is the closest behaviour available today, and it
leaves exactly one click between the visitor and the cart.

Making the full version work is a small change on the catalog side: have it read
something like `?add=Retatrutide%2012mg&qty=1`, add that item and open the cart
drawer. Once that exists, put the URL in `catalog.addToCartUrl` in
`build-product.py`, re-run the generator, and every button switches over.

---

## Editing the page

Everything lives in the `PRODUCT` block at the top of `build-product.py`:

```python
PRODUCT = {
    "slug": "retatrutide",
    "output": "index.html",
    "name": "Retatrutide",
    "dose": "12mg",
    "catalog": { "base": ..., "category": ..., "productName": ..., "addToCartUrl": "" },
    "price": "$135",
    "promo": {...}, "inStock": True,
    "tagline": {...}, "blurb": {...}, "overview": {...},
    "specs": [...],
}
```

Then:

```bash
python3 build-product.py
```

That rewrites `index.html`. Nothing else needs touching.

### Fields left empty

Any value may be left as `""`. An empty spec row is omitted rather than rendered
blank, and with no specs at all the page shows a short note pointing to the
catalog instead of an empty table. An empty `price` shows "Current pricing is
shown in our catalog." Nothing half-filled ever reaches a visitor.

Open the page with `?audit=1` to see a banner listing what is still empty. The
same list is printed by `build-product.py` on every run and logged to the
browser console.

**Currently outstanding:** purity, appearance, molecular formula, molecular
weight, CAS number, storage, reconstitution. All from the COA.

### Adding a second product

Copy `build-product.py`, change `PRODUCT` — including `output`, e.g.
`product-tirzepatide.html` — and run it. `vercel.json` sets `cleanUrls`, so that
file is served at `/product-tirzepatide`.

The vial illustration is drawn in SVG from `name` and `dose`, so it re-labels
itself per product with no image to commission. A long product name is pinned to
the label width rather than spilling over it.

---

## The brand kit

`brand.py` holds the logo lockups, the favicon set, the colour tokens and the
Google Tag Manager snippets, all as plain strings. They were lifted from the
main landing page so this repository does not depend on it.

If the branding changes on the main site, update `brand.py` and re-run the
generator.

---

## Tracking

Google Tag Manager container **GTM-M2GVDQ44** is installed: the snippet high in
the `<head>` and the `<noscript>` iframe immediately after `<body>`.

The page pushes two events to `dataLayer`:

| Event | When | Carries |
| --- | --- | --- |
| `view_item` | page load | `item_name`, `item_variant`, `language` |
| `select_item` | any click through to the catalog | the above plus `location` |

`location` is which button was used: `header`, `hero-primary`, `buy-card` or
`sticky-bar`. Build your GTM trigger on `select_item` — that is the commercial
intent signal this page exists to produce.

A click also fires `cta_click` for the non-catalog buttons, and
`language_change` when the toggle is used.

---

## What was left out of the product copy

The catalog entry carries a trial-efficacy figure ("patients losing up to 24% of
body weight at 48 weeks") and a dosing protocol ("once-weekly subcutaneous
approach with gradual titration"). Neither is on this page, deliberately.

If this page runs behind Google Ads, both put the account at risk: a weight-loss
efficacy claim for an unapproved compound, and human dosing instructions for a
product the same page describes as not for human consumption. The second also
contradicts the research-use-only positioning the rest of the site rests on.

What is kept is the pharmacology and development status — triple-receptor
agonist, GLP-1/GIP/glucagon, under development for obesity and type 2 diabetes —
which is factual and carries none of that exposure. `product-test.js` asserts
those phrases stay out.

To include them anyway, put them in `PRODUCT["overview"]` and remove that
assertion.

---

## Testing

```bash
npm i -D playwright && npx playwright install chromium
node product-test.js
```

36 assertions covering the catalog destinations and the exact product spelling,
the language-linked `lang` parameter, GTM and the dataLayer events, that no
unfilled field leaks into the page, six viewports from 320px to 1920px, and tap
target sizes.

---

## What goes in git, and what gets deployed

Commit everything. `.vercelignore` keeps the generator, the brand kit, the test
suite and this README out of the deployment, leaving four files served:

```
index.html
vercel.json
favicon.ico
.gitignore
```

`favicon.ico` is there only for older browsers that probe the root path
directly; nothing in the page references it.
