#!/usr/bin/env python3
"""Builds the static pages for Care United Group.

Edit this file (shared head, header, footer, forms and page bodies), then run:
    python3 _build/build.py
It writes index.html, services.html, about.html, contact.html and 404.html
to the repository root. Every path it writes is relative, so the site works
from a GitHub Pages project subfolder as well as from a custom domain.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ facts
# Only facts supplied by the client brief (plus the legal name as listed on the
# public ABN register). Do not add anything that has not been confirmed.
BUSINESS = "Care United Group"
LEGAL = "Care United Group Pty Ltd"
ABN = "44 650 599 787"
STREET = "126 Cardigan St"
SUBURB = "Auburn"
STATE = "NSW"
POSTCODE = "2144"
PHONE1 = "0405 785 338"
PHONE1_TEL = "+61405785338"
PHONE2 = "0404 726 260"
PHONE2_TEL = "+61404726260"
EMAIL = "cug.ndis@gmail.com"
WA_URL = "https://wa.me/61405785338?text=Hi%2C%20I%27d%20like%20to%20ask%20about%20your%20NDIS%20support%20services"
MAP_EMBED = "https://www.google.com/maps?q=126+Cardigan+St,+Auburn+NSW+2144&output=embed"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=126+Cardigan+St+Auburn+NSW+2144"
FORM_ACTION = "https://formspree.io/f/YOUR_FORM_ID"

SERVICES = [
    # key, anchor, name, icon, short description (home page)
    ("health", "health-assistance", "Health assistance", "health",
     "Help with the health side of everyday life, so you can stay well and keep up the routines that matter to you."),
    ("home", "home-care", "Home care", "home",
     "Support to keep your home safe, comfortable and running the way you like it."),
    ("daily", "daily-living", "Support with daily personal activities", "sunrise",
     "Respectful help with your personal routines, at your own pace, so you can do more of your day your way."),
    ("community", "community-participation", "Community participation", "people",
     "Company and support to get out and about, and take part in the community events and activities you enjoy."),
]

# ------------------------------------------------------------------ icons
_I = {
    "phone": '<path d="M5.2 3.8h3.4l1.8 4.6-2.3 1.4a11.5 11.5 0 0 0 6.1 6.1l1.4-2.3 4.6 1.8v3.4a1.9 1.9 0 0 1-2 1.9C10.5 20.2 3.8 13.5 3.3 5.8a1.9 1.9 0 0 1 1.9-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11.4A7 7 0 0 1 19 9.6C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.6"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.2 2"/>',
    "arrow": '<path d="M4.5 12h15M13.5 6l6 6-6 6"/>',
    "arrow-down": '<path d="M12 4.5v15M6 13.5l6 6 6-6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "health": '<path d="M12 20.2s-7.6-4.6-9-9.6C2 7 4.3 4 7.4 4c2 0 3.5 1.1 4.6 2.7C13.1 5.1 14.6 4 16.6 4c3.1 0 5.4 3 4.4 6.6-1.4 5-9 9.6-9 9.6z"/><path d="M6 11.5h3l1.5-2.5 2.5 5 1.5-2.5h3.5"/>',
    "home": '<path d="M3.5 10.8 12 3.8l8.5 7"/><path d="M5.5 9.3V20h13V9.3"/><path d="M10 20v-5.5h4V20"/>',
    "sunrise": '<path d="M3 18.5h18"/><path d="M6.5 18.5a5.5 5.5 0 0 1 11 0"/><path d="M12 4v3.2M4.6 9.4l2.1 1.8M19.4 9.4l-2.1 1.8M2.8 14.5h2.4M18.8 14.5h2.4"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.4 2.7-6 6-6s6 2.6 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16.2 14.1c2.9.3 4.8 2.7 4.8 5.9"/>',
    "shield": '<path d="M12 3.2 19.5 6v5.6c0 4.4-3.1 8.1-7.5 9.2-4.4-1.1-7.5-4.8-7.5-9.2V6z"/><path d="m8.8 12.2 2.3 2.3 4.3-4.5"/>',
    "badge": '<circle cx="12" cy="9" r="5.4"/><path d="M8.7 13.3 7.4 21l4.6-2.6 4.6 2.6-1.3-7.7"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>')


def img(name, widths, alt, sizes, ratio, eager=False, cls=""):
    """Responsive WebP image. ratio = (w, h) of the stored crop."""
    srcset = ", ".join(f"images/{name}-{w}.webp {w}w" for w in widths)
    w = widths[-1]
    h = round(w * ratio[1] / ratio[0])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="images/{name}-{widths[0]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async">')


TODO_PHOTO = "<!-- TODO: replace with real client photos (stock image used as a placeholder) -->"

# ------------------------------------------------------------------ schema
def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": LEGAL,
        "alternateName": BUSINESS,
        "description": "NDIS disability support in Sydney: health assistance, home care, support with daily personal activities and community participation.",
        "taxID": f"ABN {ABN}",
        "telephone": PHONE1_TEL,
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": SUBURB,
            "addressRegion": STATE,
            "postalCode": POSTCODE,
            "addressCountry": "AU",
        },
        "areaServed": {"@type": "City", "name": "Sydney"},
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": PHONE1_TEL, "contactType": "customer service", "areaServed": "AU", "availableLanguage": "English"},
            {"@type": "ContactPoint", "telephone": PHONE2_TEL, "contactType": "customer service", "areaServed": "AU", "availableLanguage": "English"},
        ],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "17:00"},
        ],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[2]}} for s in SERVICES],
    }
    return ('<!-- TODO: once the final domain is live, add "url" and "image" (absolute URLs) to this schema. -->\n'
            '  <script type="application/ld+json">\n' + json.dumps(data, indent=2) + "\n  </script>")


# ------------------------------------------------------------------ shell
def head(title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {extra}<title>{title}</title>
  <meta name="description" content="{desc}">
  <!-- TODO: this is a preview/pitch copy. Remove the noindex line below (and the Disallow in robots.txt) when the site moves to the client's own domain. -->
  <meta name="robots" content="noindex, nofollow">
  <!-- TODO: add <link rel="canonical"> and og:url with the final absolute URL once the domain is confirmed. -->
  <meta name="theme-color" content="#163b35">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{LEGAL}">
  <meta property="og:locale" content="en_AU">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <!-- TODO: social networks need an absolute og:image URL. Change to https://YOUR-DOMAIN/images/og-image.jpg once the domain is final. -->
  <meta property="og:image" content="images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="A support worker pouring a drink for a man in a wheelchair at a kitchen table">
  <meta name="twitter:card" content="summary_large_image">
  <!-- TODO: favicon is a placeholder made from the existing logo mark. Replace with a final icon set if the client has one. -->
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,400..600,0..100&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.className += " js";</script>
  {schema()}
</head>
"""


NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Contact")]


def header(current):
    cur = ' aria-current="page"'
    links = "\n".join(
        f'          <li><a href="{href}"{cur if href == current else ""}>{label}</a></li>'
        for href, label in NAV)
    return f"""<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <!-- TODO: legal name corrected from "Unitrd" to "United" to match the ABN register (ABN {ABN}: CARE UNITED GROUP PTY LTD). Confirm spelling with client. -->
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="{BUSINESS}, home">
        <!-- Logo: one-colour version of the client's existing mark, traced to SVG. TODO: confirm logo use / colours with client. -->
        <img src="images/logo-mark.svg" alt="" width="46" height="51">
        <span class="brand-name">Care United<small>Group Pty Ltd</small></span>
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
{links}
        </ul>
        <div class="nav-extra">
          <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
          <a class="btn btn--ghost" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
          <a class="btn btn--ghost" href="tel:{PHONE2_TEL}">{icon("phone")}Call {PHONE2}</a>
        </div>
      </nav>
      <a class="header-phone" href="tel:{PHONE1_TEL}">{icon("phone")}<span><span class="visually-hidden">Call us on </span>{PHONE1}</span></a>
      <a class="btn btn--primary header-quote" href="contact.html#quote-form"><span class="q-long">Request a quote</span><span class="q-short">Get a quote</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        {icon("menu", "icon-menu")}{icon("close", "icon-close")}
      </button>
    </div>
  </header>
"""


def cta_band(title, text):
    return f"""
    <section class="cta-band on-dark" aria-labelledby="cta-band-title">
      <div class="wrap">
        <div>
          <h2 id="cta-band-title">{title}</h2>
          <p>{text}</p>
        </div>
        <div class="cta-row">
          <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {icon("arrow")}</a>
          <a class="btn btn--ghost" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
        </div>
      </div>
    </section>
"""


def footer():
    service_links = "\n".join(f'            <li><a href="services.html#{s[1]}">{s[2]}</a></li>' for s in SERVICES)
    return f"""
  <footer class="site-footer on-dark">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="footer-brand" href="index.html"><img src="images/logo-mark.svg" alt="" width="44" height="48"><span>{BUSINESS}</span></a>
          <p>NDIS disability support at home and in the community, across Sydney.</p>
          <p>{LEGAL}<br>ABN {ABN}</p>
          <!-- TODO: add NDIS registration status and registration number here once confirmed by the client. -->
          <address>{STREET}, {SUBURB} {STATE} {POSTCODE}</address>
          <div class="footer-cta"><a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a></div>
        </div>
        <div>
          <h2>Contact</h2>
          <ul>
            <li><a href="tel:{PHONE1_TEL}">{PHONE1}</a></li>
            <li><a href="tel:{PHONE2_TEL}">{PHONE2}</a></li>
            <li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp +61 405 785 338<span class="visually-hidden"> (opens in a new tab)</span></a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          </ul>
          <h2 style="margin-top:28px">Opening hours</h2>
          <ul class="footer-hours">
            <li><span>Monday to Friday</span><span>9am to 7pm</span></li>
            <li><span>Saturday</span><span>9am to 5pm</span></li>
            <li><span>Sunday</span><span>Closed</span></li>
          </ul>
        </div>
        <div>
          <h2>Services</h2>
          <ul>
{service_links}
          </ul>
        </div>
        <div>
          <h2>Quick links</h2>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="about.html">About us</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="contact.html#quote-form">Request a quote</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; <span data-year>2026</span> {LEGAL}. All rights reserved.</p>
        <p>Site design and build: <a href="https://nextdigitalevel.com/">Next Digital Level</a></p>
      </div>
    </div>
  </footer>

  <div class="fab-stack">
    <a class="fab fab--call" href="tel:{PHONE1_TEL}" aria-label="Call {BUSINESS} on {PHONE1}">{icon("phone")}</a>
    <a class="fab fab--wa" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Chat with {BUSINESS} on WhatsApp (opens in a new tab)">{WA_SVG}</a>
  </div>

  <script src="js/main.js" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ form
def quote_form(fid, full):
    def services_boxes():
        return "\n".join(
            f'''                <label class="choice"><input type="checkbox" name="services" value="{s[2]}"{f' id="{fid}-services"' if i == 0 else ""}> <span>{s[2]}</span></label>'''
            for i, s in enumerate(SERVICES))

    def radios(name, legend, options, hint=""):
        h = f'<p class="hint" id="{fid}-{name}-hint">{hint}</p>' if hint else ""
        desc = f' aria-describedby="{fid}-{name}-hint"' if hint else ""
        opts = "\n".join(
            f'                <label class="choice"><input type="radio" name="{name}" value="{o}"> <span>{o}</span></label>' for o in options)
        return f'''            <fieldset class="field"{desc}>
              <legend>{legend} <span class="visually-hidden">(optional)</span></legend>
              {h}
              <div class="choices choices--2">
{opts}
              </div>
            </fieldset>'''

    email_suburb = f'''            <div class="form-grid form-grid--2">
              <div class="field" data-field="email">
                <label for="{fid}-email">Email</label>
                <input type="email" id="{fid}-email" name="email" autocomplete="email" inputmode="email" aria-describedby="{fid}-email-error">
                <p class="error-msg" id="{fid}-email-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="{fid}-suburb">Suburb</label>
                <input type="text" id="{fid}-suburb" name="suburb" autocomplete="address-level2">
              </div>
            </div>'''

    who = f'''            <div class="field">
              <label for="{fid}-who">I am a&hellip;</label>
              <select id="{fid}-who" name="enquirer">
                <option value="">Please choose</option>
                <option>Participant</option>
                <option>Family member or carer</option>
                <option>Support coordinator</option>
                <option>Other</option>
              </select>
            </div>''' if full else ""

    plan = radios("plan_management", "How is the NDIS plan managed?",
                  ["Self-managed", "Plan-managed", "NDIA-managed", "Not sure"]) if full else ""

    contact_method = radios("contact_method", "How would you like us to contact you?", ["Phone", "WhatsApp", "Email"])

    message = f'''            <div class="field">
              <label for="{fid}-message">{"Tell us about the support you need" if full else "Anything you'd like us to know?"}</label>
              <p class="hint" id="{fid}-message-hint">For example, which days suit you, or what matters most to you. Please don't include detailed medical information.</p>
              <textarea id="{fid}-message" name="message" rows="{5 if full else 3}" aria-describedby="{fid}-message-hint"></textarea>
            </div>'''

    return f'''
          <div class="form-head">
            <h{2 if full else 3} id="{fid}-title">{"Request a quote" if full else "Request a quote"}</h{2 if full else 3}>
            <p class="form-intro">{"Fill in as much as you can. It helps us understand what you need before we call." if full else "Just the basics for now. We'll call you to talk it through."}</p>
          </div>
          <!-- TODO: replace YOUR_FORM_ID with the real Formspree form ID (create the form at formspree.io with {EMAIL} as the recipient). Until then the form shows the thank-you message but sends nothing. -->
          <form id="{fid}" class="quote-form" action="{FORM_ACTION}" method="POST" novalidate data-quote-form aria-labelledby="{fid}-title">
            <div class="form-summary" tabindex="-1" role="alert">
              <h3>Please check a few things</h3>
              <ul></ul>
            </div>
            <input type="hidden" name="_subject" value="New quote request from the website ({"full form" if full else "home page"})">
            <div class="hp" aria-hidden="true">
              <label for="{fid}-gotcha">Leave this field empty</label>
              <input type="text" id="{fid}-gotcha" name="_gotcha" tabindex="-1" autocomplete="off">
            </div>
            <p class="req-note">Fields marked <abbr title="required">*</abbr> are required.</p>
            <div class="form-grid">
            <div class="form-grid form-grid--2">
              <div class="field" data-field="name">
                <label for="{fid}-name">Full name <abbr title="required">*</abbr></label>
                <input type="text" id="{fid}-name" name="name" autocomplete="name" required aria-required="true" aria-describedby="{fid}-name-error">
                <p class="error-msg" id="{fid}-name-error" aria-live="polite"></p>
              </div>
              <div class="field" data-field="phone">
                <label for="{fid}-phone">Phone <abbr title="required">*</abbr></label>
                <input type="tel" id="{fid}-phone" name="phone" autocomplete="tel" inputmode="tel" required aria-required="true" aria-describedby="{fid}-phone-error">
                <p class="error-msg" id="{fid}-phone-error" aria-live="polite"></p>
              </div>
            </div>
{email_suburb}
{who}
            <fieldset class="field" data-field="services" aria-describedby="{fid}-services-error">
              <legend>Which services are you interested in? <abbr title="required">*</abbr></legend>
              <p class="hint">Choose as many as you like.</p>
              <div class="choices choices--2" data-validate>
{services_boxes()}
              </div>
              <p class="error-msg" id="{fid}-services-error" aria-live="polite"></p>
            </fieldset>
{plan}
{contact_method}
{message}
            <div class="field" data-field="consent">
              <label class="consent" for="{fid}-consent"><input type="checkbox" id="{fid}-consent" name="consent" value="Yes" required aria-required="true" aria-describedby="{fid}-consent-error"> <span>I agree to Care United Group contacting me about my enquiry. <abbr title="required">*</abbr></span></label>
              <p class="error-msg" id="{fid}-consent-error" aria-live="polite"></p>
            </div>
            <div class="form-actions">
              <button class="btn btn--primary" type="submit"><span>Send my request</span> {icon("arrow")}</button>
              <p class="form-fine">Prefer to talk? Call <a href="tel:{PHONE1_TEL}">{PHONE1}</a>.</p>
            </div>
            <p class="form-error-send" tabindex="-1" role="alert">Sorry, your request didn't send. Please try again, or call us on <a href="tel:{PHONE1_TEL}">{PHONE1}</a>.</p>
            </div>
          </form>
          <div class="form-success" tabindex="-1" role="status" aria-live="polite">
            <div class="tick">{icon("check")}</div>
            <h{2 if full else 3}>Thank you, we've got your request</h{2 if full else 3}>
            <p>We'll be in touch soon using the contact method you chose. If it's urgent, please call us on <a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a>.</p>
          </div>'''


def contact_options():
    return f'''<ul class="contact-options">
            <li><a href="tel:{PHONE1_TEL}">{icon("phone")}<span><strong>{PHONE1}</strong><span>Call us</span></span></a></li>
            <li><a href="tel:{PHONE2_TEL}">{icon("phone")}<span><strong>{PHONE2}</strong><span>Or our second line</span></span></a></li>
            <li><a class="wa" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}<span><strong>WhatsApp</strong><span>Send us a message<span class="visually-hidden"> (opens in a new tab)</span></span></span></a></li>
            <li><a href="mailto:{EMAIL}">{icon("mail")}<span><strong>{EMAIL}</strong><span>Email us</span></span></a></li>
          </ul>'''


def hours_list():
    return '''<ul class="hours">
                  <li><span>Monday to Friday</span><span>9am to 7pm</span></li>
                  <li><span>Saturday</span><span>9am to 5pm</span></li>
                  <li><span>Sunday</span><span>Closed</span></li>
                </ul>'''


def or_call():
    return f'<span class="or">or call <a href="tel:{PHONE1_TEL}">{PHONE1}</a></span>'


# ------------------------------------------------------------------ pages
def page_home():
    items = "\n".join(f'''            <li class="reveal">
              <div class="icon">{icon(s[3])}</div>
              <div class="body">
                <h3>{s[2]}</h3>
                <p>{s[4]}</p>
                <a class="text-link" href="services.html#{s[1]}"><span>More about {s[2].lower() if s[0] != "daily" else "daily personal support"}</span>{icon("arrow")}</a>
              </div>
            </li>''' for s in SERVICES)

    body = f"""
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <h1 id="hero-title">NDIS support in Sydney, <span class="soft">planned around you</span></h1>
          <p class="lead">Care United Group helps people with disability live well at home and take part in their community. We start by getting to know you, then build support that fits your goals, your routine and your NDIS plan.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {icon("arrow")}</a>
            <a class="btn btn--ghost" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
          </div>
          <dl class="hero-meta">
            <div><dt>{icon("pin")}Based in Auburn</dt><dd>Supporting people across Sydney</dd></div>
            <div><dt>{icon("clock")}Open six days</dt><dd>Mon to Fri 9am to 7pm, Sat 9am to 5pm</dd></div>
          </dl>
        </div>
        <div class="hero-media">
          {TODO_PHOTO}
          {img("hero", [640, 1000], "A support worker pours a glass of juice for a young man in a wheelchair at a kitchen table", "(min-width: 900px) 40vw, 92vw", (4, 5), eager=True)}
          <p class="hero-note"><strong>Four kinds of support</strong>Health, home care, daily personal activities and community participation.</p>
        </div>
      </div>
    </section>

    <section class="section section--paper" aria-labelledby="services-title">
      <div class="wrap split">
        <div class="sticky reveal">
          <h2 id="services-title">How we can help</h2>
          <p>Everyone's support looks different. These are the four areas we work in. You can choose one, or combine them into one plan.</p>
          <p>Not sure what you need yet? That's fine. Tell us what a normal week looks like, and we'll help you work it out.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            <a class="text-link" href="services.html"><span>See all services</span>{icon("arrow")}</a>
          </div>
        </div>
        <ul class="service-list">
{items}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="how-title">
      <div class="wrap split split--reverse">
        <div class="media-frame media-frame--offset reveal-img">
          {TODO_PHOTO}
          {img("assess", [700, 1100], "A support worker with a clipboard listens to a woman during a conversation at home", "(min-width: 900px) 52vw, 92vw", (5, 4))}
        </div>
        <div class="reveal">
          <h2 id="how-title">We get to know you before we plan anything</h2>
          <p>Good support starts with listening. Here is what happens after you get in touch.</p>
          <ol class="steps">
            <li>
              <h3>We assess your needs</h3>
              <p>We talk with you, and your family or support coordinator if you like, about your needs, what you can already do and where you'd like help.</p>
            </li>
            <li>
              <h3>We create a support plan with you</h3>
              <p>Together we put together a plan tailored to you: the support you'll get, when you'll get it, and how it fits your NDIS plan.</p>
            </li>
            <li>
              <h3>We adjust it as your needs change</h3>
              <p>Life changes, and your support should change with it. We check in and update your plan whenever your needs change.</p>
            </li>
          </ol>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Start with a conversation</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--forest on-dark" aria-labelledby="values-title">
      <div class="wrap values-grid">
        <div class="reveal">
          <h2 id="values-title">What you can count on</h2>
          <p>Three things guide how we work with every participant.</p>
          <ul class="values-list">
            <li>
              <h3>{icon("badge")}Experience</h3>
              <p>You deserve support from people who know the work. Experience means calmer days and more confidence, for you and for your family.</p>
            </li>
            <li>
              <h3>{icon("clock")}Punctuality</h3>
              <p>We turn up when we say we will. If something changes, we let you know early. Your time matters.</p>
            </li>
            <li>
              <h3>{icon("shield")}Safety</h3>
              <p>Safety comes first for every participant, at home and out in the community. We take care at every step.</p>
            </li>
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
        <div class="values-photo reveal-img">
          {TODO_PHOTO}
          {img("community-friends", [600, 900], "Four friends, one of them in a wheelchair, smiling together on a sunny waterfront boardwalk", "(min-width: 900px) 44vw, 92vw", (4, 5))}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="who-title">
      <div class="wrap">
        <div class="reveal">
          <h2 id="who-title">Whoever is reaching out, we're glad you did</h2>
          <p class="lead">You might be looking for support for yourself, for someone you love, or for a participant you work with.</p>
        </div>
        <div class="audience reveal">
          <div>
            <h3>Participants</h3>
            <p>Tell us what you'd like help with and what matters to you. We'll explain your options in plain English, and you stay in charge of your support.</p>
          </div>
          <div>
            <h3>Families and carers</h3>
            <p>Looking for support for someone you care about? We'll work with you as part of their team, with their consent.</p>
          </div>
          <div>
            <h3>Support coordinators</h3>
            <p>Send us an enquiry with the participant's needs and suburb, and we'll come back to you with what we can offer.</p>
          </div>
        </div>
        <div class="cta-row">
          <a class="btn btn--primary" href="contact.html#quote-form">Send an enquiry</a>
          {or_call()}
        </div>
      </div>
    </section>

    <!-- TODO: participant and family feedback. Add real quotes only, with written permission from each person. Never invent names, quotes or star ratings. Remove this placeholder block once real feedback is added. -->
    <section class="section section--sand" aria-labelledby="feedback-title">
      <div class="wrap">
        <div class="placeholder reveal">
          <span class="tag">Coming soon</span>
          <h2 id="feedback-title">In their own words</h2>
          <p>We'll share feedback from participants and families here, with their permission.</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="area-title">
      <div class="wrap area-grid">
        <div class="reveal-img">
          {TODO_PHOTO}
          {img("cafe", [532], "Friends, two of them in wheelchairs, chatting over drinks at an outdoor cafe table", "(min-width: 900px) 34vw, 92vw", (1, 1))}
        </div>
        <div class="reveal">
          <h2 id="area-title">Based in Auburn, supporting people across Sydney</h2>
          <p>Our office is at {STREET}, {SUBURB}. We support participants across Sydney, at home and out in the community. Not sure if we cover your suburb? Just ask.</p>
          <!-- TODO: list the suburbs or regions the client confirms they cover (e.g. for local SEO). Do not add areas until confirmed. -->
          <dl class="details">
            <div><dt>{icon("pin")}Address</dt><dd><a href="{MAP_LINK}" target="_blank" rel="noopener">{STREET}, {SUBURB} {STATE} {POSTCODE}<span class="visually-hidden"> (opens Google Maps in a new tab)</span></a></dd></div>
            <div><dt>{icon("clock")}Opening hours</dt><dd>{hours_list()}</dd></div>
            <div><dt>{icon("phone")}Phone</dt><dd><a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a></dd></div>
          </dl>
          <div class="cta-row">
            <a class="btn btn--primary" href="#quote">Ask if we cover your area</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--sand" id="quote" aria-labelledby="quote-title">
      <div class="wrap quote-grid">
        <div class="sticky">
          <h2 id="quote-title">Ask us for a quote</h2>
          <p>Tell us a little about the support you're looking for. We'll get back to you to talk it through, with no obligation.</p>
          {contact_options()}
          <p style="margin-top:24px">Want to tell us more? Use the <a href="contact.html#quote-form">full quote form</a>.</p>
        </div>
        <div class="form-card">
{quote_form("home-quote", full=False)}
        </div>
      </div>
    </section>
  </main>
"""
    return (head("NDIS Support Services Sydney | Care United Group, Auburn",
                 "NDIS disability support in Sydney from Care United Group in Auburn: health assistance, home care, daily personal activities and community participation. Request a quote.")
            + header("index.html") + body + footer())


SERVICE_DETAIL = {
    "health": {
        "img": ("health", "A support worker checks a woman's blood pressure at home while a family member sits with her"),
        "intro": [
            "Staying well takes effort, and you don't have to manage it on your own.",
            "We support you with the health-related parts of your day, in a way that fits your routine, your goals and your NDIS plan.",
        ],
        "list": [
            "Support to keep up the health routines that are part of your plan",
            "Help getting ready for appointments",
            "Keeping your family or support team in the loop, with your permission",
        ],
    },
    "home": {
        "img": ("home-care", "A support worker hands a glass of water to a woman resting on a sofa at home"),
        "intro": [
            "Home should feel safe and comfortable.",
            "We help with the jobs that keep your home running, so you can spend your energy on the things you enjoy.",
        ],
        "list": [
            "Help with household tasks around your home",
            "Keeping your space safe, tidy and easy to move around",
            "Support that follows your routine and the way you like things done",
        ],
    },
    "daily": {
        "img": ("daily-living", "A woman in a wheelchair prepares breakfast in her kitchen"),
        "intro": [
            "Everyday routines are personal.",
            "We help with them respectfully and at your pace, building on what you can already do, so you keep as much independence as you want.",
        ],
        "list": [
            "Help with personal routines, such as getting ready for the day",
            "Support at the times of day that suit you",
            "Care that respects your privacy, dignity and choices",
        ],
    },
    "community": {
        "img": ("community", "A group of friends laughing together outdoors in a park"),
        "intro": [
            "Being part of your community matters.",
            "We support you to get out, join in and enjoy the community events and activities you care about, with someone you trust beside you.",
        ],
        "list": [
            "Going to community events and activities",
            "Trying a new interest, or getting back to an old one",
            "Building confidence when you're out and about",
        ],
    },
}


def page_services():
    jump = "\n".join(
        f'            <li><a href="#{s[1]}">{icon(s[3], "ico")}{s[2]}{icon("arrow-down", "arrow")}</a></li>' for s in SERVICES)
    blocks = []
    for i, s in enumerate(SERVICES):
        d = SERVICE_DETAIL[s[0]]
        intro = "\n".join(f"            <p>{p}</p>" for p in d["intro"])
        ticks = "\n".join(f'              <li>{icon("check")}<span>{t}</span></li>' for t in d["list"])
        sec_cls = "section section--paper" if i % 2 else "section"
        flip = " service-block--flip" if i % 2 else ""
        blocks.append(f"""
    <section class="{sec_cls}" id="{s[1]}" aria-labelledby="{s[1]}-title">
      <div class="wrap service-block{flip}">
        <div class="reveal">
          <div class="num-icon">{icon(s[3])}</div>
          <h2 id="{s[1]}-title">{s[2]}</h2>
{intro}
          <p class="ticks-title">This can include:</p>
          <!-- TODO: confirm these examples with the client before launch. -->
          <ul class="ticks">
{ticks}
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html?service={s[0]}#quote-form">Ask about {s[2].lower() if s[0] != "daily" else "daily personal support"}</a>
            {or_call()}
          </div>
        </div>
        <div class="photo reveal-img">
          {TODO_PHOTO}
          {img(d["img"][0], [700, 1200] if s[0] == "community" else [700, 1100], d["img"][1], "(min-width: 900px) 42vw, 92vw", (4, 3) if s[0] != "community" else (3, 2))}
        </div>
      </div>
    </section>""")

    body = f"""
  <main id="main">
    <section class="page-hero page-hero--split" aria-labelledby="page-title">
      <div class="wrap">
        <div>
          <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> Services</p>
          <h1 id="page-title">NDIS support services in Sydney</h1>
          <p class="lead">We offer four kinds of disability support for NDIS participants across Sydney. Each one is tailored to the person, and you can combine them in one plan.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {icon("arrow")}</a>
            {or_call()}
          </div>
        </div>
        <nav aria-label="Services on this page">
          <ul class="jump">
{jump}
          </ul>
        </nav>
      </div>
    </section>

    <div class="wrap wide-photo reveal-img">
      {TODO_PHOTO}
      {img("kitchen", [900, 1600], "A support worker and a young woman help an older woman in a wheelchair prepare vegetables at the kitchen table", "(min-width: 1240px) 1144px, 92vw", (2, 1))}
    </div>
{"".join(blocks)}

    <section class="section section--sand" aria-labelledby="start-title">
      <div class="wrap split">
        <div class="reveal">
          <h2 id="start-title">Every service starts the same way</h2>
          <p>Whichever support you choose, we begin by understanding you. Then we plan together, and we keep adjusting as your needs change.</p>
        </div>
        <div class="reveal">
          <ol class="steps" style="margin-top:0">
            <li><h3>We assess your needs</h3><p>A conversation about your needs, your abilities and what you'd like help with.</p></li>
            <li><h3>We create your support plan</h3><p>A plan tailored to you, that fits your routine and your NDIS plan.</p></li>
            <li><h3>We adjust it as things change</h3><p>We review your support and update it whenever your needs change.</p></li>
          </ol>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>
{cta_band("Not sure which support you need?", "Tell us about your week and what you'd like help with. We'll suggest options that fit you.")}
  </main>
"""
    return (head("NDIS Home Care & Disability Support Services Sydney | Care United Group",
                 "Health assistance, home care, support with daily personal activities and community participation for NDIS participants across Sydney. Based in Auburn.")
            + header("services.html") + body + footer())


def page_about():
    body = f"""
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> About</p>
        <h1 id="page-title">About Care United Group</h1>
        <p class="lead">We're a disability support provider based in Auburn, working with NDIS participants and their families across Sydney.</p>
        <!-- TODO: NDIS registration status and registration number go here once confirmed by the client. Make no claim about NDIS registration until the client confirms it. -->
      </div>
    </section>

    <section class="section section--paper" aria-labelledby="approach-title">
      <div class="wrap about-intro">
        <div class="media-frame media-frame--offset reveal-img">
          {TODO_PHOTO}
          {img("about", [600, 900], "A woman in a wheelchair and a friend share a laugh on a park bench", "(min-width: 900px) 38vw, 92vw", (4, 5))}
        </div>
        <div class="prose reveal">
          <h2 id="approach-title">Support that starts with the person</h2>
          <p>Good support begins with understanding. Before anything else, we take the time to learn about your needs, your abilities and how you like to live.</p>
          <p>From there we create a support plan that is tailored to you. As your needs change, we adjust it, so your support always fits where you are now.</p>
          <p>We help with <a href="services.html#health-assistance">health assistance</a>, <a href="services.html#home-care">home care</a>, <a href="services.html#daily-living">daily personal activities</a> and <a href="services.html#community-participation">community participation</a>, at home and around Sydney.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--forest on-dark" aria-labelledby="values-title">
      <div class="wrap split">
        <div class="reveal">
          <h2 id="values-title">What we value</h2>
          <p>Three things shape how we work with every participant, every time.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
        <ul class="values-list reveal">
          <li>
            <h3>{icon("badge")}Experience</h3>
            <p>Support works best when it comes from people who know the work. We bring that experience to every visit, so things feel calm and well organised.</p>
          </li>
          <li>
            <h3>{icon("clock")}Punctuality</h3>
            <p>We turn up on time. If plans need to change, we tell you early and work out a solution with you.</p>
          </li>
          <li>
            <h3>{icon("shield")}Safety</h3>
            <p>Every participant's safety comes first, at home and in the community. We plan carefully and take care at every step.</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="more-title">
      <div class="wrap">
        <h2 id="more-title" class="reveal">More about us, coming soon</h2>
        <div class="placeholder-grid">
          <!-- TODO: team section. Add real names, roles and photos only once the client supplies them, with each person's permission. Do not invent staff or qualifications. -->
          <div class="placeholder reveal">
            <span class="tag">Coming soon</span>
            <h3>Meet the team</h3>
            <p>Photos and short introductions of the people who will support you will appear here.</p>
          </div>
          <!-- TODO: languages spoken. Ask the client which languages the team speaks and list them here. -->
          <div class="placeholder reveal">
            <span class="tag">Coming soon</span>
            <h3>Languages we speak</h3>
            <p>We'll list the languages our team speaks here. In the meantime, just ask us when you call.</p>
          </div>
        </div>
        <div class="cta-row">
          <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
          {or_call()}
        </div>
      </div>
    </section>

    <section class="section section--sand" aria-labelledby="details-title">
      <div class="wrap split">
        <div class="reveal">
          <h2 id="details-title">Business details</h2>
          <p>Here are our official details, for participants, families, plan managers and support coordinators.</p>
          <div class="media-frame reveal-img" style="margin-top:32px">
            {TODO_PHOTO}
            {img("about-park", [700, 1200], "A young man in a wheelchair smiles as a friend blows a dandelion in a park", "(min-width: 900px) 36vw, 92vw", (3, 2))}
          </div>
        </div>
        <div class="facts-card reveal">
          <dl>
            <div><dt>Legal name</dt><dd>{LEGAL}</dd></div>
            <div><dt>ABN</dt><dd>{ABN}</dd></div>
            <!-- TODO: add a row for NDIS registration status / registration number once confirmed. -->
            <div><dt>Address</dt><dd>{STREET}, {SUBURB} {STATE} {POSTCODE}</dd></div>
            <div><dt>Service area</dt><dd>Sydney</dd></div>
            <div><dt>Phone</dt><dd><a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div><dt>Opening hours</dt><dd>{hours_list()}</dd></div>
          </dl>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
          </div>
        </div>
      </div>
    </section>
{cta_band("Let's talk about the support you need", "Call us, send a WhatsApp message or fill in the quote form. We'll take it from there together.")}
  </main>
"""
    return (head("About Care United Group | Disability Support in Auburn, Sydney",
                 "Care United Group is a disability support provider in Auburn, NSW. We assess each person's needs, build a tailored support plan and adjust it as needs change.")
            + header("about.html") + body + footer())


def page_contact():
    body = f"""
  <main id="main">
    <section class="page-hero page-hero--split" aria-labelledby="page-title">
      <div class="wrap">
        <div>
          <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> Contact</p>
          <h1 id="page-title">Contact us or request a quote</h1>
          <p class="lead">Call, send a message or fill in the form below. Tell us what you need, and we'll get back to you to talk it through.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="#quote-form">Go to the quote form {icon("arrow-down")}</a>
            {or_call()}
          </div>
        </div>
        <div class="media-frame reveal-img">
          {TODO_PHOTO}
          {img("contact", [600, 900], "A young man in a wheelchair laughs with a friend standing behind him on a sunny boardwalk", "(min-width: 900px) 38vw, 92vw", (4, 5), eager=True)}
        </div>
      </div>
    </section>

    <section class="section section--sand" aria-labelledby="quote-form-title">
      <div class="wrap quote-grid">
        <div class="sticky">
          <h2>Talk to us directly</h2>
          <p>Prefer to speak to someone? Call or message us during opening hours.</p>
          {contact_options()}
          <dl class="details" style="margin-top:28px">
            <div><dt>{icon("pin")}Address</dt><dd>{STREET}, {SUBURB} {STATE} {POSTCODE}</dd></div>
            <div><dt>{icon("clock")}Opening hours</dt><dd>{hours_list()}</dd></div>
          </dl>
        </div>
        <div class="form-card" id="quote-form-card">
{quote_form("quote-form", full=True)}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="map-title">
      <div class="wrap split">
        <div>
          <h2 id="map-title">Find us in Auburn</h2>
          <p>Our office is at {STREET}, {SUBURB} {STATE} {POSTCODE}. We support participants across Sydney, at home and in the community.</p>
          <p><a class="text-link" href="{MAP_LINK}" target="_blank" rel="noopener"><span>Open in Google Maps<span class="visually-hidden"> (opens in a new tab)</span></span>{icon("arrow")}</a></p>
          <div class="cta-row">
            <a class="btn btn--primary" href="#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
        <div class="map-frame">
          <iframe src="{MAP_EMBED}" title="Map showing {STREET}, {SUBURB} {STATE} {POSTCODE}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </section>
  </main>
"""
    return (head("Request a Quote | NDIS Home Care Auburn & Sydney | Care United Group",
                 "Contact Care United Group in Auburn for NDIS support across Sydney. Call 0405 785 338, message us on WhatsApp or send a quote request online.")
            + header("contact.html") + body + footer())


def page_404():
    # GitHub Pages serves 404.html for any missing path, including nested ones
    # like /repo/a/b. Relative links would then resolve against /repo/a/, so this
    # page alone sets a <base> to the site root, worked out in the browser.
    base = ("<script>(function(){var p=location.pathname.split('/');"
            "if(location.protocol==='file:')return;var root=/\\.github\\.io$/.test(location.hostname)&&p.length>2?'/'+p[1]+'/':'/';"
            "document.write('<base href=\"'+root+'\">');})();</script>\n  ")
    body = f"""
  <main id="main">
    <section class="notfound">
      <div class="wrap split">
        <div>
          <h1>Sorry, we can't find that page</h1>
          <p class="lead">The link may be old, or the address may have a small typo. These pages might help.</p>
          <ul class="links">
            <li><a class="text-link" href="index.html"><span>Home page</span>{icon("arrow")}</a></li>
            <li><a class="text-link" href="services.html"><span>Our services</span>{icon("arrow")}</a></li>
            <li><a class="text-link" href="about.html"><span>About us</span>{icon("arrow")}</a></li>
            <li><a class="text-link" href="contact.html"><span>Contact us</span>{icon("arrow")}</a></li>
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
            {or_call()}
          </div>
        </div>
        <div class="media-frame media-frame--offset">
          {TODO_PHOTO}
          {img("community", [700, 1200], "A group of friends laughing together outdoors in a park", "(min-width: 900px) 52vw, 92vw", (3, 2))}
        </div>
      </div>
    </section>
  </main>
"""
    return (head("Page not found | Care United Group", "Sorry, this page could not be found. Find NDIS support services in Sydney from Care United Group.", extra=base)
            + header("") + body + footer())


PAGES = {
    "index.html": page_home,
    "services.html": page_services,
    "about.html": page_about,
    "contact.html": page_contact,
    "404.html": page_404,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
