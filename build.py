#!/usr/bin/env python3
"""
Builds index.html — the GLP-1 guidance landing page.

Layout follows the supplied reference design. Colour, type and logo come from
the Peptides Costa Rica brand kit in brand.py, so the page reads as ours rather
than as the reference.

    python3 build.py

WHAT THIS PAGE DELIBERATELY DOES NOT SAY
  · no compound names — no Retatrutide, Semaglutide, Tirzepatide, Ozempic,
    Wegovy or Zepbound
  · no licensed-provider, clinician or consultation claim. The reference design
    is built on "we connect you with licensed providers"; that claim is not
    made here, and the copy is written so nothing implies it.
  · no prices, cart, checkout or stock
  · no promised outcome and no dosing guidance
GLP-1 is described as the hormone the body produces. Physiology, not a product.
"""
from brand import ICONS, LOGO, LOGO_LIGHT, TOKENS, GTM_HEAD, GTM_BODY

# Lifestyle photograph for the "Built around you" panel, inlined so the page
# stays self-contained. Supplied by the client — see the licensing note in the
# README before this goes live.
PHOTO = open('photo.b64', encoding='utf-8').read().strip()

CFG = {
    "endpoint": "/api/lead",
    "source": "glp1_lp",
    "thankYou": "/thank-you.html",
    "popupMs": 5000,
    "email": "info@peptidescostarica.net",
    "phoneUS": "+1 (831) 471-5559",
    "phoneCR": "+506 8404-6973",
}


def icon(paths, sw="1.7"):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (sw, paths))

I = {
 "check":  icon('<path d="m5 12.5 4.5 4.5L19 7"/>', "2.4"),
 "shield": icon('<path d="M12 3.2 4.8 6v5.4c0 4.4 3 8.3 7.2 9.4 4.2-1.1 7.2-5 7.2-9.4V6z"/><path d="m9.2 12 2 2 3.6-3.8"/>'),
 "flask":  icon('<path d="M10 3h4"/><path d="M11 3v6.2L5.6 18a2.2 2.2 0 0 0 1.9 3.3h9a2.2 2.2 0 0 0 1.9-3.3L13 9.2V3"/><path d="M8.2 15h7.6"/>'),
 "lock":   icon('<rect x="4.8" y="10.2" width="14.4" height="9.6" rx="2.6"/><path d="M8.2 10.2V7.6a3.8 3.8 0 0 1 7.6 0v2.6"/>'),
 "people": icon('<circle cx="9" cy="8.2" r="3.1"/><path d="M3.4 19.4a5.6 5.6 0 0 1 11.2 0"/><path d="M16.4 5.6a3.1 3.1 0 0 1 0 5.6M17.6 19.4a5.6 5.6 0 0 0-1.9-4.2"/>'),
 "user":   icon('<circle cx="12" cy="8.4" r="3.6"/><path d="M5.4 20a6.6 6.6 0 0 1 13.2 0"/>'),
 "mail":   icon('<rect x="3" y="5.4" width="18" height="13.2" rx="2.6"/><path d="m3.6 7.2 8.4 6 8.4-6"/>'),
 "phone":  icon('<path d="M6.2 3.6h3l1.5 3.8-2 1.4a12 12 0 0 0 5.5 5.5l1.4-2 3.8 1.5v3a1.8 1.8 0 0 1-2 1.8A16.4 16.4 0 0 1 4.4 5.6a1.8 1.8 0 0 1 1.8-2z"/>'),
 "cutlery":icon('<path d="M6.5 3v7M4.4 3v4.2a2.1 2.1 0 0 0 4.2 0V3M6.5 10v11"/><path d="M17.6 3c-1.6 1.4-2.4 3.3-2.4 5.4 0 1.6.7 2.8 2.4 3.2V21"/>'),
 "flame":  icon('<path d="M12 21c3.6 0 6-2.4 6-5.6 0-4-3.4-5.6-4.2-9.4-2 1.2-3 3-3 5 0 .9-.6 1.4-1.2 1.4-.9 0-1.5-.8-1.5-2C6.6 12 6 13.4 6 15.4 6 18.6 8.4 21 12 21Z"/>'),
 "drop":   icon('<path d="M12 3.4c3 3.6 5.4 6.4 5.4 9.4a5.4 5.4 0 0 1-10.8 0c0-3 2.4-5.8 5.4-9.4Z"/>'),
 "scale":  icon('<rect x="3.4" y="5.6" width="17.2" height="13.4" rx="3"/><path d="M8.4 15.2a3.9 3.9 0 0 1 7.2 0"/><path d="m12 11.6 2.4-2.4"/>'),
 "doc":    icon('<path d="M6.5 3.5h7L18 8v12.5H6.5z"/><path d="M13.2 3.6V8.2H17.9"/><path d="M9.2 12.6h5.6M9.2 16h5.6"/>'),
 "chat":   icon('<path d="M20.4 12c0 4-3.8 7.2-8.4 7.2a9.9 9.9 0 0 1-2.6-.34L4.6 20.4l1.6-3.9A6.9 6.9 0 0 1 3.6 12c0-4 3.8-7.2 8.4-7.2s8.4 3.2 8.4 7.2Z"/>'),
 "heart":  icon('<path d="M12 20s-7.2-4.4-7.2-9.2A4.1 4.1 0 0 1 12 8.4a4.1 4.1 0 0 1 7.2 2.4C19.2 15.6 12 20 12 20Z"/>'),
 "arrow":  icon('<path d="M4.5 12h14M13 6.5l5.5 5.5L13 17.5"/>'),
 "chevron":icon('<path d="M8 4.5 15.5 12 8 19.5"/>'),
 "plus":   icon('<path d="M12 5.5v13M5.5 12h13"/>', "2"),
 "info":   icon('<circle cx="12" cy="12" r="8.4"/><path d="M12 11.2v5M12 8.1v.1"/>'),
}

# ── Spanish ─────────────────────────────────────────────────────────────────
ES = {
 "wiz.back":"Atrás",
 "q.goal":"¿Qué te gustaría entender mejor?",
 "q.goal.h":"Esto nos dice en qué centrar la información.",
 "q.location":"¿Dónde te encuentras?",
 "q.location.h":"Para orientarte hacia lo que aplica donde estás.",
 "q.stage":"¿En qué punto estás?",
 "q.stage.h":"No hay respuesta incorrecta — solo marca el nivel.",
 "q.language":"¿En qué idioma respondemos?",
 "q.language.h":"Todos los mensajes llegarán en el idioma que elijas.",
 "q.contact":"¿Dónde te lo enviamos?",
 "q.contact.h":"Último paso — y alguien lo retoma desde aquí.",
 "o.glp-1-and-weight-manageme":"GLP-1 y control de peso",
 "o.glp-1-and-appetite":"GLP-1 y apetito",
 "o.glp-1-and-metabolic-healt":"GLP-1 y salud metabólica",
 "o.what-options-exist-genera":"Qué opciones existen en general",
 "o.something-else":"Otra cosa",
 "o.something-else.s":"Cuéntanos y lo cubrimos",
 "o.united-states":"Estados Unidos",
 "o.costa-rica":"Costa Rica",
 "o.somewhere-else":"En otro lugar",
 "o.somewhere-else.s":"Dinos dónde y lo adaptamos",
 "o.just-starting-to-look-int":"Estoy empezando a informarme",
 "o.read-a-lot--still-unsure":"He leído mucho y sigo con dudas",
 "o.read-a-lot--still-unsure.s":"Te lo aclaramos",
 "o.fairly-informed-already":"Ya estoy bastante informado",
 "o.fairly-informed-already.s":"Nos saltamos lo básico",
 "o.not-sure-yet":"Aún no lo sé",
 "o.english":"English",
 "o.espa-ol":"Español",
 "f.fname":"Nombre",
 "f.fname.e":"Escribe tu nombre.",
 "f.lname":"Apellido (opcional)",
 "f.email":"Correo electrónico",
 "f.email.e":"Escribe un correo válido.",
 "f.phone":"Teléfono",
 "f.phone.e":"Escribe un teléfono válido.",
 "f.alt":"Número de mensajería (opcional)",
 "f.consent":"Acepto que me contacten sobre esta solicitud y recibir información educativa ocasional por correo o teléfono. Puedo darme de baja cuando quiera.",
 "f.consent.e":"Marca la casilla para que podamos responderte.",
 "f.apierr":"No pudimos enviar tus datos. Tus respuestas siguen aquí — inténtalo de nuevo.",
 "g.p3":"El enfoque adecuado varía de una persona a otra, y por eso entender tus opciones es un primer paso importante.",
 "skip":"Saltar al formulario",
 "nav.how":"Cómo funciona","nav.about":"Sobre el GLP-1","nav.expect":"Qué esperar",
 "nav.faq":"Preguntas","nav.contact":"Contacto",
 "cta.header":"Recibir orientación","cta.hero":"Recibir orientación gratuita",
 "cta.band":"Recibir orientación gratuita","cta.pop":"Recibir orientación gratuita",
 "hero.eyebrow":"Orientación sobre GLP-1 y control de peso",
 "hero.h1":"Explora las opciones de <em>GLP-1</em>.<br>Entiende tu camino de control de peso.",
 "hero.sub":"Conoce cómo los enfoques basados en GLP-1 pueden apoyar el control de peso y descubre qué opciones podrían ser adecuadas para tus objetivos.",
 "p1.t":"Informar","p1.b":"Entiende cómo actúan los GLP-1 y su papel en el control de peso.",
 "p2.t":"Orientar","p2.b":"Recibe información clara sobre las opciones de GLP-1 disponibles.",
 "p3.t":"Acompañar","p3.b":"Pregunta lo que quieras y recibe orientación directa en el camino.",
 "hero.note":"Información clara. Sin presión. Orientación según tus objetivos.",
 "form.title":"Recibe orientación gratuita sobre el GLP-1",
 "form.kick":"Sin presión. Sin compromiso.",
 "form.sub":"Cuéntanos qué te gustaría entender y te ayudamos a explorar tus opciones.",
 "form.name":"Nombre completo","form.email":"Correo electrónico","form.phone":"Teléfono",
 "form.secure":"Tus datos están protegidos y nunca se comparten.",
 "form.err.name":"Escribe tu nombre.","form.err.email":"Escribe un correo válido.",
 "form.err.phone":"Escribe un teléfono válido.",
 "form.err.api":"No pudimos enviar tus datos. Tus respuestas siguen aquí — inténtalo de nuevo.",
 "form.sending":"Enviando…",
 "t1.t":"Información confiable","t1.b":"Información clara y directa sobre los GLP-1 y el control de peso.",
 "t2.t":"Lenguaje sencillo","t2.b":"Sin jerga innecesaria ni explicaciones confusas.",
 "t3.t":"Tu privacidad importa","t3.b":"Tu información se maneja de forma segura y respetuosa.",
 "t4.t":"Apoyo real","t4.b":"Recibe respuestas de una persona real cuando las necesites.",
 "g.eyebrow":"¿Qué es el GLP-1?","g.h2":"Entender el GLP-1 y el control de peso",
 "g.p1":"El GLP-1 es una hormona de origen natural que interviene en el apetito, la digestión y la regulación de la glucosa.",
 "g.p2":"Los enfoques basados en GLP-1 se discuten ampliamente en el control de peso por su papel en la señal de saciedad y en cómo el cuerpo regula la ingesta de alimentos.",
 "g1.t":"Señal de saciedad","g1.b":"El GLP-1 ayuda a comunicar la sensación de saciedad entre el sistema digestivo y el cerebro.",
 "g2.t":"Ritmo de la digestión","g2.b":"El GLP-1 influye en la rapidez con que los alimentos avanzan por el sistema digestivo.",
 "g3.t":"Respuesta de glucosa","g3.b":"El GLP-1 interviene en la respuesta del cuerpo a la glucosa después de las comidas.",
 "g4.t":"Parte de un conjunto","g4.b":"La alimentación, la actividad, el sueño y la salud general influyen en un control de peso sostenible.",
 "b.eyebrow":"Pensado para ti","b.h2":"Un enfoque más personalizado para tus objetivos de peso",
 "b.p":"Los objetivos, el historial y las dudas de cada persona son distintos. Cuéntanos qué quieres entender y te ayudamos a explorar las opciones relacionadas con el GLP-1, sin darte una respuesta genérica.",
 "b1.t":"Orientación personalizada","b1.b":"Recibe información según las preguntas y objetivos que realmente tienes.",
 "b2.t":"Respuestas claras","b2.b":"Entiende qué significan las distintas opciones en términos prácticos.",
 "b3.t":"Siguientes pasos","b3.b":"Sabrás qué preguntar y qué opciones vale la pena explorar más a fondo.",
 "h.eyebrow":"Cómo funciona","h.h2":"Simple. Privado. Sin presión.",
 "h1.t":"1. Comparte tus objetivos","h1.b":"Cuéntanos qué te gustaría entender sobre los GLP-1 y el control de peso.",
 "h2.t":"2. Lo revisamos","h2.b":"Revisamos tus preguntas y la información que nos das.",
 "h3.t":"3. Recibe orientación clara","h3.b":"Recibe información directa sobre las opciones de GLP-1 y los siguientes pasos.",
 "h4.t":"4. Sigue la conversación","h4.b":"Haz preguntas de seguimiento siempre que necesites más claridad.",
 "h.conf.t":"100% confidencial","h.conf.b":"Tu información se mantiene privada y segura.",
 "faq.eyebrow":"Preguntas frecuentes","faq.h2":"Lo que la gente pregunta",
 "faq1.q":"¿Qué es el GLP-1?",
 "faq1.a":"El GLP-1 es una hormona que interviene en el apetito, la digestión y la regulación de la glucosa. Ciertos medicamentos con receta actúan a través de vías relacionadas con el GLP-1 y pueden formar parte de un plan de control de peso dirigido por un profesional clínico.",
 "faq2.q":"¿El GLP-1 puede ayudar con la pérdida de peso?",
 "faq2.a":"Los medicamentos basados en GLP-1 pueden apoyar la pérdida de peso en algunas personas cuando se recetan de forma adecuada y se combinan con un manejo más amplio del estilo de vida y la salud. Los resultados y la idoneidad varían según cada persona.",
 "faq3.q":"¿Esto es asesoramiento médico?",
 "faq3.a":"No. La información de esta página es educativa y no sustituye el consejo, el diagnóstico ni el tratamiento de un profesional sanitario cualificado.",
 "faq4.q":"¿Qué pasa después de enviar el formulario?",
 "faq4.a":"Te contactaremos con información basada en tus preguntas y te ayudaremos a entender los posibles siguientes pasos.",
 "faq5.q":"¿Enviar el formulario me compromete a algo?",
 "faq5.a":"No. No hay ninguna obligación de comprar ni de continuar con nada.",
 "band.h":"¿Quieres saber más sobre el GLP-1 y la pérdida de peso?",
 "band.p":"Da el primer paso para entender tus opciones.",
 "ftr.priv":"Privacidad","ftr.terms":"Términos","ftr.contact":"Contacto",
 "ftr.legal":"Este sitio web ofrece información educativa general y no proporciona asesoramiento médico, diagnóstico ni tratamiento. La idoneidad para cualquier tratamiento con receta debe determinarla un profesional sanitario cualificado.",
 "pop.kick":"Gratis · Sin compromiso",
 "pop.title":"Recibe orientación gratuita sobre el GLP-1",
 "pop.sub":"Déjanos tus datos y te enviamos información clara. Unos 30 segundos.",
}

QUESTIONS = [
 ("goal", "What would you like to understand better?",
  "This tells us what to focus the information on.", [
   ("GLP-1 and weight management", ""),
   ("GLP-1 and appetite", ""),
   ("GLP-1 and metabolic health", ""),
   ("What options exist generally", ""),
   ("Something else", "Tell us and we will cover it"),
 ]),
 ("location", "Where are you based?",
  "So we can point you to what is relevant where you are.", [
   ("United States", ""),
   ("Costa Rica", ""),
   ("Somewhere else", "Tell us where and we will adapt"),
 ]),
 ("stage", "Where are you in the process?",
  "There is no wrong answer — it just sets the level we pitch it at.", [
   ("Just starting to look into it", ""),
   ("Read a lot, still unsure", "We will cut through it"),
   ("Fairly informed already", "We will skip the basics"),
   ("Not sure yet", ""),
 ]),
 ("language", "Which language should we reply in?",
  "Every message will come in the language you pick.", [
   ("English", ""),
   ("Español", ""),
 ]),
]


def _key(val):
    return "o." + "".join(c if c.isalnum() else "-" for c in val.lower())[:26].strip("-")


def options(key, opts):
    out = []
    for val, sub in opts:
        k = _key(val)
        inner = val
        if sub:
            inner += '<span class="opt__s" data-i18n="%s.s">%s</span>' % (k, sub)
        out.append('<button type="button" class="opt" data-q="%s" data-val="%s">'
                   '<span class="opt__d"></span>'
                   '<span class="opt__t" data-i18n="%s">%s</span></button>'
                   % (key, val, k, inner))
    return "\n            ".join(out)


def wizard(p):
    """The five-step form. p is an id prefix, so it can appear twice on one page."""
    panes = []
    for n, (key, q, hint, opts) in enumerate(QUESTIONS, start=1):
        panes.append(
            '\n        <div class="pane" data-step="%d"%s>'
            '\n          <p class="pane__q" data-i18n="q.%s">%s</p>'
            '\n          <p class="pane__h" data-i18n="q.%s.h">%s</p>'
            '\n          <div class="opts">\n            %s\n          </div>'
            '\n        </div>'
            % (n, "" if n == 1 else " hidden", key, q, key, hint, options(key, opts)))

    contact = (
        '\n        <div class="pane" data-step="5" hidden>'
        '\n          <p class="pane__q" data-i18n="q.contact">Where should we send it?</p>'
        '\n          <p class="pane__h" data-i18n="q.contact.h">Last step — then someone picks it up from here.</p>'
        '\n          <div class="frm">'
        '\n            <input type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true"'
        '\n                   style="position:absolute;left:-9999px;width:1px;height:0;padding:0;border:0;opacity:0">'
        '\n            <div class="row2">'
        '\n              <div class="fld"><span class="fld__i">{user}</span>'
        '\n                <input id="{p}fname" type="text" autocomplete="given-name" placeholder="First name"'
        '\n                       data-i18n-ph="f.fname" aria-describedby="{p}fname-e">'
        '\n                <p class="fld__e" id="{p}fname-e" hidden data-i18n="f.fname.e">Please enter your first name.</p>'
        '\n              </div>'
        '\n              <div class="fld">'
        '\n                <input id="{p}lname" type="text" autocomplete="family-name"'
        '\n                       placeholder="Last name (optional)" data-i18n-ph="f.lname">'
        '\n              </div>'
        '\n            </div>'
        '\n            <div class="fld"><span class="fld__i">{mail}</span>'
        '\n              <input id="{p}email" type="email" autocomplete="email" placeholder="Email Address"'
        '\n                     data-i18n-ph="f.email" aria-describedby="{p}email-e">'
        '\n              <p class="fld__e" id="{p}email-e" hidden data-i18n="f.email.e">Please enter a valid email address.</p>'
        '\n            </div>'
        '\n            <div class="fld"><span class="fld__i">{phone}</span>'
        '\n              <input id="{p}phone" type="tel" autocomplete="tel" placeholder="Phone Number"'
        '\n                     data-i18n-ph="f.phone" aria-describedby="{p}phone-e">'
        '\n              <p class="fld__e" id="{p}phone-e" hidden data-i18n="f.phone.e">Please enter a valid phone number.</p>'
        '\n            </div>'
        '\n            <div class="fld"><span class="fld__i">{chat}</span>'
        '\n              <input id="{p}alt" type="tel" autocomplete="tel"'
        '\n                     placeholder="Messaging number (optional)" data-i18n-ph="f.alt">'
        '\n            </div>'
        '\n            <label class="consent">'
        '\n              <input type="checkbox" id="{p}consent">'
        '\n              <span data-i18n="f.consent">I agree to be contacted about this request and to receive'
        ' occasional educational updates by email or phone. Unsubscribe any time.</span>'
        '\n            </label>'
        '\n            <p class="fld__e" id="{p}consent-e" hidden data-i18n="f.consent.e">Please tick the box so we can reply to you.</p>'
        '\n            <p class="frm__err" id="{p}err" hidden data-i18n="f.apierr">We could not send your details just then.'
        ' Your answers are still here — please press the button again.</p>'
        '\n            <button type="button" class="btn btn--primary btn--block btn--lg" id="{p}btn"'
        '\n                    data-i18n="cta.hero">Get Free Guidance</button>'
        '\n            <p class="frm__secure">{lock}<span data-i18n="form.secure">Your information is secure and will never be shared.</span></p>'
        '\n          </div>'
        '\n        </div>'
    ).format(p=p, user=I["user"], mail=I["mail"], phone=I["phone"], chat=I["chat"], lock=I["lock"])

    return (
        '<div class="wiz" id="%swiz" data-prefix="%s">'
        '\n        <div class="wiz__top">'
        '\n          <button type="button" class="wiz__back" id="%sback" hidden>%s<span data-i18n="wiz.back">Back</span></button>'
        '\n          <p class="wiz__step" id="%sstep">Step 1 of 5</p>'
        '\n        </div>'
        '\n        <div class="wiz__bar"><i id="%sbar"></i></div>'
        '\n        <div class="wiz__chips" id="%schips"></div>%s%s'
        '\n      </div>'
        % (p, p, p, I["chevron"], p, p, p, "".join(panes), contact))


PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
__GTM_HEAD__
<title>Explore GLP-1 Options — Free Guidance | Peptides Costa Rica</title>
<meta name="description" content="Clear, plain-language information about GLP-1 — what it is, how it works in the body, and what may be available to you. Free guidance in English or Spanish. No pressure, no commitment.">
<meta name="theme-color" content="#06213F">
__ICONS__
<meta property="og:title" content="Explore GLP-1 Options — Free Guidance">
<meta property="og:description" content="Understand what GLP-1 is and what may be available to you. Free, no obligation, English or Spanish.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
:root{__TOKENS__}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font-family:Poppins,system-ui,-apple-system,"Segoe UI",sans-serif;
  color:var(--ink);background:var(--surface);line-height:1.62;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
h1,h2,h3,h4,p,ul,ol,dl{margin:0}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(16px,4vw,32px)}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--b900);padding:12px 18px;z-index:99}
.skip:focus{left:0}

/* ── buttons ─────────────────────────────────────────── */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;
  min-height:48px;padding:12px 24px;border:0;border-radius:10px;font:inherit;
  font-weight:600;font-size:.97rem;text-decoration:none;cursor:pointer;
  transition:transform .15s var(--ease),box-shadow .15s var(--ease),background .15s}
.btn svg{width:18px;height:18px;flex:0 0 auto}
.btn--primary{color:#fff;background:linear-gradient(180deg,var(--o500),var(--o700));
  box-shadow:0 1px 2px rgba(10,27,45,.10),0 8px 20px rgba(168,63,6,.24)}
.btn--primary:hover{transform:translateY(-1px);box-shadow:0 2px 5px rgba(10,27,45,.12),0 12px 26px rgba(168,63,6,.32)}
.btn--lg{min-height:56px;font-size:1.03rem;border-radius:12px}
.btn--block{width:100%}
.btn:focus-visible{outline:3px solid var(--b500);outline-offset:3px}
.btn[disabled]{opacity:.72;cursor:progress}
@media (prefers-reduced-motion:reduce){.btn{transition:none}.btn:hover{transform:none}}

/* ── header ──────────────────────────────────────────── */
.hdr{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.hdr__in{display:flex;align-items:center;gap:20px;min-height:74px;padding:11px 0}
.brand{display:flex;align-items:center;flex:0 0 auto;text-decoration:none;min-height:40px}
.brand__logo{height:42px;width:auto;display:block}
.nav{display:none;margin:0 auto;gap:clamp(16px,2.1vw,30px)}
.nav a{font-size:.92rem;font-weight:500;color:var(--ink2);text-decoration:none;
  padding:6px 2px;border-bottom:2px solid transparent}
.nav a:hover{color:var(--b700);border-bottom-color:var(--b500)}
@media (min-width:1000px){.nav{display:flex}}
.hdr__end{margin-left:auto;display:flex;align-items:center;gap:10px}
@media (min-width:1000px){.hdr__end{margin-left:0}}
.lang{display:inline-flex;background:var(--b50);border:1px solid var(--b100);border-radius:999px;padding:3px}
.lang button{border:0;background:transparent;color:var(--b700);font:inherit;font-size:.76rem;
  font-weight:600;padding:5px 11px;border-radius:999px;cursor:pointer;min-height:30px}
.lang button[aria-pressed="true"]{background:#fff;color:var(--b900);box-shadow:var(--sh-s)}
.lang button:focus-visible{outline:2px solid var(--b500);outline-offset:2px}
.hdr .btn{display:none}
@media (min-width:560px){.hdr .btn{display:inline-flex}}

/* ── hero ────────────────────────────────────────────── */
.hero{position:relative;overflow:hidden;
  background:radial-gradient(900px 520px at 88% -6%,var(--b50) 0%,transparent 64%),
             linear-gradient(180deg,#FAFCFE 0%,#F2F8FD 100%)}
.hero__in{display:grid;gap:clamp(30px,4vw,54px);align-items:start;
  padding:clamp(34px,5vw,66px) 0 clamp(40px,5.5vw,72px)}
@media (min-width:960px){.hero__in{grid-template-columns:1.16fr .84fr}}
.hero__in>*{min-width:0}

.eyebrow-pill{display:inline-block;border:1px solid var(--b200);border-radius:999px;
  background:#fff;color:var(--b700);font-size:.71rem;font-weight:600;
  letter-spacing:.11em;text-transform:uppercase;padding:6px 15px}
h1{margin-top:20px;font-size:clamp(2.05rem,4.4vw,2.95rem);line-height:1.12;
  letter-spacing:-.028em;font-weight:700;text-wrap:balance}
h1 em{font-style:normal;color:var(--b500)}
.hero__sub{margin-top:20px;color:var(--ink2);font-size:1.02rem;max-width:52ch}

.pills{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:20px 24px;margin-top:32px}
.pill__h{display:flex;align-items:center;gap:9px;font-weight:600;font-size:.98rem}
.pill__c{flex:0 0 auto;width:22px;height:22px;border-radius:50%;background:var(--b500);
  color:#fff;display:grid;place-items:center}
.pill__c svg{width:13px;height:13px}
.pill p{margin-top:7px;font-size:.88rem;color:var(--ink2);line-height:1.5}

.hero__note{display:flex;gap:13px;align-items:center;margin-top:30px;
  background:var(--b50);border:1px solid var(--b100);border-radius:14px;padding:16px 18px}
.hero__note svg{width:24px;height:24px;color:var(--b600);flex:0 0 auto}
.hero__note p{font-weight:500;font-size:.94rem;line-height:1.45}

/* ── form card ───────────────────────────────────────── */
.card{background:var(--surface);border:1px solid var(--line);border-radius:18px;
  padding:clamp(22px,2.8vw,32px);box-shadow:0 1px 2px rgba(10,27,45,.05),0 22px 50px -26px rgba(10,27,45,.32)}
.card__t{font-size:clamp(1.24rem,2.4vw,1.5rem);line-height:1.28;font-weight:600;
  text-align:center;letter-spacing:-.012em;text-wrap:balance}
.card__rule{width:54px;height:3px;border-radius:2px;background:var(--b500);margin:15px auto 0}
.card__k{margin-top:15px;text-align:center;font-weight:600;font-size:.94rem}
.card__s{margin-top:7px;text-align:center;color:var(--ink2);font-size:.9rem;line-height:1.5}
.fld{position:relative}
.fld__i{position:absolute;left:14px;top:15px;color:var(--ink3);pointer-events:none}
.fld__i svg{width:19px;height:19px;display:block}
.fld input{width:100%;min-height:50px;padding:12px 14px 12px 44px;border:1px solid var(--line);
  border-radius:10px;font:inherit;font-size:.95rem;color:var(--ink);background:var(--surface)}
.fld input::placeholder{color:var(--ink3)}
.fld input:focus{outline:0;border-color:var(--b500);box-shadow:0 0 0 3px var(--b100)}
.fld input[aria-invalid="true"]{border-color:#C4573A;background:#FFF8F6}
.fld__e{margin-top:5px;font-size:.8rem;color:#9E3F22;font-weight:500}
.frm__err{background:#FFF7F5;border:1px solid #F6DED6;border-radius:9px;
  padding:10px 13px;font-size:.85rem;color:#8E3A20}
.frm__secure{display:flex;gap:7px;align-items:center;justify-content:center;
  margin-top:12px;font-size:.8rem;color:var(--ink3)}
.frm__secure svg{width:14px;height:14px;flex:0 0 auto}
/* ── wizard ──────────────────────────────────────────── */
.wiz{margin-top:20px}
.wiz__top{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:30px}
.wiz__back{display:inline-flex;align-items:center;gap:6px;border:0;background:none;padding:6px 4px;
  min-height:30px;font:inherit;font-size:.82rem;font-weight:500;color:var(--ink3);cursor:pointer}
.wiz__back svg{width:14px;height:14px;transform:rotate(180deg)}
.wiz__back:hover{color:var(--b700)}
.wiz__back:focus-visible{outline:2px solid var(--b500);outline-offset:2px;border-radius:6px}
.wiz__back[hidden]{display:none}
.wiz__step{margin-left:auto;font-size:.72rem;font-weight:600;letter-spacing:.07em;
  text-transform:uppercase;color:var(--ink3)}
.wiz__bar{height:4px;border-radius:2px;background:var(--b100);margin-top:8px;overflow:hidden}
.wiz__bar i{display:block;height:100%;width:20%;border-radius:2px;
  background:linear-gradient(90deg,var(--b600),var(--b400));transition:width .3s var(--ease)}
@media (prefers-reduced-motion:reduce){.wiz__bar i{transition:none}}

.wiz__chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.wiz__chips:empty{display:none}
.chip{display:inline-flex;align-items:center;gap:5px;background:var(--b50);border:1px solid var(--b100);
  color:var(--b700);font-size:.73rem;font-weight:500;padding:4px 9px;border-radius:999px;
  max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

.pane{margin-top:18px}
.pane[hidden]{display:none}
.pane__q{font-size:1.06rem;font-weight:600;line-height:1.35;text-wrap:balance}
.pane__h{margin-top:5px;font-size:.85rem;color:var(--ink3);line-height:1.5}
.opts{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.opt{display:flex;align-items:center;gap:11px;width:100%;text-align:left;min-height:52px;
  padding:12px 15px;border:1px solid var(--line);border-radius:11px;background:var(--surface);
  font:inherit;font-size:.94rem;color:var(--ink);cursor:pointer;
  transition:border-color .14s,background .14s}
.opt:hover{border-color:var(--b400);background:var(--b50)}
.opt:focus-visible{outline:3px solid var(--b500);outline-offset:2px}
.opt.sel{border-color:var(--b500);background:var(--b50)}
.opt__d{flex:0 0 auto;width:19px;height:19px;border-radius:50%;border:2px solid var(--b200);
  background:var(--surface);transition:border-color .14s,box-shadow .14s}
.opt.sel .opt__d{border-color:var(--b500);box-shadow:inset 0 0 0 4px var(--b500)}
.opt__t{display:block;line-height:1.35}
.opt__s{display:block;margin-top:2px;font-size:.79rem;color:var(--ink3);font-weight:400}
@media (prefers-reduced-motion:reduce){.opt,.opt__d{transition:none}}

.row2{display:grid;gap:12px}
@media (min-width:420px){.row2{grid-template-columns:1fr 1fr}}
.consent{display:flex;gap:10px;align-items:flex-start;font-size:.81rem;color:var(--ink2);
  line-height:1.48;cursor:pointer;padding:2px 0}
.consent input{flex:0 0 auto;width:18px;height:18px;margin-top:2px;accent-color:var(--b600);cursor:pointer}

/* ── trust strip ─────────────────────────────────────── */
.strip{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--surface)}
.strip__in{display:grid;gap:0}
@media (min-width:600px){.strip__in{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.strip__in{grid-template-columns:repeat(4,1fr)}}
.tr{display:flex;gap:15px;align-items:flex-start;padding:24px clamp(14px,1.8vw,26px)}
@media (min-width:600px){.tr:nth-child(even){box-shadow:inset 1px 0 0 var(--line)}
  .tr:nth-child(n+3){box-shadow:inset 0 1px 0 var(--line)}
  .tr:nth-child(4){box-shadow:inset 1px 0 0 var(--line),inset 0 1px 0 var(--line)}}
@media (min-width:1000px){.tr+.tr{box-shadow:inset 1px 0 0 var(--line)}}
.tr svg{width:30px;height:30px;color:var(--b500);flex:0 0 auto;margin-top:1px}
.tr h3{font-size:.9rem;font-weight:600;margin-bottom:4px}
.tr p{font-size:.84rem;color:var(--ink2);line-height:1.5}

/* ── sections ────────────────────────────────────────── */
.sec{padding:clamp(44px,5.4vw,70px) 0}
.sec--tint{background:linear-gradient(180deg,var(--surface),var(--bg))}
.sec--bg{background:var(--bg)}
.kick{font-size:.72rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--b600)}
.h2{font-size:clamp(1.5rem,3.2vw,2.1rem);line-height:1.2;letter-spacing:-.018em;
  font-weight:700;text-wrap:balance}

/* what is GLP-1 */
.glp{display:grid;gap:clamp(28px,4vw,48px);align-items:start}
@media (min-width:900px){.glp{grid-template-columns:minmax(260px,.72fr) 1.28fr}}
.glp__l .h2{margin:10px 0 16px}
.glp__l p{color:var(--ink2);font-size:.95rem}
.glp__l p+p{margin-top:14px}
.glp__r{display:grid;gap:0;grid-template-columns:1fr 1fr}
@media (min-width:760px){.glp__r{grid-template-columns:repeat(4,1fr)}}
.gi{padding:4px clamp(9px,1.1vw,15px);text-align:center;min-width:0}
.gi+.gi{box-shadow:inset 1px 0 0 var(--line)}
@media (max-width:759px){.gi:nth-child(odd){box-shadow:none}
  .gi:nth-child(n+3){margin-top:26px}}
.gi svg{width:30px;height:30px;color:var(--b500);margin-bottom:12px}
.gi h3{font-size:.9rem;font-weight:600;line-height:1.34;margin-bottom:8px;text-wrap:balance}
.gi p{font-size:.83rem;color:var(--ink2);line-height:1.52}

/* built around you */
.built{display:grid;gap:clamp(26px,3.6vw,44px);align-items:center}
@media (min-width:900px){.built{grid-template-columns:.78fr 1.02fr .9fr}}
.built__art{border-radius:18px;overflow:hidden;aspect-ratio:5/4;background:var(--b50)}
.built__art img{width:100%;height:100%;object-fit:cover;display:block}
.built__b .h2{margin:10px 0 14px}
.built__b p{color:var(--ink2);font-size:.95rem;max-width:46ch}
.ticks{display:flex;flex-direction:column;gap:20px}
.tick{display:flex;gap:13px;align-items:flex-start}
.tick__c{flex:0 0 auto;width:26px;height:26px;border-radius:50%;background:var(--b500);
  color:#fff;display:grid;place-items:center;margin-top:1px}
.tick__c svg{width:15px;height:15px}
.tick h3{font-size:.96rem;font-weight:600;margin-bottom:3px}
.tick p{font-size:.87rem;color:var(--ink2);line-height:1.5}

/* how it works */
.how{display:grid;gap:clamp(26px,3.6vw,42px);align-items:center}
@media (min-width:980px){.how{grid-template-columns:1.42fr .58fr}}
.how__head{text-align:center}
.how__head .h2{margin-top:10px}
.steps{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:center;
  gap:10px;margin-top:34px}
.step{flex:1 1 132px;max-width:172px;text-align:center}
.step__c{width:62px;height:62px;margin:0 auto 13px;border-radius:50%;background:var(--surface);
  border:1px solid var(--b100);display:grid;place-items:center;box-shadow:var(--sh-s)}
.step__c svg{width:26px;height:26px;color:var(--b500)}
.step h3{font-size:.87rem;font-weight:600;margin-bottom:5px}
.step p{font-size:.79rem;color:var(--ink2);line-height:1.45}
.steps__a{flex:0 0 auto;align-self:flex-start;margin-top:20px;color:var(--b200)}
.steps__a svg{width:20px;height:20px;display:block}
@media (max-width:700px){.steps__a{display:none}
  .steps{gap:24px}.step{flex:1 1 44%;max-width:none}}
.conf{background:var(--surface);border:1px solid var(--line);border-radius:16px;
  padding:clamp(22px,2.6vw,30px);text-align:center;box-shadow:var(--sh-s)}
.conf svg{width:44px;height:44px;color:var(--b500);margin-bottom:12px}
.conf h3{font-size:1.06rem;font-weight:600;margin-bottom:7px}
.conf p{font-size:.86rem;color:var(--ink2);line-height:1.5}

/* faq */
.faq{max-width:800px;margin:0 auto}
.faq__head{text-align:center;margin-bottom:30px}
.faq__head .h2{margin-top:10px}
.q{border-top:1px solid var(--line)}
.q:last-child{border-bottom:1px solid var(--line)}
.q__b{width:100%;display:flex;align-items:center;justify-content:space-between;gap:18px;
  background:none;border:0;font:inherit;font-weight:600;font-size:.98rem;color:var(--ink);
  text-align:left;padding:19px 2px;cursor:pointer;min-height:56px}
.q__b:focus-visible{outline:2px solid var(--b500);outline-offset:-2px}
.q__b svg{width:18px;height:18px;color:var(--b500);flex:0 0 auto;transition:transform .22s var(--ease)}
.q__b[aria-expanded="true"] svg{transform:rotate(45deg)}
.q__p{overflow:hidden;height:0;transition:height .26s var(--ease)}
.q__p>div{padding:0 2px 20px;color:var(--ink2);font-size:.92rem;line-height:1.62;max-width:70ch}
@media (prefers-reduced-motion:reduce){.q__p{transition:none}.q__b svg{transition:none}}

/* dark band */
.band{background:linear-gradient(120deg,var(--b900),#0A2A50 55%,#03101F);color:#fff}
.band__in{display:flex;flex-wrap:wrap;gap:22px;align-items:center;justify-content:space-between;
  padding:clamp(26px,3.4vw,40px) 0}
.band__t{font-size:clamp(1.24rem,2.7vw,1.72rem);line-height:1.24;font-weight:700;
  letter-spacing:-.015em;text-wrap:balance}
.band__s{margin-top:7px;color:#B4CCE4;font-size:.94rem}

/* footer */
.ftr{background:var(--surface);border-top:1px solid var(--line);padding:26px 0 34px}
.ftr__in{display:flex;flex-wrap:wrap;gap:18px 34px;align-items:center}
.ftr__logo{height:34px;width:auto;display:block}
.ftr nav{display:flex;flex-wrap:wrap;gap:8px 24px}
.ftr nav a{font-size:.87rem;color:var(--ink2);text-decoration:none;
  display:inline-block;padding:5px 0;min-height:26px}
.ftr nav a:hover{color:var(--b700);text-decoration:underline}
.ftr__legal{margin-left:auto;font-size:.79rem;color:var(--ink3);line-height:1.5;max-width:46ch}
.ftr__copy{margin-top:20px;padding-top:16px;border-top:1px solid var(--line);
  font-size:.79rem;color:var(--ink3)}

/* ── popup ───────────────────────────────────────────── */
.ov{position:fixed;inset:0;z-index:60;display:grid;place-items:center;padding:18px;
  background:rgba(6,20,36,.55);backdrop-filter:blur(5px);
  opacity:0;visibility:hidden;transition:opacity .26s var(--ease),visibility .26s}
.ov.open{opacity:1;visibility:visible}
.ov__c{width:100%;max-width:452px;max-height:92vh;overflow-y:auto;position:relative;
  transform:translateY(14px) scale(.985);transition:transform .28s var(--ease)}
.ov.open .ov__c{transform:none}
.ov__x{position:absolute;top:12px;right:12px;width:36px;height:36px;border-radius:50%;
  border:0;background:var(--b50);color:var(--ink2);font-size:1.15rem;line-height:1;
  cursor:pointer;display:grid;place-items:center}
.ov__x:hover{background:var(--b100)}
.ov__x:focus-visible{outline:2px solid var(--b500);outline-offset:2px}
.ov__k{display:inline-flex;align-items:center;gap:7px;font-size:.72rem;font-weight:600;
  letter-spacing:.08em;text-transform:uppercase;color:var(--b600)}
.ov__k i{width:7px;height:7px;border-radius:50%;background:var(--lime);display:block}
@media (prefers-reduced-motion:reduce){.ov,.ov__c{transition:none}}
body.locked{overflow:hidden}
</style>
</head>
<body>
__GTM_BODY__
<a class="skip" href="#lead" data-i18n="skip">Skip to the guidance form</a>

<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="#top" aria-label="Peptides Costa Rica">
      <img class="brand__logo" src="__LOGO__" width="199" height="96" alt="Peptides Costa Rica" fetchpriority="high" decoding="async">
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="#how"     data-i18n="nav.how">How It Works</a>
      <a href="#about"   data-i18n="nav.about">About GLP-1</a>
      <a href="#expect"  data-i18n="nav.expect">What to Expect</a>
      <a href="#faq"     data-i18n="nav.faq">FAQs</a>
      <a href="#contact" data-i18n="nav.contact">Contact</a>
    </nav>
    <div class="hdr__end">
      <div class="lang" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-pressed="true">EN</button>
        <button type="button" data-lang="es" aria-pressed="false">ES</button>
      </div>
      <a class="btn btn--primary" href="#lead" data-cta="header" data-i18n="cta.header">Get Free Guidance</a>
    </div>
  </div>
</header>

<main id="top">

<section class="hero">
  <div class="wrap hero__in">
    <div>
      <span class="eyebrow-pill" data-i18n="hero.eyebrow">GLP-1 Guidance &amp; Weight Loss Support</span>
      <h1 data-i18n="hero.h1">Explore <em>GLP-1</em> Options.<br>Understand Your Weight Loss Path.</h1>
      <p class="hero__sub" data-i18n="hero.sub">Learn how GLP-1-based approaches may support weight management and discover what options could be appropriate for your goals.</p>

      <div class="pills">
        <div class="pill">
          <div class="pill__h"><span class="pill__c">__I_CHECK__</span><span data-i18n="p1.t">Educate</span></div>
          <p data-i18n="p1.b">Understand how GLP-1s work and their role in weight management.</p>
        </div>
        <div class="pill">
          <div class="pill__h"><span class="pill__c">__I_CHECK__</span><span data-i18n="p2.t">Guide</span></div>
          <p data-i18n="p2.b">Get clear information about available GLP-1 options.</p>
        </div>
        <div class="pill">
          <div class="pill__h"><span class="pill__c">__I_CHECK__</span><span data-i18n="p3.t">Support</span></div>
          <p data-i18n="p3.b">Ask questions and get straightforward guidance along the way.</p>
        </div>
      </div>

      <div class="hero__note">
        __I_PEOPLE__
        <p data-i18n="hero.note">Clear information. No pressure. Guidance built around your goals.</p>
      </div>
    </div>

    <div class="card" id="lead">
      <h2 class="card__t" data-i18n="form.title">Get Free Guidance on GLP-1 Options</h2>
      <div class="card__rule"></div>
      <p class="card__k" data-i18n="form.kick">No pressure. No commitment.</p>
      <p class="card__s" data-i18n="form.sub">Tell us what you’d like to understand and we’ll help you explore your options.</p>
      __FORM_HERO__
    </div>
  </div>
</section>

<section class="strip" aria-label="What to expect from us">
  <div class="wrap"><div class="strip__in">
    <div class="tr">__I_FLASK__<div><h3 data-i18n="t1.t">Information You Can Trust</h3><p data-i18n="t1.b">Clear, straightforward information about GLP-1s and weight management.</p></div></div>
    <div class="tr">__I_DOC__<div><h3 data-i18n="t2.t">Plain Language</h3><p data-i18n="t2.b">No unnecessary jargon or confusing explanations.</p></div></div>
    <div class="tr">__I_LOCK__<div><h3 data-i18n="t3.t">Your Privacy Matters</h3><p data-i18n="t3.b">Your information is handled securely and respectfully.</p></div></div>
    <div class="tr">__I_PEOPLE__<div><h3 data-i18n="t4.t">Real Support</h3><p data-i18n="t4.b">Get answers from a real person when you need them.</p></div></div>
  </div></div>
</section>

<section class="sec" id="about">
  <div class="wrap glp">
    <div class="glp__l">
      <p class="kick" data-i18n="g.eyebrow">What is GLP-1?</p>
      <h2 class="h2" data-i18n="g.h2">Understanding GLP-1 and Weight Management</h2>
      <p data-i18n="g.p1">GLP-1 is a naturally occurring hormone involved in appetite, digestion, and blood sugar regulation.</p>
      <p data-i18n="g.p2">GLP-1-based approaches have become widely discussed in weight management because of their role in appetite signaling and how the body regulates food intake.</p>
      <p data-i18n="g.p3">The right approach varies from person to person, which is why understanding your options is an important first step.</p>
    </div>
    <div class="glp__r">
      <div class="gi">__I_CUTLERY__<h3 data-i18n="g1.t">A role in appetite signaling</h3><p data-i18n="g1.b">GLP-1 helps communicate feelings of fullness between the digestive system and brain.</p></div>
      <div class="gi">__I_FLAME__<h3 data-i18n="g2.t">A role in digestion</h3><p data-i18n="g2.b">GLP-1 influences how quickly food moves through the digestive system.</p></div>
      <div class="gi">__I_DROP__<h3 data-i18n="g3.t">A role in blood sugar</h3><p data-i18n="g3.b">GLP-1 is involved in the body’s response to blood sugar after meals.</p></div>
      <div class="gi">__I_SCALE__<h3 data-i18n="g4.t">Part of a bigger picture</h3><p data-i18n="g4.b">Nutrition, activity, sleep, and overall health all play a role in sustainable weight management.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="expect">
  <div class="wrap built">
    <div class="built__art">
      <img src="__PHOTO__" alt="" width="440" height="352" loading="lazy" decoding="async">
    </div>
    <div class="built__b">
      <p class="kick" data-i18n="b.eyebrow">Built around you</p>
      <h2 class="h2" data-i18n="b.h2">A More Personalized Approach to Your Weight Loss Goals</h2>
      <p data-i18n="b.p">Everyone’s goals, history, and questions are different. Tell us what you’re trying to understand, and we’ll help you explore GLP-1-related options without giving you a one-size-fits-all answer.</p>
    </div>
    <div class="ticks">
      <div class="tick"><span class="tick__c">__I_CHECK__</span><div><h3 data-i18n="b1.t">Personalized Guidance</h3><p data-i18n="b1.b">Get information based on the questions and goals you actually have.</p></div></div>
      <div class="tick"><span class="tick__c">__I_CHECK__</span><div><h3 data-i18n="b2.t">Clear Answers</h3><p data-i18n="b2.b">Understand what the different options mean in practical terms.</p></div></div>
      <div class="tick"><span class="tick__c">__I_CHECK__</span><div><h3 data-i18n="b3.t">Next Steps</h3><p data-i18n="b3.b">Know what questions to ask and what options may be worth exploring further.</p></div></div>
    </div>
  </div>
</section>

<section class="sec sec--bg" id="how">
  <div class="wrap how">
    <div>
      <div class="how__head">
        <p class="kick" data-i18n="h.eyebrow">How it works</p>
        <h2 class="h2" data-i18n="h.h2">Simple. Private. Supportive.</h2>
      </div>
      <div class="steps">
        <div class="step"><div class="step__c">__I_DOC__</div><h3 data-i18n="h1.t">1. Share Your Goals</h3><p data-i18n="h1.b">Tell us what you’d like to understand about GLP-1s and weight management.</p></div>
        <span class="steps__a" aria-hidden="true">__I_ARROW__</span>
        <div class="step"><div class="step__c">__I_USER__</div><h3 data-i18n="h2.t">2. We Review It</h3><p data-i18n="h2.b">We look at your questions and the information you provide.</p></div>
        <span class="steps__a" aria-hidden="true">__I_ARROW__</span>
        <div class="step"><div class="step__c">__I_CHAT__</div><h3 data-i18n="h3.t">3. Get Clear Guidance</h3><p data-i18n="h3.b">Receive straightforward information about GLP-1 options and next steps.</p></div>
        <span class="steps__a" aria-hidden="true">__I_ARROW__</span>
        <div class="step"><div class="step__c">__I_HEART__</div><h3 data-i18n="h4.t">4. Keep the Conversation Going</h3><p data-i18n="h4.b">Ask follow-up questions whenever you need more clarity.</p></div>
      </div>
    </div>
    <div class="conf">
      __I_SHIELD__
      <h3 data-i18n="h.conf.t">100% Confidential</h3>
      <p data-i18n="h.conf.b">Your information is kept private and secure.</p>
    </div>
  </div>
</section>

<section class="sec" id="faq">
  <div class="wrap faq">
    <div class="faq__head">
      <p class="kick" data-i18n="faq.eyebrow">Frequently asked</p>
      <h2 class="h2" data-i18n="faq.h2">What people ask</h2>
    </div>
    __FAQ__
  </div>
</section>

<section class="band">
  <div class="wrap band__in">
    <div>
      <p class="band__t" data-i18n="band.h">Ready to Learn More About GLP-1 and Weight Loss?</p>
      <p class="band__s" data-i18n="band.p">Take the first step toward understanding your options.</p>
    </div>
    <a class="btn btn--primary btn--lg" href="#lead" data-cta="band" data-i18n="cta.band">Get Free Guidance</a>
  </div>
</section>

</main>

<footer class="ftr" id="contact">
  <div class="wrap">
    <div class="ftr__in">
      <img class="ftr__logo" src="__LOGO__" width="199" height="96" alt="Peptides Costa Rica" loading="lazy" decoding="async">
      <nav aria-label="Footer">
        <a href="#" data-i18n="ftr.priv">Privacy Policy</a>
        <a href="#" data-i18n="ftr.terms">Terms of Service</a>
        <a href="mailto:__EMAIL__" data-i18n="ftr.contact">Contact Us</a>
      </nav>
      <p class="ftr__legal" data-i18n="ftr.legal">This website provides general educational information only and does not provide medical advice, diagnosis, or treatment. Eligibility for any prescription treatment must be determined by a licensed healthcare professional.</p>
    </div>
    <p class="ftr__copy">&copy; 2026 Peptides Costa Rica · __EMAIL__ · US __PHONE_US__ · CR __PHONE_CR__</p>
  </div>
</footer>

<div class="ov" id="ov" role="dialog" aria-modal="true" aria-labelledby="popT" hidden>
  <div class="ov__c">
    <div class="card">
      <button type="button" class="ov__x" id="ovX" aria-label="Close">&#215;</button>
      <p class="ov__k"><i></i><span data-i18n="pop.kick">Free · No obligation</span></p>
      <h2 class="card__t" id="popT" style="margin-top:10px" data-i18n="pop.title">Get Free Guidance on GLP-1 Options</h2>
      <div class="card__rule"></div>
      <p class="card__s" data-i18n="pop.sub">Leave your details and we will send you clear information. About 30 seconds.</p>
      __FORM_POP__
    </div>
  </div>
</div>

<script>
(function(){
"use strict";

var CONFIG = __CONFIG__;

var $  = function(s,c){ return (c||document).querySelector(s); };
var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

function track(ev, d){
  d = d || {}; d.event = ev;
  if (window.dataLayer && window.dataLayer.push) window.dataLayer.push(d);
  if (window.console && console.debug) console.debug("[track]", ev, d);
}

/* ---------- attribution: read once, before anything can change the URL ----- */
var ATTR = (function(){
  var q = new URLSearchParams(location.search);
  return {
    utm_source:   q.get("utm_source")   || "",
    utm_medium:   q.get("utm_medium")   || "",
    utm_campaign: q.get("utm_campaign") || "",
    source:       q.get("source")       || CONFIG.source
  };
})();

/* ---------- i18n ---------- */
var ES = __ES__;
var lang = "en";

function snapshot(){
  $$("[data-i18n]").forEach(function(el){ el.setAttribute("data-en", el.innerHTML); });
  $$("[data-i18n-ph]").forEach(function(el){ el.setAttribute("data-en-ph", el.placeholder); });
}
function setLang(next){
  lang = next === "es" ? "es" : "en";
  document.documentElement.lang = lang;
  $$("[data-i18n]").forEach(function(el){
    var k = el.getAttribute("data-i18n");
    el.innerHTML = (lang === "es" && ES[k]) ? ES[k] : el.getAttribute("data-en");
  });
  $$("[data-i18n-ph]").forEach(function(el){
    var k = el.getAttribute("data-i18n-ph");
    el.placeholder = (lang === "es" && ES[k]) ? ES[k] : el.getAttribute("data-en-ph");
  });
  $$(".lang button").forEach(function(b){
    b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false");
  });
  try { localStorage.setItem("pcr_lang", lang); } catch(e){}
}

/* ---------- validation ---------- */
var V = {
  name:  function(v){ return v.trim().length >= 2 && v.trim().length <= 120; },
  email: function(v){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v.trim()) && v.length <= 254; },
  phone: function(v){ var d = v.replace(/\D/g, ""); return d.length >= 7 && d.length <= 15; }
};

function mark(input, bad){
  input.setAttribute("aria-invalid", bad ? "true" : "false");
  var e = document.getElementById(input.id + "-e");
  if (e) e.hidden = !bad;
}

/* ---------- the form ----------
   One wizard, instantiated twice: the hero card and the popup. Each keeps its
   own answers, so a visitor who starts in one and finishes in the other is not
   surprised by half-filled state. Whichever completes first wins; `done` then
   stops the other and stops the popup reopening. */
var sending = false, done = false;
// Set as soon as someone engages with the hero form. The popup checks it, so
// nobody gets a dialog dropped on top of a question they are halfway through.
var engaged = false;

function wizard(prefix, where){
  var root = document.getElementById(prefix + "wiz");
  if (!root) return;

  var panes  = $$(".pane", root);
  var bar    = document.getElementById(prefix + "bar");
  var stepEl = document.getElementById(prefix + "step");
  var backEl = document.getElementById(prefix + "back");
  var chips  = document.getElementById(prefix + "chips");
  var btn    = document.getElementById(prefix + "btn");
  var box    = document.getElementById(prefix + "err");
  var label  = btn.innerHTML;
  var total  = panes.length;
  var step   = 1;
  var answers = {};
  var started = false;

  function paint(){
    panes.forEach(function(pane){
      pane.hidden = Number(pane.getAttribute("data-step")) !== step;
    });
    bar.style.width = Math.round(step / total * 100) + "%";
    stepEl.textContent = (lang === "es" ? "Paso " : "Step ") + step +
                         (lang === "es" ? " de " : " of ") + total;
    backEl.hidden = step === 1;

    chips.innerHTML = "";
    Object.keys(answers).forEach(function(k){
      var c = document.createElement("span");
      c.className = "chip";
      c.textContent = answers[k];
      chips.appendChild(c);
    });
  }

  function go(n){
    step = Math.max(1, Math.min(total, n));
    paint();
    var first = panes[step - 1].querySelector(".opt, input");
    if (first) setTimeout(function(){ first.focus({ preventScroll: true }); }, 60);
  }

  $$(".opt", root).forEach(function(opt){
    opt.addEventListener("click", function(){
      var q = opt.getAttribute("data-q");
      $$('.opt[data-q="' + q + '"]', root).forEach(function(o){ o.classList.remove("sel"); });
      opt.classList.add("sel");
      answers[q] = opt.getAttribute("data-val");
      if (!started){ started = true; track("form_start", { location: where }); }
      if (where === "hero") engaged = true;
      track("form_step", { location: where, step: step, question: q, answer: answers[q] });
      setTimeout(function(){ go(step + 1); }, 220);
    });
  });

  backEl.addEventListener("click", function(){ go(step - 1); });

  $$("input", root).forEach(function(i){
    i.addEventListener("focus", function(){ if (where === "hero") engaged = true; });
    i.addEventListener("input", function(){
      if (i.getAttribute("aria-invalid") === "true") mark(i, false);
      if (box) box.hidden = true;
    });
  });

  btn.addEventListener("click", function(){
    if (sending || done) return;
    if (root.querySelector('[name="company"]').value !== "") return;   // honeypot
    if (box) box.hidden = true;

    var f = document.getElementById(prefix + "fname");
    var e = document.getElementById(prefix + "email");
    var ph = document.getElementById(prefix + "phone");
    var cs = document.getElementById(prefix + "consent");
    var csErr = document.getElementById(prefix + "consent-e");

    var checks = [[f, V.name(f.value)], [e, V.email(e.value)], [ph, V.phone(ph.value)]];
    var bad = null;
    checks.forEach(function(c){ mark(c[0], !c[1]); if (!c[1] && !bad) bad = c[0]; });
    if (csErr) csErr.hidden = cs.checked;
    if (!cs.checked && !bad) bad = cs;
    if (bad){ bad.focus(); track("lead_validation_error", { location: where }); return; }

    var first = f.value.trim();
    var last  = document.getElementById(prefix + "lname").value.trim();
    var payload = {
      name: (first + " " + last).trim(),
      email: e.value.trim(),
      phone: ph.value.trim(),
      language: (answers.language === "Español") ? "es" : (answers.language === "English" ? "en" : lang),
      source: ATTR.source,
      utm_source: ATTR.utm_source, utm_medium: ATTR.utm_medium, utm_campaign: ATTR.utm_campaign
    };
    var detail = {
      goal: answers.goal || "", location: answers.location || "",
      stage: answers.stage || "", preferredLanguage: answers.language || "",
      altPhone: document.getElementById(prefix + "alt").value.trim()
    };

    sending = true;
    btn.disabled = true;
    btn.innerHTML = (lang === "es" && ES["form.sending"]) ? ES["form.sending"] : "Sending…";
    track("lead_submit_attempt", { location: where, source: payload.source });

    post(payload).then(function(){
      done = true;
      track("lead_submit_success", { location: where, source: payload.source });
      try {
        sessionStorage.setItem("pcr_lead", JSON.stringify({
          ts: Date.now(), lang: payload.language,
          lead: {
            firstName: first,
            category: detail.goal,
            location: detail.location,
            volume: detail.stage,
            preferredLanguage: detail.preferredLanguage
          },
          payload: payload, ads: {}, fired: false
        }));
      } catch(err){}
      location.assign(CONFIG.thankYou + "?lang=" + encodeURIComponent(payload.language));
    }).catch(function(err){
      sending = false;
      btn.disabled = false;
      btn.innerHTML = label;
      if (box) box.hidden = false;
      track("lead_submit_failed", { location: where, status: err.status || 0 });
      console.error("Lead submission failed:", err.message, "| endpoint:", CONFIG.endpoint);
    });
  });

  paint();
  return { repaint: paint };
}

function post(payload){
  // file:// has no origin a same-origin path can resolve against
  if (location.protocol === "file:"){
    console.warn("[lead] LOCAL PREVIEW — nothing sent. Payload:", payload);
    return Promise.resolve();
  }
  var ctl = new AbortController();
  var t = setTimeout(function(){ ctl.abort(); }, 15000);
  return fetch(CONFIG.endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
    signal: ctl.signal
  }).then(function(r){
    clearTimeout(t);
    if (!r.ok){ var e = new Error("HTTP " + r.status); e.status = r.status; throw e; }
    return r.json().catch(function(){ return {}; });
  });
}

/* ---------- popup ---------- */
var ov = $("#ov"), lastFocus = null, fired = false;

function openPop(trigger){
  if (fired || done || engaged || ov.classList.contains("open")){
    if (engaged) track("popup_suppressed", { reason: "already filling the form" });
    return;
  }
  fired = true;
  lastFocus = document.activeElement;
  ov.hidden = false;
  requestAnimationFrame(function(){ ov.classList.add("open"); });
  document.body.classList.add("locked");
  setTimeout(function(){ var f = $("#popwiz .opt, #popwiz input"); if (f) f.focus({ preventScroll: true }); }, 240);
  track("popup_open", { trigger: trigger });
}
function closePop(){
  ov.classList.remove("open");
  document.body.classList.remove("locked");
  setTimeout(function(){ ov.hidden = true; }, 280);
  if (lastFocus && lastFocus.focus) lastFocus.focus();
}
$("#ovX").addEventListener("click", closePop);
ov.addEventListener("mousedown", function(e){ if (e.target === ov) closePop(); });
document.addEventListener("keydown", function(e){
  if (e.key === "Escape" && ov.classList.contains("open")) closePop();
  if (e.key === "Tab" && ov.classList.contains("open")){
    var f = $$('button, input, a[href]', ov).filter(function(x){ return x.offsetParent !== null; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
  }
});
setTimeout(function(){ openPop("time-" + CONFIG.popupMs + "ms"); }, CONFIG.popupMs);

/* ---------- faq ---------- */
$$(".q__b").forEach(function(b){
  b.addEventListener("click", function(){
    var panel = b.parentNode.querySelector(".q__p");
    var open = b.getAttribute("aria-expanded") === "true";
    b.setAttribute("aria-expanded", open ? "false" : "true");
    panel.style.height = open ? "0px" : panel.firstElementChild.offsetHeight + "px";
    if (!open) track("faq_open", { question: b.textContent.trim().slice(0, 70) });
  });
});

/* ---------- boot ---------- */
snapshot();
$$(".lang button").forEach(function(b){
  b.addEventListener("click", function(){
    setLang(b.getAttribute("data-lang"));
    if (heroWiz) heroWiz.repaint();
    if (popWiz) popWiz.repaint();
    track("language_change", { language: b.getAttribute("data-lang") });
  });
});
var urlLang = (new URLSearchParams(location.search)).get("lang");
var saved = null; try { saved = localStorage.getItem("pcr_lang"); } catch(e){}
var navLang = (navigator.language || "en").toLowerCase().indexOf("es") === 0 ? "es" : "en";
setLang(urlLang === "es" || urlLang === "en" ? urlLang : (saved || navLang));

var heroWiz = wizard("", "hero");
var popWiz  = wizard("pop", "popup");

$$("a[data-cta]").forEach(function(a){
  a.addEventListener("click", function(){ track("cta_click", { location: a.getAttribute("data-cta"), language: lang }); });
});

track("page_view_lp", { variant: "glp1_design_v2", language: lang });
})();
</script>
</body>
</html>
'''

FAQS = [
 ("faq1", "What is GLP-1?",
  "GLP-1 is a hormone involved in appetite, digestion, and blood sugar regulation. Certain prescription medications work through GLP-1-related pathways and may be used as part of a clinician-directed weight management plan."),
 ("faq2", "Can GLP-1 help with weight loss?",
  "GLP-1-based medications may support weight loss for some people when appropriately prescribed and combined with broader lifestyle and health management. Results and suitability vary by individual."),
 ("faq3", "Is this medical advice?",
  "No. The information on this page is educational and is not a substitute for advice, diagnosis, or treatment from a licensed healthcare professional."),
 ("faq4", "What happens after I submit the form?",
  "We\u2019ll follow up with information based on your questions and help you understand possible next steps."),
 ("faq5", "Does submitting the form commit me to anything?",
  "No. There is no obligation to purchase or proceed with anything."),
]

faq_html = '\n'.join(
  '''    <div class="q">
      <h3><button type="button" class="q__b" aria-expanded="false"><span data-i18n="%s.q">%s</span>%s</button></h3>
      <div class="q__p"><div><p data-i18n="%s.a">%s</p></div></div>
    </div>''' % (k, q, I["plus"], k, a) for k, q, a in FAQS)

import json
out = PAGE
for k, v in [
    ('__GTM_HEAD__', GTM_HEAD), ('__GTM_BODY__', GTM_BODY), ('__ICONS__', ICONS),
    ('__PHOTO__', PHOTO),
    ('__TOKENS__', TOKENS), ('__LOGO__', LOGO),
    ('__FORM_HERO__', wizard('')),
    ('__FORM_POP__',  wizard('pop')),
    ('__FAQ__', faq_html),
    ('__EMAIL__', CFG['email']),
    ('__PHONE_US__', CFG['phoneUS']), ('__PHONE_CR__', CFG['phoneCR']),
    ('__CONFIG__', json.dumps({k: CFG[k] for k in ('endpoint','source','thankYou','popupMs')})),
    ('__ES__', json.dumps(ES, ensure_ascii=False)),
]:
    out = out.replace(k, v)
for name, glyph in I.items():
    out = out.replace('__I_%s__' % name.upper(), glyph)

open('index.html', 'w', encoding='utf-8').write(out)
print('index.html written, %d bytes' % len(out))

# guard
import re
vis = out[out.index('<body>'):]
BAD = [r'\b(Retatrutide|Semaglutide|Tirzepatide|Ozempic|Wegovy|Zepbound)\b',
       r'\badd to cart\b', r'\bbuy now\b', r'\bcheckout\b', r'\bvials?\b',
       r'\$\s?\d', r'\blicensed (provider|professional)', r'\bguaranteed\b']
hits = [m.group(0) for b in BAD for m in re.finditer(b, vis, re.I)]
print('banned-term scan:', 'clean' if not hits else 'HITS ' + str(set(hits)))
