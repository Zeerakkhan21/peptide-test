#!/usr/bin/env python3
"""
Generates the product page.

    python3 build-product.py

Edit the PRODUCT block below and re-run. The brand kit — logo lockups, favicons,
colour tokens and the Google Tag Manager snippets — comes from brand.py, so a
product page carries no external image or CSS files at all.

To add a second product, copy this file, change PRODUCT (including "output"),
and run it. Each page is fully self-contained.
"""
import json
from brand import ICONS, LOGO, LOGO_LIGHT, TOKENS, GTM_HEAD, GTM_BODY

# ============================================================================
#  PRODUCT  —  the only block you edit
#  Leave a value as "" and the page simply omits that row. Nothing half-filled
#  is ever shown to a visitor. Open the page with ?audit=1 to list what is
#  still missing.
# ============================================================================
PRODUCT = {
    "slug": "retatrutide",
    # The deployment serves this at the domain root. Name a second product
    # something like "product-tirzepatide.html" and it is served at that path.
    "output": "index.html",
    "name": "Retatrutide",
    "dose": "12mg",

    # ── where the buttons go ──────────────────────────────────────────────
    # The catalog reads ?product= and opens that product's detail modal, matching
    # on the product name (case-insensitive) or its id. So a click lands the
    # visitor on the real product card with the catalog's own ADD TO CART button
    # in front of them, rather than on a category list they have to search.
    #
    # productName must match the catalog's spelling exactly — "Retatrutide 12mg",
    # not "Retatrutide 12MG".
    #
    # The catalog has no URL that adds to the cart directly: the cart lives in
    # the app's own state, keyed to a visitor id it sets itself, so nothing on
    # another domain can write to it. If your catalog developer adds such a URL,
    # put it in addToCartUrl and every button switches to it automatically.
    "catalog": {
        "base": "https://catalog.peptidescostarica.net/catalog",
        "category": "Weight Loss & Metabolism",
        "productName": "Retatrutide 12mg",
        "addToCartUrl": "",
    },

    "coaUrl": "",                     # empty hides the COA button

    "price": "$135",
    "unit":     {"en": "1 Vial",      "es": "1 Vial"},
    "promo":    {"en": "Buy 5+ vials, get 15% off",
                 "es": "Compra 5+ viales y obtén 15% de descuento"},
    "inStock": True,

    "tagline":  {"en": "High-purity peptide for advanced research applications.",
                 "es": "Péptido de alta pureza para aplicaciones avanzadas de investigación."},
    "blurb":    {"en": "Each batch is manufactured and tested to ensure consistent quality, purity and reliability.",
                 "es": "Cada lote se fabrica y analiza para garantizar una calidad, pureza y fiabilidad constantes."},

    # Mechanism and development status, taken from the catalog entry. The
    # catalog's trial-efficacy figure and its dosing protocol are deliberately
    # left out — see the note in the README.
    "overview": {"en": "Retatrutide is an investigational triple-receptor agonist peptide, targeting the GLP-1, GIP and glucagon receptors. It is under development for obesity and type 2 diabetes and is studied widely in research settings. This vial is supplied strictly for laboratory research use.",
                 "es": "La retatrutida es un péptido agonista triple en investigación, dirigido a los receptores GLP-1, GIP y glucagón. Se encuentra en desarrollo para la obesidad y la diabetes tipo 2 y se estudia ampliamente en entornos de investigación. Este vial se suministra exclusivamente para uso en investigación de laboratorio."},

    # value "" → the row is hidden. Fill these from your COA.
    "specs": [
        {"key": "purity",   "label": {"en": "Purity",            "es": "Pureza"},              "value": ""},
        {"key": "form",     "label": {"en": "Appearance",        "es": "Apariencia"},          "value": ""},
        {"key": "formula",  "label": {"en": "Molecular formula", "es": "Fórmula molecular"},   "value": ""},
        {"key": "weight",   "label": {"en": "Molecular weight",  "es": "Peso molecular"},      "value": ""},
        {"key": "cas",      "label": {"en": "CAS number",        "es": "Número CAS"},          "value": ""},
        {"key": "storage",  "label": {"en": "Storage",           "es": "Conservación"},        "value": ""},
        {"key": "reconst",  "label": {"en": "Reconstitution",    "es": "Reconstitución"},      "value": ""},
    ],
}

import urllib.parse as _u
def catalog_url(lang="es"):
    c = PRODUCT["catalog"]
    if c.get("addToCartUrl"):
        return c["addToCartUrl"]
    q = {"category": c["category"], "lang": lang}
    if c.get("productName"):
        q["product"] = c["productName"]
    return c["base"] + "?" + _u.urlencode(q, quote_via=_u.quote)

PRODUCT["catalogUrl"] = catalog_url("es")

# ============================================================================

VIAL = '''<svg class="vial" viewBox="0 0 210 400" role="img" aria-label="__ALT__" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"    stop-color="#fff"    stop-opacity=".36"/>
      <stop offset=".14"  stop-color="#fff"    stop-opacity=".08"/>
      <stop offset=".48"  stop-color="#9CC9F0" stop-opacity=".13"/>
      <stop offset=".88"  stop-color="#fff"    stop-opacity=".05"/>
      <stop offset="1"    stop-color="#fff"    stop-opacity=".30"/>
    </linearGradient>
    <linearGradient id="cap" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#07264C"/>
      <stop offset=".2"  stop-color="#1573D6"/>
      <stop offset=".54" stop-color="#0B4A8F"/>
      <stop offset="1"   stop-color="#052041"/>
    </linearGradient>
    <linearGradient id="crimp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#7C8FA2"/>
      <stop offset=".22" stop-color="#F4F8FB"/>
      <stop offset=".55" stop-color="#B6C6D5"/>
      <stop offset=".8"  stop-color="#8A9CAE"/>
      <stop offset="1"   stop-color="#6D8093"/>
    </linearGradient>
    <linearGradient id="powder" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#FFFFFF" stop-opacity=".70"/>
      <stop offset=".32" stop-color="#FFFFFF" stop-opacity=".93"/>
      <stop offset="1"   stop-color="#D6E3F1" stop-opacity=".96"/>
    </linearGradient>
    <clipPath id="bodyclip">
      <path d="M40 162C40 128 84 120 84 98H126C126 120 170 128 170 162V330a18 18 0 0 1-18 18H58a18 18 0 0 1-18-18Z"/>
    </clipPath>
  </defs>

  <ellipse cx="105" cy="360" rx="64" ry="9" fill="#0A1B2D" opacity=".15"/>

  <!-- cap: flat top, flanged over the crimp ring -->
  <rect x="80" y="16" width="50" height="38" rx="6" fill="url(#cap)"/>
  <rect x="80" y="16" width="50" height="9" rx="4.5" fill="#fff" opacity=".22"/>
  <!-- aluminium crimp collar, wider than the cap and skirted over the neck -->
  <rect x="74" y="48" width="62" height="26" rx="4" fill="url(#crimp)"/>
  <rect x="74" y="68" width="62" height="6" rx="3" fill="#000" opacity=".10"/>
  <!-- short neck -->
  <path d="M84 72h42v28H84z" fill="url(#glass)" stroke="#BFD8EF" stroke-opacity=".36" stroke-width="1.3"/>

  <!-- body: neck flares out over a rounded shoulder, then straight sides to a
       softly rounded base — the proportions of a standard 10ml vial -->
  <path d="M40 162C40 128 84 120 84 98H126C126 120 170 128 170 162V330a18 18 0 0 1-18 18H58a18 18 0 0 1-18-18Z" fill="url(#glass)" stroke="#BFD8EF" stroke-opacity=".45" stroke-width="1.5"/>

  <!-- lyophilised cake settled in the base -->
  <g clip-path="url(#bodyclip)">
    <path d="M40 308c18-7 34-9 65-9s47 2 65 9v58H40z" fill="url(#powder)"/>
  </g>

  <!-- glass highlights, behind the label so they cannot wash over its edges -->
  <rect x="50" y="172" width="8" height="164" rx="4" fill="#fff" opacity=".26"/>
  <rect x="156" y="180" width="4" height="150" rx="2" fill="#fff" opacity=".14"/>

  <!-- label -->
  <rect x="48" y="170" width="114" height="124" rx="5" fill="#fff"/>
  <text __NAMEATTRS__ y="198" font-family="Poppins,sans-serif" font-weight="700" font-size="14" fill="#0A1B2D">__NAME__</text>
  <rect x="76" y="208" width="58" height="22" rx="6" fill="none" stroke="#1573D6" stroke-width="1.6"/>
  <text x="105" y="223" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="600" font-size="11" fill="#0B4A8F">__DOSE__</text>
  <text x="70" y="246" font-family="Poppins,sans-serif" font-weight="600" font-size="6.6" fill="#465D74" textLength="70" lengthAdjust="spacingAndGlyphs">RESEARCH USE ONLY</text>
  <text x="63" y="257" font-family="Poppins,sans-serif" font-weight="500" font-size="5.4" fill="#8296A8" textLength="84" lengthAdjust="spacingAndGlyphs">NOT FOR HUMAN CONSUMPTION</text>
  <rect x="48" y="263" width="114" height="12" fill="#D11B1E"/>
  <text x="65" y="272" font-family="Poppins,sans-serif" font-weight="700" font-size="6.4" fill="#fff" textLength="80" lengthAdjust="spacingAndGlyphs">PEPTIDES COSTA RICA</text>
  <text x="105" y="288" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="500" font-size="5.6" fill="#607285">peptidescostarica.net</text>
</svg>'''


def icon(path, extra=''):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (extra, path))

I = {
  'shield':  icon('<path d="M12 3.2 4.8 6v5.4c0 4.4 3 8.3 7.2 9.4 4.2-1.1 7.2-5 7.2-9.4V6z"/><path d="m9.2 12 2 2 3.6-3.8"/>'),
  'flask':   icon('<path d="M10 3h4"/><path d="M11 3v6.2L5.6 18a2.2 2.2 0 0 0 1.9 3.3h9a2.2 2.2 0 0 0 1.9-3.3L13 9.2V3"/><path d="M8.2 15h7.6"/>'),
  'check':   icon('<path d="M9 4h6a1 1 0 0 1 1 1v1H8V5a1 1 0 0 1 1-1z"/><path d="M16 5.5h2A1.5 1.5 0 0 1 19.5 7v12A1.5 1.5 0 0 1 18 20.5H6A1.5 1.5 0 0 1 4.5 19V7A1.5 1.5 0 0 1 6 5.5h2"/><path d="m8.6 12.4 1.7 1.7 3.4-3.6"/>'),
  'snow':    icon('<path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9"/><path d="M12 6.4 9.9 4.6M12 6.4l2.1-1.8M12 17.6l-2.1 1.8M12 17.6l2.1 1.8"/>'),
  'truck':   icon('<path d="M3 7.5h10.5v9H3z"/><path d="M13.5 10.5H17l3 3v3h-6.5z"/><circle cx="7" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/>'),
  'lock':    icon('<rect x="4.8" y="10.2" width="14.4" height="9.6" rx="2.6"/><path d="M8.2 10.2V7.6a3.8 3.8 0 0 1 7.6 0v2.6"/>'),
  'target':  icon('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1.8v3M12 19.2v3M1.8 12h3M19.2 12h3"/>'),
  'boxes':   icon('<path d="M4 8.2 12 4.4l8 3.8v7.6L12 19.6 4 15.8z"/><path d="M4 8.2 12 12l8-3.8M12 12v7.6"/>'),
  'person':  icon('<circle cx="12" cy="8.4" r="3.6"/><path d="M5.4 20a6.6 6.6 0 0 1 13.2 0"/>'),
  'doc':     icon('<path d="M6.5 3.5h7L18 8v12.5H6.5z"/><path d="M13.2 3.6V8.2H17.9"/><path d="M9.2 12.6h5.6M9.2 16h5.6"/>'),
  'mail':    icon('<rect x="3" y="5.4" width="18" height="13.2" rx="2.6"/><path d="m3.6 7.2 8.4 6 8.4-6"/>'),
  'clock':   icon('<circle cx="12" cy="12" r="8.2"/><path d="M12 7.4V12l3 1.8"/>'),
  'cart':    icon('<path d="M2.8 3.6h2.4l2.3 11.1h9.9"/><path d="M7.5 11.9h9.6l1.9-6H5.9"/><circle cx="9" cy="19" r="1.6"/><circle cx="17" cy="19" r="1.6"/>'),
  'arrow':   icon('<path d="M4.5 12h14M13 6.5l5.5 5.5L13 17.5"/>'),
  'spark':   icon('<path d="M12 3.6l1.9 4.6 4.6 1.9-4.6 1.9L12 16.6l-1.9-4.6L5.5 10l4.6-1.9z"/><path d="M18.4 15.6l.8 1.9 1.9.8-1.9.8-.8 1.9-.8-1.9-1.9-.8 1.9-.8z"/>'),
}

PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
__GTM_HEAD__
<title>__NAME__ __DOSE__ — Research Grade Peptide | Peptides Costa Rica</title>
<meta name="description" content="__NAME__ __DOSE__ for advanced research applications. Verified purity, Certificate of Analysis available, cold-chain shipping. Research use only.">
<meta name="theme-color" content="#06213F">
__ICONS__
<meta property="og:title" content="__NAME__ __DOSE__ — Peptides Costa Rica">
<meta property="og:description" content="High-purity research peptide. Third-party tested, COA available, discreet cold-chain delivery.">
<meta property="og:type" content="product">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
:root{__TOKENS__}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font-family:Poppins,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);
  background:var(--bg);line-height:1.62;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
h1,h2,h3,p,ul,ol{margin:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 clamp(16px,4vw,32px)}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--b900);padding:12px 18px;border-radius:0 0 var(--r-s) 0;z-index:99}
.skip:focus{left:0}

/* ---------- header ---------- */
.hdr{position:sticky;top:0;z-index:40;background:rgba(6,33,63,.92);backdrop-filter:blur(10px);
  border-bottom:1px solid rgba(255,255,255,.10)}
.hdr__in{display:flex;align-items:center;gap:18px;padding:12px 0;min-height:66px}
.brand{display:flex;align-items:center;text-decoration:none;flex:0 0 auto;min-height:40px}
.brand__logo{height:44px;width:auto;display:block}
.nav{display:none;margin-left:auto;gap:clamp(18px,2.4vw,34px)}
.nav a{color:#D6E6F7;text-decoration:none;font-size:.94rem;font-weight:500;padding:6px 2px;border-bottom:2px solid transparent}
.nav a:hover{color:#fff;border-bottom-color:var(--o400)}
@media (min-width:900px){.nav{display:flex}}
.hdr__end{margin-left:auto;display:flex;align-items:center;gap:12px}
@media (min-width:900px){.hdr__end{margin-left:0}}
.lang{display:inline-flex;background:rgba(255,255,255,.12);border-radius:999px;padding:3px}
.lang button{border:0;background:transparent;color:#C9DDF2;font:inherit;font-size:.8rem;font-weight:600;
  padding:6px 13px;border-radius:999px;cursor:pointer;min-height:32px}
.lang button[aria-pressed="true"]{background:#fff;color:var(--b900)}
.lang button:focus-visible{outline:2px solid #fff;outline-offset:2px}

/* ---------- buttons ---------- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;
  padding:13px 26px;border:0;border-radius:999px;font:inherit;font-weight:600;font-size:1rem;
  text-decoration:none;cursor:pointer;transition:transform .16s var(--ease),box-shadow .16s var(--ease),background .16s}
.btn svg{width:19px;height:19px;flex:0 0 auto}
.btn--primary{color:#fff;background:linear-gradient(180deg,var(--o500),var(--o700));
  box-shadow:0 1px 2px rgba(10,27,45,.10),0 10px 24px rgba(168,63,6,.28)}
.btn--primary:hover{transform:translateY(-1px);box-shadow:0 2px 5px rgba(10,27,45,.12),0 14px 30px rgba(168,63,6,.34)}
.btn--ghost{color:#fff;background:transparent;border:1.6px solid rgba(255,255,255,.42)}
.btn--ghost:hover{background:rgba(255,255,255,.10);border-color:#fff}
.btn--outline{color:var(--b700);background:#fff;border:1.6px solid var(--b200)}
.btn--outline:hover{border-color:var(--b500);background:var(--b50)}
.btn--sm{min-height:44px;padding:10px 20px;font-size:.9rem}
.btn--block{width:100%}
.btn:focus-visible{outline:3px solid var(--o400);outline-offset:3px}
@media (prefers-reduced-motion:reduce){.btn{transition:none}.btn:hover{transform:none}}

/* ---------- hero ---------- */
.hero{position:relative;overflow:hidden;color:#fff;
  background:radial-gradient(1100px 620px at 78% 8%,#0E3F79 0%,transparent 62%),
             linear-gradient(165deg,#06213F 0%,#041navy 40%,#03101F 100%)}
.hero{background:radial-gradient(1100px 620px at 78% 8%,#0E3F79 0%,transparent 62%),
                linear-gradient(165deg,#06213F 0%,#062A50 42%,#03101F 100%)}
.hero::after{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(rgba(93,190,254,.16) 1.4px,transparent 1.4px);
  background-size:34px 34px;opacity:.5;mask-image:linear-gradient(105deg,transparent 42%,#000 100%)}
.hero__in>*{min-width:0}
.hero__in{position:relative;z-index:1;display:grid;gap:clamp(24px,4vw,48px);
  padding:clamp(34px,5.6vw,70px) 0 clamp(40px,6vw,76px);align-items:center}
@media (min-width:940px){.hero__in{grid-template-columns:1.06fr .94fr}}
.eyebrow{display:inline-block;font-size:.78rem;font-weight:600;letter-spacing:.16em;
  text-transform:uppercase;color:var(--cyan-lt);margin-bottom:14px}
.hero h1{font-size:clamp(2.7rem,7.4vw,4.6rem);line-height:1.02;letter-spacing:-.028em;font-weight:700}
.dosebadge{display:inline-block;margin-top:16px;padding:7px 20px;border-radius:12px;
  border:2px solid var(--b400);color:#BEE0FF;font-weight:600;font-size:clamp(1.05rem,2.4vw,1.4rem);letter-spacing:.02em}
.hero .tagline{margin-top:22px;font-size:clamp(1.08rem,2.2vw,1.34rem);font-weight:600;line-height:1.42;max-width:min(24ch,100%)}
.hero .blurb{margin-top:12px;color:#B4CCE4;max-width:min(46ch,100%);font-size:.99rem}

.pills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 10px;margin-top:30px;max-width:470px}
@media (min-width:520px){.pills{grid-template-columns:repeat(4,minmax(0,1fr))}}
.pill{text-align:center;color:#CFE3F6;min-width:0}
.pill svg{width:27px;height:27px;color:var(--cyan-lt);margin-bottom:7px}
.pill span{display:block;font-size:.76rem;font-weight:500;line-height:1.35}

.hero__cta{display:flex;flex-wrap:wrap;gap:13px;margin-top:32px}
.hero__art{display:flex;justify-content:center;align-items:center}
.vial{width:clamp(210px,32vw,320px);height:auto;filter:drop-shadow(0 34px 54px rgba(0,0,0,.55))}

/* ---------- assurance strip ---------- */
.strip{position:relative;z-index:2;margin-top:calc(-1 * clamp(20px,3vw,34px))}
.strip__in{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  box-shadow:var(--sh);display:grid;gap:2px;overflow:hidden}
@media (min-width:640px){.strip__in{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.strip__in{grid-template-columns:repeat(4,1fr)}}
.assure{padding:22px clamp(18px,2vw,26px);display:flex;gap:14px;align-items:flex-start}
@media (min-width:640px){.assure+.assure{box-shadow:-1px 0 0 var(--line)}}
@media (min-width:640px) and (max-width:999px){.assure:nth-child(odd){box-shadow:none}
  .assure:nth-child(n+3){box-shadow:0 -1px 0 var(--line)}
  .assure:nth-child(4){box-shadow:-1px 0 0 var(--line),0 -1px 0 var(--line)}}
.assure svg{width:24px;height:24px;color:var(--b500);flex:0 0 auto;margin-top:2px}
.assure h3{font-size:.79rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin-bottom:5px}
.assure p{font-size:.87rem;color:var(--ink2);line-height:1.52}

/* ---------- sections ---------- */
.sec{padding:clamp(48px,7vw,86px) 0}
.sec--white{background:var(--surface)}
.sec--tint{background:linear-gradient(180deg,#fff,var(--b50))}
.kicker{text-align:center;font-size:.78rem;font-weight:600;letter-spacing:.15em;
  text-transform:uppercase;color:var(--b600);margin-bottom:12px}
.kicker--left{text-align:left}
.h2{font-size:clamp(1.55rem,3.4vw,2.25rem);line-height:1.2;letter-spacing:-.018em;font-weight:700}

/* ---------- overview ---------- */
.ov{display:grid;gap:clamp(26px,4vw,44px);align-items:start}
@media (min-width:820px){.ov{grid-template-columns:.72fr 1.28fr}}
@media (min-width:1080px){.ov{grid-template-columns:.66fr 1.2fr .84fr}}
.ov__art{display:flex;justify-content:center;align-items:flex-start}
.ov__art .vial{width:clamp(160px,24vw,230px);filter:drop-shadow(0 22px 34px rgba(10,27,45,.20))}
.ov__body .h2{margin:4px 0 14px}
.ov__body>p{color:var(--ink2);max-width:58ch}
.specs{list-style:none;padding:0;margin:24px 0 0}
.specs li{display:flex;gap:11px;align-items:flex-start;padding:9px 0;border-top:1px solid var(--line);font-size:.94rem}
.specs li:first-child{border-top:0}
.specs svg{width:18px;height:18px;color:var(--b500);flex:0 0 auto;margin-top:4px}
.specs b{font-weight:600}
.specs span{color:var(--ink2)}
.specs__empty{margin-top:22px;padding:16px 18px;border:1px dashed var(--b200);border-radius:var(--r);
  background:var(--b50);color:var(--ink2);font-size:.9rem}

.buy{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  box-shadow:var(--sh);padding:clamp(22px,2.6vw,28px);position:sticky;top:86px}
.buy h3{font-size:.82rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.buy .unit{color:var(--ink3);font-size:.88rem;margin-top:3px}
.buy .price{font-size:clamp(1.9rem,4vw,2.5rem);font-weight:700;color:var(--b700);letter-spacing:-.02em;
  margin:14px 0 4px;line-height:1.1}
.buy .price--ask{font-size:1.22rem;color:var(--ink);font-weight:600;line-height:1.4}
.buy hr{border:0;border-top:1px solid var(--line);margin:18px 0}
.buy ul{list-style:none;padding:0;margin:0 0 20px}
.buy li{display:flex;gap:10px;align-items:flex-start;padding:6px 0;font-size:.9rem;color:var(--ink2)}
.buy li svg{width:17px;height:17px;color:var(--b500);flex:0 0 auto;margin-top:4px}
.buy .fine{margin-top:12px;text-align:center;font-size:.78rem;color:var(--ink3)}
.buy__head{display:flex;align-items:flex-start;gap:10px;justify-content:space-between}
.stock{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:999px;
  background:#E8F8EE;color:#1B6B3A;font-size:.72rem;font-weight:600;letter-spacing:.02em;white-space:nowrap}
.stock i{width:7px;height:7px;border-radius:50%;background:#2FA560;display:block}
.promo{display:flex;gap:8px;align-items:flex-start;margin:10px 0 0;padding:10px 13px;border-radius:var(--r-s);
  background:linear-gradient(180deg,#FFF6EE,#FFEFE2);border:1px solid #F7DCC6;color:#7A3B10;
  font-size:.85rem;font-weight:600;line-height:1.4}
.promo svg{width:16px;height:16px;flex:0 0 auto;margin-top:2px;color:var(--o500)}

/* ---------- why ---------- */
.why{display:grid;gap:26px;margin-top:34px;grid-template-columns:repeat(auto-fit,minmax(168px,1fr))}
.why__i{text-align:center}
.why__i svg{width:30px;height:30px;color:var(--b500);margin-bottom:11px}
.why__i h3{font-size:.97rem;font-weight:600;margin-bottom:5px}
.why__i p{font-size:.86rem;color:var(--ink2);line-height:1.55}

/* ---------- bottom cards ---------- */
.cards{display:grid;gap:22px;grid-template-columns:1fr}
@media (min-width:760px){.cards{grid-template-columns:1fr 1fr}}
@media (min-width:1060px){.cards{grid-template-columns:1.15fr 1fr .85fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  padding:clamp(22px,2.6vw,28px);box-shadow:var(--sh-s)}
.card h3{display:flex;align-items:center;gap:9px;font-size:.79rem;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;margin-bottom:16px}
.card h3 svg{width:18px;height:18px;color:var(--b500)}
.steps{list-style:none;counter-reset:s;padding:0;margin:0}
.steps li{counter-increment:s;display:flex;gap:14px;padding:9px 0}
.steps li::before{content:counter(s);flex:0 0 auto;width:27px;height:27px;border-radius:50%;
  background:var(--b600);color:#fff;font-size:.83rem;font-weight:600;display:grid;place-items:center;margin-top:1px}
.steps b{display:block;font-weight:600;font-size:.93rem}
.steps span{font-size:.86rem;color:var(--ink2);line-height:1.52}
.notice{font-size:.87rem;color:var(--ink2);line-height:1.62}
.contact p{font-size:.88rem;color:var(--ink2);margin-bottom:14px}
.contact a.row{display:flex;gap:10px;align-items:center;color:var(--b600);text-decoration:none;
  font-size:.9rem;font-weight:500;padding:5px 0}
.contact a.row:hover{text-decoration:underline}
.contact .row svg{width:17px;height:17px;flex:0 0 auto}
.contact .hours{display:flex;gap:10px;align-items:center;color:var(--ink2);font-size:.88rem;padding:5px 0}
.contact .hours svg{width:17px;height:17px;color:var(--b500);flex:0 0 auto}

/* ---------- footer ---------- */
.ftr{background:var(--b900);color:#9FBBD6;text-align:center;padding:26px 16px 32px;font-size:.85rem}
.ftr strong{display:block;color:#fff;font-weight:600;margin-bottom:6px}
.ftr a{color:#BFD8EF}

/* ---------- mobile sticky buy bar ---------- */
.buybar{position:fixed;left:0;right:0;bottom:0;z-index:45;display:flex;gap:12px;align-items:center;
  padding:11px clamp(12px,4vw,18px);padding-bottom:calc(11px + env(safe-area-inset-bottom));
  background:rgba(255,255,255,.96);backdrop-filter:blur(10px);border-top:1px solid var(--line);
  box-shadow:0 -6px 22px rgba(10,27,45,.10);transform:translateY(110%);transition:transform .26s var(--ease)}
.buybar.show{transform:none}
.buybar__p{flex:1 1 auto;min-width:0;line-height:1.25}
.buybar__p b{display:block;font-size:.92rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.buybar__p span{font-size:.78rem;color:var(--ink3)}
.buybar .btn{flex:0 0 auto}
@media (min-width:820px){.buybar{display:none}}
@media (prefers-reduced-motion:reduce){.buybar{transition:none}}
body.has-bar{padding-bottom:78px}
@media (min-width:820px){body.has-bar{padding-bottom:0}}
</style>
</head>
<body>
__GTM_BODY__
<a class="skip" href="#overview" data-i18n="skip">Skip to product details</a>

<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="https://peptidescostarica.net/">
      <img class="brand__logo" src="__LOGO_LIGHT__" width="199" height="96" alt="Peptides Costa Rica" fetchpriority="high" decoding="async">
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="__CATALOG__" data-cta="nav-products" data-i18n="nav.products">Products</a>
      <a href="#quality"  data-i18n="nav.quality">Quality</a>
      <a href="#overview" data-i18n="nav.overview">Overview</a>
      <a href="#order"    data-i18n="nav.order">How to order</a>
      <a href="#contact"  data-i18n="nav.contact">Contact</a>
    </nav>
    <div class="hdr__end">
      <div class="lang" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-pressed="true">EN</button>
        <button type="button" data-lang="es" aria-pressed="false">ES</button>
      </div>
      <a class="btn btn--primary btn--sm" href="__CATALOG__" data-cta="header" data-i18n="cta.header">__CART_EN__</a>
    </div>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap hero__in">
    <div>
      <span class="eyebrow" data-i18n="hero.eyebrow">Research grade</span>
      <h1>__NAME__</h1>
      <div><span class="dosebadge">__DOSE__</span></div>
      <p class="tagline" data-i18n="hero.tagline">__TAGLINE_EN__</p>
      <p class="blurb" data-i18n="hero.blurb">__BLURB_EN__</p>

      <div class="pills">
        <div class="pill">__I_SHIELD__<span data-i18n="pill.rou">Research<br>use only</span></div>
        <div class="pill">__I_CHECK__<span data-i18n="pill.tested">Third-party<br>tested</span></div>
        <div class="pill">__I_FLASK__<span data-i18n="pill.purity">Verified<br>purity</span></div>
        <div class="pill">__I_TRUCK__<span data-i18n="pill.ship">Secure<br>shipping</span></div>
      </div>

      <div class="hero__cta">
        <a class="btn btn--primary" href="__CATALOG__" data-cta="hero-primary">__I_CART__<span data-i18n="cta.cart">__CART_EN__</span></a>
        __COA_BTN__
      </div>
    </div>
    <div class="hero__art">__VIAL__</div>
  </div>
</section>

<section class="strip" id="quality" aria-label="Quality assurances">
  <div class="wrap"><div class="strip__in">
    <div class="assure">__I_SHIELD__<div><h3 data-i18n="a1.h">Quality you can trust</h3><p data-i18n="a1.p">Manufactured in controlled environments under strict quality standards.</p></div></div>
    <div class="assure">__I_CHECK__<div><h3 data-i18n="a2.h">Transparent testing</h3><p data-i18n="a2.p">Every batch is tested for identity, purity and potency.</p></div></div>
    <div class="assure">__I_SNOW__<div><h3 data-i18n="a3.h">Cold chain shipping</h3><p data-i18n="a3.p">Held at the correct temperature from our facility to your door.</p></div></div>
    <div class="assure">__I_LOCK__<div><h3 data-i18n="a4.h">Discreet delivery</h3><p data-i18n="a4.p">Secure, unbranded packaging. Your privacy is protected.</p></div></div>
  </div></div>
</section>

<section class="sec" id="overview">
  <div class="wrap ov">
    <div class="ov__art">__VIAL2__</div>

    <div class="ov__body">
      <p class="kicker kicker--left" data-i18n="ov.kicker">Product overview</p>
      <h2 class="h2">__NAME__ __DOSE__</h2>
      <p data-i18n="ov.body">__OVERVIEW_EN__</p>
      __SPECS__
    </div>

    <aside class="buy">
      <div class="buy__head">
        <div>
          <h3>__NAME__ __DOSE__</h3>
          <p class="unit" data-i18n="buy.unit">__UNIT_EN__</p>
        </div>
        __STOCK__
      </div>
      __PRICE__
      __PROMO__
      <hr>
      <ul>
        <li>__I_CHECK__<span data-i18n="buy.b1">Certificate of Analysis with every order</span></li>
        <li>__I_SNOW__<span data-i18n="buy.b2">Temperature-controlled dispatch</span></li>
        <li>__I_LOCK__<span data-i18n="buy.b3">Discreet, unbranded packaging</span></li>
      </ul>
      <a class="btn btn--primary btn--block" href="__CATALOG__" data-cta="buy-card">__I_CART__<span data-i18n="cta.cart2">__CART_EN__</span></a>
      <p class="fine" data-i18n="buy.fine">Supplied for laboratory research use only.</p>
    </aside>
  </div>
</section>

<section class="sec sec--tint">
  <div class="wrap">
    <p class="kicker" data-i18n="why.kicker">Why researchers choose us</p>
    <div class="why">
      <div class="why__i">__I_TARGET__<h3 data-i18n="w1.h">Consistent quality</h3><p data-i18n="w1.p">Rigorous in-house and third-party testing.</p></div>
      <div class="why__i">__I_BOXES__<h3 data-i18n="w2.h">Reliable supply</h3><p data-i18n="w2.p">Stable inventory and on-time delivery.</p></div>
      <div class="why__i">__I_PERSON__<h3 data-i18n="w3.h">Expert support</h3><p data-i18n="w3.p">A knowledgeable team ready to assist.</p></div>
      <div class="why__i">__I_DOC__<h3 data-i18n="w4.h">Documentation</h3><p data-i18n="w4.p">Full COA and testing data provided.</p></div>
      <div class="why__i">__I_LOCK__<h3 data-i18n="w5.h">Privacy first</h3><p data-i18n="w5.p">Your data and your order stay private.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--white" id="order">
  <div class="wrap cards">
    <div class="card">
      <h3>__I_BOXES__<span data-i18n="how.h">How to order</span></h3>
      <ol class="steps">
        <li><div><b data-i18n="s1.t">Browse the catalog</b><span data-i18n="s1.d">Open the product in our catalog to see live availability and pricing.</span></div></li>
        <li><div><b data-i18n="s2.t">Confirm your order</b><span data-i18n="s2.d">Our team follows up by email with availability and next steps.</span></div></li>
        <li><div><b data-i18n="s3.t">Secure checkout</b><span data-i18n="s3.d">Complete your order through our encrypted checkout.</span></div></li>
      </ol>
    </div>

    <div class="card">
      <h3>__I_FLASK__<span data-i18n="note.h">Important notice</span></h3>
      <p class="notice" data-i18n="note.p">This product is intended for laboratory research use only and is not for human consumption. It is not intended to diagnose, treat, cure or prevent any disease. By ordering you confirm that you are a qualified researcher and will use this product only for laboratory research purposes.</p>
    </div>

    <div class="card contact" id="contact">
      <h3>__I_PERSON__<span data-i18n="contact.h">Have questions?</span></h3>
      <p data-i18n="contact.p">Our team is here to help.</p>
      <a class="row" href="mailto:info@peptidescostarica.net">__I_MAIL__<span>info@peptidescostarica.net</span></a>
      <div class="hours">__I_CLOCK__<span data-i18n="contact.hours">Monday to Friday, 9am – 5pm</span></div>
      <a class="btn btn--outline btn--sm btn--block" style="margin-top:14px" href="mailto:info@peptidescostarica.net" data-cta="contact" data-i18n="cta.contact">Contact us</a>
    </div>
  </div>
</section>
</main>

<footer class="ftr">
  <div class="wrap">
    <strong data-i18n="ftr.rou">Research use only. Not for human consumption.</strong>
    <span data-i18n="ftr.rights">&copy; Peptides Costa Rica. All rights reserved.</span>
  </div>
</footer>

<div class="buybar" id="buybar" aria-hidden="true">
  <div class="buybar__p">
    <b>__NAME__ __DOSE__</b>
    <span data-i18n="bar.sub">__UNIT_EN__</span>
  </div>
  <a class="btn btn--primary btn--sm" href="__CATALOG__" data-cta="sticky-bar">__I_CART__<span data-i18n="cta.cart3">__CART_EN__</span></a>
</div>

<script>
(function(){
"use strict";

var PRODUCT = __PRODUCT_JSON__;

var $  = function(s,c){ return (c||document).querySelector(s); };
var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

function track(ev, data){
  var d = data || {}; d.event = ev;
  if (window.dataLayer && window.dataLayer.push) window.dataLayer.push(d);
  if (window.console && console.debug) console.debug("[track]", ev, d);
}

/* ---------- i18n ---------- */
var ES = __ES_JSON__;
var lang = "en";

function snapshot(){ $$("[data-i18n]").forEach(function(el){ el.setAttribute("data-en-html", el.innerHTML); }); }

function setLang(next){
  lang = (next === "es") ? "es" : "en";
  document.documentElement.lang = lang;
  $$("[data-i18n]").forEach(function(el){
    var k = el.getAttribute("data-i18n");
    el.innerHTML = (lang === "es" && ES[k]) ? ES[k] : el.getAttribute("data-en-html");
  });
  $$(".lang button").forEach(function(b){
    b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false");
  });
  // The catalog carries its own language parameter; keep it in step with the page.
  $$("a[data-cta]").forEach(function(a){
    var href = a.getAttribute("href") || "";
    if (href.indexOf("catalog.peptidescostarica.net") === -1) return;
    a.setAttribute("href", href.replace(/([?&]lang=)(en|es)/, "$1" + lang));
  });
  try { localStorage.setItem("pcr_lang", lang); } catch(e){}
  track("language_change", { language: lang });
}

/* ---------- catalog click tracking ----------
   Every route to the catalog is a commercial intent signal, so each one is
   pushed to the dataLayer with the place it was clicked from. Build the GTM
   trigger on select_item. */
function wireCta(){
  $$("a[data-cta]").forEach(function(a){
    a.addEventListener("click", function(){
      var toCatalog = (a.getAttribute("href") || "").indexOf("catalog.") !== -1;
      track(toCatalog ? "select_item" : "cta_click", {
        location: a.getAttribute("data-cta"),
        item_name: PRODUCT.name,
        item_variant: PRODUCT.dose,
        language: lang
      });
    });
  });
}

/* ---------- sticky buy bar on mobile ---------- */
function wireBar(){
  var bar = $("#buybar"), anchor = $(".hero__cta");
  if (!bar || !anchor || !("IntersectionObserver" in window)) return;
  document.body.classList.add("has-bar");
  new IntersectionObserver(function(entries){
    var past = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
    bar.classList.toggle("show", past);
    bar.setAttribute("aria-hidden", past ? "false" : "true");
  }, { threshold: 0 }).observe(anchor);
}

/* ---------- ?audit=1 : what is still unfilled ---------- */
function audit(){
  var missing = [];
  if (!PRODUCT.price) missing.push("price");
  if (!PRODUCT.coaUrl) missing.push("coaUrl");
  PRODUCT.specs.forEach(function(s){ if (!s.value) missing.push("specs." + s.key); });
  if (!missing.length) return;

  console.warn("[product] " + missing.length + " field(s) still empty, so they are hidden from the page:\n  " +
    missing.join("\n  ") + "\nFill them in build-product.py and re-run it.");

  if ((new URLSearchParams(location.search)).get("audit") !== "1") return;
  var b = document.createElement("div");
  b.style.cssText = "position:fixed;left:0;right:0;top:0;z-index:99;background:#8F3604;color:#fff;" +
    "font:600 13px/1.5 Poppins,sans-serif;padding:9px 16px;text-align:center";
  b.textContent = "Draft — still to fill: " + missing.join(", ");
  document.body.appendChild(b);
}

/* ---------- boot ---------- */
snapshot();
$$(".lang button").forEach(function(b){
  b.addEventListener("click", function(){ setLang(b.getAttribute("data-lang")); });
});
var urlLang = (new URLSearchParams(location.search)).get("lang");
var saved = null; try { saved = localStorage.getItem("pcr_lang"); } catch(e){}
var navLang = (navigator.language || "en").toLowerCase().indexOf("es") === 0 ? "es" : "en";
setLang(urlLang === "es" || urlLang === "en" ? urlLang : (saved || navLang));

wireCta(); wireBar(); audit();
track("view_item", { item_name: PRODUCT.name, item_variant: PRODUCT.dose, language: lang });
})();
</script>
</body>
</html>
'''

# ---------------------------------------------------------------- assemble --
def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))

CART = {"en": "Add to cart", "es": "Añadir al carrito"}
COA  = {"en": "View Certificate of Analysis", "es": "Ver certificado de análisis"}

filled = [s for s in PRODUCT['specs'] if s['value']]
if filled:
    rows = '\n'.join(
        '        <li>%s<div><b>%s:</b> <span>%s</span></div></li>'
        % (I['check'], esc(s['label']['en']), esc(s['value'])) for s in filled)
    SPECS = '<ul class="specs" id="specs">\n%s\n      </ul>' % rows
else:
    SPECS = ('<p class="specs__empty" data-i18n="ov.pending">Full specifications — purity, molecular data, '
             'storage and reconstitution guidance — are listed with the product in our catalog, '
             'and the Certificate of Analysis is supplied with every order.</p>')

if PRODUCT['price']:
    PRICE = '<p class="price">%s</p>' % esc(PRODUCT['price'])
else:
    PRICE = ('<p class="price price--ask" data-i18n="buy.ask">Current pricing is shown in our catalog.</p>')

STOCK = ('<span class="stock"><i></i><span data-i18n="buy.stock">In stock</span></span>'
         if PRODUCT.get('inStock') else '')

_promo = PRODUCT.get('promo') or {}
PROMO = ('<p class="promo">%s<span data-i18n="buy.promo">%s</span></p>'
         % (I['spark'], esc(_promo['en']))) if _promo.get('en') else ''

# With no COA link yet the hero would carry a single lone button. The ghost slot
# falls back to an in-page jump, so the button pairing from the design survives.
if PRODUCT['coaUrl']:
    COA_BTN = ('<a class="btn btn--ghost" href="%s" data-cta="hero-coa" data-i18n="cta.coa">%s</a>'
               % (esc(PRODUCT['coaUrl']), COA['en']))
else:
    COA_BTN = '<a class="btn btn--ghost" href="#overview" data-cta="hero-details" data-i18n="cta.details">View product details</a>'

# The label panel is 88 units wide with a little breathing room either side.
# Poppins Bold runs about 0.63em per glyph, so anything that would exceed the
# panel gets pinned with textLength rather than spilling over the edge.
_label = PRODUCT['name'].upper()
# Chromium places text-anchor="middle" inconsistently once textLength is set, so
# a constrained line is positioned from its left edge instead — deterministic,
# and it keeps any product name inside the panel.
_natural = len(_label) * 14 * 0.63
_attrs = ('x="55" textLength="100" lengthAdjust="spacingAndGlyphs"'
          if _natural > 100 else 'x="105" text-anchor="middle"')

vial = (VIAL.replace('__NAMEATTRS__', _attrs)
            .replace('__NAME__', esc(_label))
            .replace('__DOSE__', esc(PRODUCT['dose']))
            .replace('__ALT__', esc('%s %s vial, research use only' % (PRODUCT['name'], PRODUCT['dose']))))

ES_DICT = {
    "skip": "Saltar a los detalles del producto",
    "nav.products": "Productos", "nav.quality": "Calidad", "nav.overview": "Descripción",
    "nav.order": "Cómo pedir", "nav.contact": "Contacto",
    "cta.header": CART['es'], "cta.cart": CART['es'], "cta.cart2": CART['es'], "cta.cart3": CART['es'],
    "cta.coa": COA['es'], "cta.details": "Ver detalles del producto", "cta.contact": "Contáctanos",
    "hero.eyebrow": "Grado investigación",
    "hero.tagline": PRODUCT['tagline']['es'],
    "hero.blurb": PRODUCT['blurb']['es'],
    "pill.rou": "Solo para<br>investigación", "pill.tested": "Analizado por<br>terceros",
    "pill.purity": "Pureza<br>verificada", "pill.ship": "Envío<br>seguro",
    "a1.h": "Calidad en la que confiar", "a1.p": "Fabricado en entornos controlados bajo estrictos estándares de calidad.",
    "a2.h": "Análisis transparentes", "a2.p": "Cada lote se analiza para verificar identidad, pureza y potencia.",
    "a3.h": "Cadena de frío", "a3.p": "Mantenido a la temperatura correcta desde nuestras instalaciones hasta tu puerta.",
    "a4.h": "Entrega discreta", "a4.p": "Embalaje seguro y sin marcas. Tu privacidad está protegida.",
    "ov.kicker": "Descripción del producto",
    "ov.body": PRODUCT['overview']['es'],
    "ov.pending": "Las especificaciones completas — pureza, datos moleculares, conservación y reconstitución — figuran junto al producto en nuestro catálogo, y el certificado de análisis se entrega con cada pedido.",
    "buy.unit": PRODUCT['unit']['es'],
    "buy.ask": "El precio actual se muestra en nuestro catálogo.",
    "buy.stock": "En stock",
    "buy.promo": _promo.get("es", ""),
    "buy.b1": "Certificado de análisis con cada pedido",
    "buy.b2": "Envío con temperatura controlada",
    "buy.b3": "Embalaje discreto y sin marcas",
    "buy.fine": "Suministrado únicamente para uso en investigación de laboratorio.",
    "bar.sub": PRODUCT['unit']['es'],
    "why.kicker": "Por qué los investigadores nos eligen",
    "w1.h": "Calidad constante", "w1.p": "Análisis rigurosos internos y de terceros.",
    "w2.h": "Suministro fiable", "w2.p": "Inventario estable y entregas puntuales.",
    "w3.h": "Soporte experto", "w3.p": "Un equipo capacitado listo para ayudarte.",
    "w4.h": "Documentación", "w4.p": "COA completo y datos de análisis incluidos.",
    "w5.h": "Privacidad ante todo", "w5.p": "Tus datos y tu pedido son privados.",
    "how.h": "Cómo pedir",
    "s1.t": "Explora el catálogo", "s1.d": "Abre el producto en nuestro catálogo para ver disponibilidad y precio actualizados.",
    "s2.t": "Confirma tu pedido", "s2.d": "Nuestro equipo te contacta por correo con la disponibilidad y los siguientes pasos.",
    "s3.t": "Pago seguro", "s3.d": "Completa tu pedido mediante nuestro proceso de pago cifrado.",
    "note.h": "Aviso importante",
    "note.p": "Este producto está destinado únicamente al uso en investigación de laboratorio y no es apto para el consumo humano. No está destinado a diagnosticar, tratar, curar ni prevenir ninguna enfermedad. Al realizar el pedido confirmas que eres un investigador cualificado y que utilizarás este producto solo con fines de investigación de laboratorio.",
    "contact.h": "¿Tienes preguntas?", "contact.p": "Nuestro equipo está aquí para ayudarte.",
    "contact.hours": "De lunes a viernes, 9:00 – 17:00",
    "ftr.rou": "Solo para uso en investigación. No apto para consumo humano.",
    "ftr.rights": "© Peptides Costa Rica. Todos los derechos reservados.",
}

out = PAGE
for k, v in [
    ('__GTM_HEAD__', GTM_HEAD), ('__GTM_BODY__', GTM_BODY), ('__ICONS__', ICONS),
    ('__TOKENS__', TOKENS), ('__LOGO_LIGHT__', LOGO_LIGHT),
    ('__VIAL2__', vial), ('__VIAL__', vial),
    ('__SPECS__', SPECS), ('__PRICE__', PRICE), ('__COA_BTN__', COA_BTN),
    ('__STOCK__', STOCK), ('__PROMO__', PROMO),
    ('__CATALOG__', esc(PRODUCT['catalogUrl'])),
    ('__NAME__', esc(PRODUCT['name'])), ('__DOSE__', esc(PRODUCT['dose'])),
    ('__TAGLINE_EN__', esc(PRODUCT['tagline']['en'])),
    ('__BLURB_EN__', esc(PRODUCT['blurb']['en'])),
    ('__OVERVIEW_EN__', esc(PRODUCT['overview']['en'])),
    ('__UNIT_EN__', esc(PRODUCT['unit']['en'])),
    ('__CART_EN__', CART['en']),
    ('__PRODUCT_JSON__', json.dumps(PRODUCT, ensure_ascii=False)),
    ('__ES_JSON__', json.dumps(ES_DICT, ensure_ascii=False)),
]:
    out = out.replace(k, v)
for name, glyph in I.items():
    out = out.replace('__I_%s__' % name.upper(), glyph)

path = PRODUCT.get('output') or ('product-%s.html' % PRODUCT['slug'])
open(path, 'w', encoding='utf-8').write(out)

pend = [s['key'] for s in PRODUCT['specs'] if not s['value']] + ([] if PRODUCT['price'] else ['price'])
print('%s written, %d bytes' % (path, len(out)))
print('still to fill: %s' % (', '.join(pend) if pend else 'nothing'))
