#!/usr/bin/env python3
"""Builds the static pages for Care United Group (v2, brand colours).

Edit this file (facts, shared head/header/footer, forms, page bodies), then run:
    python3 _build/build.py
It writes index.html, services.html, about.html, contact.html and 404.html
to the repository root. Every path is relative, so the site works from a
GitHub Pages project subfolder as well as from a custom domain.

Sources for the facts below:
- client brief (contact details, hours, services, process, values)
- the client's current site www.cugndis.com (tagline, process and values wording, images)
- ABN register (legal name CARE UNITED GROUP PTY LTD, ABN active from 31 May 2021)
- NDIS Quality and Safeguards Commission provider register (registration approved,
  13 registration groups), checked 19 November 2026
- the user (they have a wheelchair-accessible van)
"""
import json, re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ facts
BUSINESS = "Care United Group"
LEGAL = "Care United Group Pty Ltd"
SITE = "https://www.cugndis.com.au/"  # live domain since 24 Nov 2026
ABN = "44 650 599 787"
SUBURB = "Auburn"
STATE = "NSW"
POSTCODE = "2144"
PHONE1 = "0440 127 111"
PHONE1_TEL = "+61440127111"
PHONE2 = "0411 394 111"
PHONE2_TEL = "+61411394111"
EMAIL = "cug.ndis@gmail.com"
WA_URL = "https://wa.me/61440127111?text=Hi%2C%20I%27d%20like%20to%20ask%20about%20your%20NDIS%20support%20services"
NDIS_REG_URL = "https://www.ndiscommission.gov.au/provider-registration/care-united-group-pty-ltd"
FORM_ACTION = "https://formspree.io/f/YOUR_FORM_ID"

# key, anchor, name, icon, image, image alt, short copy
SERVICES = [
    ("health", "health-assistance", "Health assistance", "health", "nurse",
     "A smiling support worker in blue scrubs stands behind a young woman in a wheelchair",
     "Staying well takes effort, and you don't have to manage it alone. We help with the health-related parts of your day, in a way that fits your routine, your goals and your NDIS plan."),
    ("home", "home-care", "Home care", "home", "home-care",
     "A support worker hands a glass of water to a woman resting on a sofa at home",
     "Home should feel safe, calm and comfortable. We help with household tasks and keep things running the way you like them, so your energy goes to the things you enjoy."),
    ("daily", "daily-living", "Support with daily personal activities", "sunrise", "daily-living",
     "A woman in a wheelchair prepares breakfast in her kitchen",
     "Personal routines are personal. We help respectfully and at your pace, building on what you can already do, so you keep as much independence as you want."),
    ("community", "community-participation", "Community participation", "people", "community",
     "A group of friends laughing together outdoors in a park",
     "Being part of your community matters. We support you to get out, join in and enjoy community events and activities, with someone you trust beside you."),
]
TRANSPORT_LABEL = "Transport in our wheelchair-accessible van"

# Approved registration groups, exactly as listed on the NDIS Commission register,
# with a plain-English name for each.
REG_GROUPS = [
    ("Assist-Personal Activities", "Assistance with daily personal activities"),
    ("Household Tasks", "Household tasks"),
    ("Participate Community", "Participation in community, social and civic activities"),
    ("Innov Community Participation", "Innovative community participation"),
    ("Group/Centre Activities", "Group and centre-based activities"),
    ("Assist-Travel/Transport", "Assistance with travel and transport arrangements"),
    ("Development-Life Skills", "Development of daily living and life skills"),
    ("Daily Tasks/Shared Living", "Help with daily tasks in shared living"),
    ("Supported Independent Living", "Supported Independent Living (SIL)"),
    ("Accommodation/Tenancy", "Accommodation and tenancy assistance"),
    ("Assist-Life Stage, Transition", "Support through life stages and transitions"),
    ("Assist Access/Maintain Employ", "Help to find and keep a job or study"),
    ("Assistive Prod-Household Task", "Assistive products for household tasks"),
]

# ------------------------------------------------------------------ icons
_I = {
    "phone": '<path d="M5.2 3.8h3.4l1.8 4.6-2.3 1.4a11.5 11.5 0 0 0 6.1 6.1l1.4-2.3 4.6 1.8v3.4a1.9 1.9 0 0 1-2 1.9C10.5 20.2 3.8 13.5 3.3 5.8a1.9 1.9 0 0 1 1.9-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11.4A7 7 0 0 1 19 9.6C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.6"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.2 2"/>',
    "arrow": '<path d="M4.5 12h15M13.5 6l6 6-6 6"/>',
    "arrow-down": '<path d="M12 4.5v15M6 13.5l6 6 6-6"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "check-circle": '<circle cx="12" cy="12" r="8.8"/><path d="m8 12.3 2.7 2.7L16.2 9.4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "health": '<path d="M12 20.2s-7.6-4.6-9-9.6C2 7 4.3 4 7.4 4c2 0 3.5 1.1 4.6 2.7C13.1 5.1 14.6 4 16.6 4c3.1 0 5.4 3 4.4 6.6-1.4 5-9 9.6-9 9.6z"/><path d="M6 11.5h3l1.5-2.5 2.5 5 1.5-2.5h3.5"/>',
    "home": '<path d="M3.5 10.8 12 3.8l8.5 7"/><path d="M5.5 9.3V20h13V9.3"/><path d="M10 20v-5.5h4V20"/>',
    "sunrise": '<path d="M3 18.5h18"/><path d="M6.5 18.5a5.5 5.5 0 0 1 11 0"/><path d="M12 4v3.2M4.6 9.4l2.1 1.8M19.4 9.4l-2.1 1.8M2.8 14.5h2.4M18.8 14.5h2.4"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.4 2.7-6 6-6s6 2.6 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16.2 14.1c2.9.3 4.8 2.7 4.8 5.9"/>',
    "shield": '<path d="M12 3.2 19.5 6v5.6c0 4.4-3.1 8.1-7.5 9.2-4.4-1.1-7.5-4.8-7.5-9.2V6z"/><path d="m8.8 12.2 2.3 2.3 4.3-4.5"/>',
    "badge": '<circle cx="12" cy="9" r="5.4"/><path d="M8.7 13.3 7.4 21l4.6-2.6 4.6 2.6-1.3-7.7"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/>',
    "van": '<path d="M2.8 16.5V8.2a2 2 0 0 1 2-2h9.6l4.4 4.4h.6a2 2 0 0 1 2 2v3.9h-2"/><path d="M14.4 6.2v4.4h4.4"/><path d="M9.3 16.5h5.6"/><circle cx="6.8" cy="17" r="2.2"/><circle cx="17.2" cy="17" r="2.2"/>',
    "wheelchair": '<circle cx="11" cy="4.6" r="1.8"/><path d="M11 7.5v6h5.2l2.3 5"/><path d="M11 10h4.5"/><path d="M8.2 10.6a5.6 5.6 0 1 0 6.9 7.6"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "shop": '<path d="M5 8h14l-1.2 11.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


ARROW = icon("arrow", "arrow")
NEWTAB = '<span class="visually-hidden"> (opens in a new tab)</span>'

WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>')

# name: (widths, stored aspect w/h)
IMAGES = {
    "team": ([800, 1400], (3, 2)), "home-care": ([700, 1200], (4, 3)), "assess": ([700, 1200], (5, 4)),
    "community": ([700, 1200], (4, 3)), "friends-studio": ([600, 1000], (4, 5)), "planning": ([600, 1000], (4, 5)),
    "cafe": ([532], (1, 1)), "drawing": ([326], (4, 3)),
    "van-exterior": ([260], (1, 1)), "van-side": ([260], (1, 1)), "van-lift": ([260], (1, 1)),
    "ndis-people": ([600, 920], (1, 1)), "greeting": ([700, 1200], (3, 2)), "paper-chain": ([700, 1200], (3, 2)),
    "nurse": ([700, 1200], (4, 3)), "park": ([700, 1200], (4, 3)),
    "hero-logo": ([640, 1100], (4, 5)), "health": ([700, 1200], (4, 3)), "daily-living": ([700, 1200], (4, 3)),
    "friends": ([600, 1000], (4, 5)), "bench": ([600, 1000], (4, 5)), "dandelion": ([700, 1200], (3, 2)),
    "boardwalk": ([600, 1000], (4, 5)), "kitchen": ([1000, 1800], (21, 9)),
}

# Images reused from the client's current website, and licence-free stand-ins for the
# five watermarked Adobe Stock previews on that site.
# Photos the client sent us directly (22 Nov 2026, via Messenger).
CLIENT_OWN = {"van-exterior", "van-side", "van-lift", "ndis-people"}
CLIENT_IMAGES = {"team", "home-care", "assess", "community", "friends-studio", "planning", "cafe", "drawing"}
STANDINS = {"greeting": "1238389313", "paper-chain": "1246633814", "nurse": "1499957809", "park": "1548763731"}

# Once the client licenses an Adobe Stock image, _build/swap_adobe.py records it in
# _build/adobe/licensed.json and the page switches to this alt text for it.
ADOBE_ALT = {
    "greeting": "A woman greets a smiling man in a wheelchair in a bright living room",
    "paper-chain": "Cupped hands holding a chain of paper people against a warm sunset",
    "nurse": "A man in a white coat walks beside a smiling woman in a wheelchair outdoors",
    "park": "A carer leans in to chat with a smiling woman in a wheelchair in a sunny park",
}
_REC = pathlib.Path(__file__).resolve().parent / "adobe" / "licensed.json"
LICENSED = json.loads(_REC.read_text()) if _REC.exists() else {}


def img(name, alt, sizes, eager=False):
    widths, (rw, rh) = IMAGES[name]
    srcset = ", ".join(f"images/{name}-{w}.webp {w}w" for w in widths)
    w = widths[-1]
    h = round(w * rh / rw)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if name in LICENSED:
        alt = ADOBE_ALT[name]
        note = f"<!-- Licensed Adobe Stock #{LICENSED[name]} (licence held by the client). -->"
    elif name == "hero-logo":
        note = ("<!-- Made 24 Nov 2026 at the client's request: their logo on a board with cut-out Pexels photos "
                "(#8524618, #6606139, #7294852, free Pexels licence). Source script: _build/hero_logo.py. -->")
    elif name == "ndis-people":
        note = ("<!-- Image supplied by the client. TODO: it shows the NDIA's NDIS logo; check the NDIA brand rules allow a provider to use it, "
                "or swap for the NDIS Commission's registered-provider logo. -->")
    elif name in CLIENT_OWN:
        note = "<!-- The client's own van photo (sent 22 Nov 2026 as a small Messenger image). TODO: ask for the full-size original. -->"
    elif name in STANDINS:
        note = (f"<!-- TODO: licence-free stand-in for the watermarked Adobe Stock #{STANDINS[name]} on the client's current site. "
                f"Replace with the client's own photo, or license that Adobe Stock image. -->")
    elif name in CLIENT_IMAGES:
        note = "<!-- Image from the client's current website (Pexels). TODO: replace with real client photos when available. -->"
    else:
        note = "<!-- TODO: replace with real client photos (stock image used as a placeholder) -->"
    return (f'{note}<img src="images/{name}-{widths[0]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async">')


# ------------------------------------------------------------------ schema
def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": LEGAL,
        "alternateName": BUSINESS,
        "description": "Registered NDIS provider in Auburn, NSW. Health assistance, home care, support with daily personal activities, community participation and transport in a wheelchair-accessible van, across Sydney.",
        "taxID": f"ABN {ABN}",
        "telephone": PHONE1_TEL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": SUBURB,
                    "addressRegion": STATE, "addressCountry": "AU"},
        "areaServed": {"@type": "City", "name": "Sydney"},
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": PHONE1_TEL, "contactType": "customer service", "areaServed": "AU", "availableLanguage": "English"},
            {"@type": "ContactPoint", "telephone": PHONE2_TEL, "contactType": "customer service", "areaServed": "AU", "availableLanguage": "English"},
        ],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "17:00"},
        ],
        "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "Registered NDIS provider",
                          "recognizedBy": {"@type": "GovernmentOrganization", "name": "NDIS Quality and Safeguards Commission"},
                          "url": NDIS_REG_URL},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[2]}} for s in SERVICES]
                      + [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": TRANSPORT_LABEL}}],
    }
    data["url"] = SITE
    data["image"] = SITE + "images/og-image.jpg"
    data["logo"] = SITE + "images/logo-badge-320.webp"
    return ('  <script type="application/ld+json">\n' + json.dumps(data, indent=2) + "\n  </script>")


# ------------------------------------------------------------------ shell
def head(title, desc, extra="", path=None):
    """path: the page's URL path on SITE (\"\" for home). None = not indexable (404)."""
    if path is None:
        meta = '<meta name="robots" content="noindex">'
    else:
        meta = f'<link rel="canonical" href="{SITE}{path}">\n  <meta property="og:url" content="{SITE}{path}">'
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {extra}<title>{title}</title>
  <meta name="description" content="{desc}">
  {meta}
  <meta name="theme-color" content="#5a17a8">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{LEGAL}">
  <meta property="og:locale" content="en_AU">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE}images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="A support worker pouring a drink for a young man in a wheelchair at a kitchen table">
  <meta name="twitter:card" content="summary_large_image">
  <!-- Favicon made from the client's existing logo mark (original colours). -->
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@800;900&amp;family=Figtree:wght@400..700&amp;family=Newsreader:opsz,wght@6..72,400..600&amp;display=swap">
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.className += " js";</script>
  {schema()}
</head>
"""


NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Contact")]

WORDMARK = '<span class="wordmark" aria-hidden="true"><span class="w1">CARE <b>UNITED</b></span><span class="w2">GROUP PTY LTD</span></span>'


def header(current):
    cur = ' aria-current="page"'
    links = "\n".join(f'          <li><a href="{h}"{cur if h == current else ""}>{l}</a></li>' for h, l in NAV)
    return f"""<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <!-- TODO: the brief and the client's current homepage say "Care Unitrd Group"; the ABN register (ABN {ABN}) and the NDIS Commission register both say CARE UNITED GROUP PTY LTD, so this site uses "United". Confirm spelling with client. -->
  <div class="utility on-dark">
    <div class="wrap">
      <a class="reg" href="{NDIS_REG_URL}" target="_blank" rel="noopener">{icon("shield")}Registered NDIS provider{NEWTAB}</a>
      <span>Based in {SUBURB}, Sydney</span>
      <span>Mon to Fri 9am to 7pm, Sat 9am to 5pm</span>
      <a class="spacer" href="tel:{PHONE2_TEL}">{icon("phone")}{PHONE2}</a>
      <a href="{WA_URL}" target="_blank" rel="noopener">{icon("check-circle")}WhatsApp{NEWTAB}</a>
    </div>
  </div>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="{LEGAL}, home">
        <img src="images/logo-badge-160.webp" alt="" width="60" height="60">
        {WORDMARK}
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
{links}
        </ul>
        <div class="nav-extra">
          <a class="btn btn--primary" href="contact.html#quote-form">Request a quote</a>
          <a class="btn btn--outline" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
          <a class="btn btn--outline" href="tel:{PHONE2_TEL}">{icon("phone")}Call {PHONE2}</a>
          <p class="nav-reg">{icon("shield")}Registered NDIS provider, Auburn NSW</p>
        </div>
      </nav>
      <a class="header-phone" href="tel:{PHONE1_TEL}"><span class="ph-ico">{icon("phone")}</span><span><span class="visually-hidden">Call us on </span>{PHONE1}</span></a>
      <a class="btn btn--primary header-quote" href="contact.html#quote-form"><span class="q-long">Request a quote</span><span class="q-short">Get a quote</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        {icon("menu", "icon-menu")}{icon("close", "icon-close")}
      </button>
    </div>
  </header>
"""


def or_call():
    return f'<span class="or">or call <a href="tel:{PHONE1_TEL}">{PHONE1}</a></span>'


def cta_card(title, text, image, alt, top=False):
    return f"""
    <section class="cta-band{' cta-band--top' if top else ''}" aria-labelledby="cta-title">
      <div class="wrap">
        <div class="cta-card on-dark">
          <div class="body reveal">
            <h2 id="cta-title">{title}</h2>
            <p>{text}</p>
            <div class="cta-row">
              <a class="btn btn--light" href="contact.html#quote-form">Request a quote {ARROW}</a>
              <a class="btn btn--outline" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
            </div>
          </div>
          <div class="media">{img(image, alt, "(min-width: 900px) 46vw, 100vw")}</div>
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
          <a class="footer-brand" href="index.html" aria-label="{LEGAL}, home"><span class="disc"><img src="images/logo-badge-160.webp" alt="" width="68" height="68" loading="lazy"></span>{WORDMARK}</a>
          <p>Disability support at home and in the community, across Sydney.</p>
          <p class="footer-reg">{icon("shield")}<a href="{NDIS_REG_URL}" target="_blank" rel="noopener">Registered NDIS provider{NEWTAB}</a></p>
          <p>{LEGAL}<br>ABN {ABN}</p>
          <p>Based in {SUBURB}, supporting people across Sydney</p>
          <div class="footer-cta"><a class="btn btn--light" href="contact.html#quote-form">Request a quote</a></div>
        </div>
        <div>
          <h2>Contact</h2>
          <ul>
            <li><a href="tel:{PHONE1_TEL}">{PHONE1}</a></li>
            <li><a href="tel:{PHONE2_TEL}">{PHONE2}</a></li>
            <li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp {PHONE1}{NEWTAB}</a></li>
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
            <li><a href="services.html#transport">Wheelchair-accessible transport</a></li>
            <li><a href="services.html#supports">All approved NDIS supports</a></li>
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
    service_names = [s[2] for s in SERVICES] + [TRANSPORT_LABEL]
    boxes = "\n".join(
        f'                <label class="choice"><input type="checkbox" name="services" value="{n}"{f" id={chr(34)}{fid}-services{chr(34)}" if i == 0 else ""}> <span>{n}</span></label>'
        for i, n in enumerate(service_names))

    def radios(name, legend, options):
        opts = "\n".join(f'                <label class="choice"><input type="radio" name="{name}" value="{o}"> <span>{o}</span></label>' for o in options)
        return f'''            <fieldset class="field">
              <legend>{legend}</legend>
              <div class="choices choices--2">
{opts}
              </div>
            </fieldset>'''

    hx = "h2" if full else "h3"
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
    plan = radios("plan_management", "How is the NDIS plan managed?", ["Self-managed", "Plan-managed", "NDIA-managed", "Not sure"]) if full else ""
    return f'''
          <div class="form-head">
            <{hx} id="{fid}-title">Request a quote</{hx}>
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
            <div class="form-grid form-grid--2">
              <div class="field" data-field="email">
                <label for="{fid}-email">Email</label>
                <input type="email" id="{fid}-email" name="email" autocomplete="email" inputmode="email" aria-describedby="{fid}-email-error">
                <p class="error-msg" id="{fid}-email-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="{fid}-suburb">Suburb</label>
                <input type="text" id="{fid}-suburb" name="suburb" autocomplete="address-level2">
              </div>
            </div>
{who}
            <fieldset class="field" data-field="services" aria-describedby="{fid}-services-error">
              <legend>Which services are you interested in? <abbr title="required">*</abbr></legend>
              <p class="hint">Choose as many as you like.</p>
              <div class="choices choices--2">
{boxes}
              </div>
              <p class="error-msg" id="{fid}-services-error" aria-live="polite"></p>
            </fieldset>
{plan}
{radios("contact_method", "How would you like us to contact you?", ["Phone", "WhatsApp", "Email"])}
            <div class="field">
              <label for="{fid}-message">{"Tell us about the support you need" if full else "Anything you'd like us to know?"}</label>
              <p class="hint" id="{fid}-message-hint">For example, which days suit you, or what matters most to you. Please don't include detailed medical information.</p>
              <textarea id="{fid}-message" name="message" rows="{5 if full else 3}" aria-describedby="{fid}-message-hint"></textarea>
            </div>
            <div class="field" data-field="consent">
              <label class="consent" for="{fid}-consent"><input type="checkbox" id="{fid}-consent" name="consent" value="Yes" required aria-required="true" aria-describedby="{fid}-consent-error"> <span>I agree to Care United Group contacting me about my enquiry. <abbr title="required">*</abbr></span></label>
              <p class="error-msg" id="{fid}-consent-error" aria-live="polite"></p>
            </div>
            <div class="form-actions">
              <button class="btn btn--primary" type="submit"><span>Send my request</span> {ARROW}</button>
              <p class="form-fine">Prefer to talk? Call <a href="tel:{PHONE1_TEL}">{PHONE1}</a>.</p>
            </div>
            <p class="form-error-send" tabindex="-1" role="alert">Sorry, your request didn't send. Please try again, or call us on <a href="tel:{PHONE1_TEL}">{PHONE1}</a>.</p>
            </div>
          </form>
          <div class="form-success" tabindex="-1" role="status" aria-live="polite">
            <div class="tick">{icon("check")}</div>
            <{hx}>Thank you, we've got your request</{hx}>
            <p>We'll be in touch soon using the contact method you chose. If it's urgent, please call us on <a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a>.</p>
          </div>'''


def contact_options():
    return f'''<ul class="contact-options">
            <li><a href="tel:{PHONE1_TEL}"><span class="c-ico">{icon("phone")}</span><span><strong>{PHONE1}</strong><span class="sub">Call us</span></span></a></li>
            <li><a href="tel:{PHONE2_TEL}"><span class="c-ico">{icon("phone")}</span><span><strong>{PHONE2}</strong><span class="sub">Our second line</span></span></a></li>
            <li><a class="wa" href="{WA_URL}" target="_blank" rel="noopener"><span class="c-ico">{WA_SVG}</span><span><strong>WhatsApp</strong><span class="sub">Send us a message{NEWTAB}</span></span></a></li>
            <li><a href="mailto:{EMAIL}"><span class="c-ico">{icon("mail")}</span><span><strong>{EMAIL}</strong><span class="sub">Email us</span></span></a></li>
          </ul>'''


def hours_list():
    return '''<ul class="hours">
                  <li><span>Monday to Friday</span><span>9am to 7pm</span></li>
                  <li><span>Saturday</span><span>9am to 5pm</span></li>
                  <li><span>Sunday</span><span>Closed</span></li>
                </ul>'''


def steps_html(short=False):
    if short:
        items = [("We assess your needs", "A conversation about your needs, your capabilities and what you'd like help with."),
                 ("We create a tailored plan", "A plan designed around you, your routine and your NDIS plan."),
                 ("We adapt and refine it", "We review your support and adjust it whenever your needs change.")]
    else:
        items = [("We assess your needs", "We take the time to understand your needs, your capabilities, and your mental and physical abilities. Your family or support coordinator can be part of it if you like."),
                 ("We create a tailored plan", "Together we build a plan designed to make a real, positive difference: the support you'll get, when you'll get it, and how it fits your NDIS plan."),
                 ("We adapt and refine it", "Life changes, and your support should too. We adjust your plan as your needs change, so you always get the right support.")]
    li = "\n".join(f"            <li><h3>{h}</h3><p>{p}</p></li>" for h, p in items)
    return f'<ol class="steps">\n{li}\n          </ol>'


VALUES = [
    ("badge", "Experience", "You deserve support from people who know the work. Experience means calmer days and more confidence, for you and your family."),
    ("clock", "Punctuality", "We turn up when we say we will. If something changes, we tell you early. Your time matters."),
    ("spark", "Modern methods", "We use modern, practical ways of working, so your support is organised, consistent and easy to follow."),
    ("shield", "Safety and security", "High safety and security standards for every participant, at home and out in the community."),
]


def values_html():
    return "\n".join(f'''            <div class="reveal{' reveal-d1' if i % 2 else ''}">
              <div class="v-ico">{icon(ic)}</div>
              <h3>{t}</h3>
              <p>{p}</p>
            </div>''' for i, (ic, t, p) in enumerate(VALUES))


def supports_html():
    li = "\n".join(f'          <li>{icon("check-circle")}<span>{plain}</span></li>' for _, plain in REG_GROUPS)
    return f'<ul class="supports">\n{li}\n        </ul>'


# ------------------------------------------------------------------ pages
def page_home():
    tabs = "\n".join(
        f'''          <button class="svc-tab" type="button" id="tab-{s[0]}" data-tab><span class="t-ico">{icon(s[3])}</span>{s[2]}</button>'''
        for s in SERVICES)
    panels = "\n".join(f'''          <article class="svc-panel" id="panel-{s[0]}" data-panel>
            <div class="media">{img(s[4], s[5], "(min-width: 900px) 34vw, 92vw")}</div>
            <div class="body">
              <div class="svc-ico">{icon(s[3])}</div>
              <h3>{s[2]}</h3>
              <p>{s[6]}</p>
              <div class="cta-row">
                <a class="btn btn--primary" href="contact.html?service={s[0]}#quote-form">Ask about this service {ARROW}</a>
                <a class="text-link" href="services.html#{s[1]}"><span>Learn more</span>{icon("arrow")}</a>
              </div>
            </div>
          </article>''' for s in SERVICES)

    gallery = [
        ("g1", "park", "A support worker points something out to a young man in a wheelchair in a leafy park", "(min-width: 1100px) 32vw, (min-width: 900px) 46vw, 92vw"),
        ("g2", "cafe", "Friends, two of them in wheelchairs, chatting over drinks at an outdoor cafe table", "(min-width: 1100px) 32vw, (min-width: 900px) 24vw, 46vw"),
        ("g3", "friends-studio", "A woman in a wheelchair with two friends standing beside her", "(min-width: 1100px) 16vw, (min-width: 900px) 24vw, 46vw"),
        ("g4", "drawing", "Children and adults colouring pictures together at a table", "(min-width: 900px) 16vw, 46vw"),
        ("g5", "dandelion", "A young man in a wheelchair smiles as a friend blows a dandelion", "(min-width: 1100px) 16vw, 46vw"),
        ("g6", "boardwalk", "A young man in a wheelchair laughs with a friend on a sunny boardwalk", "(min-width: 1100px) 16vw, 92vw"),
    ]
    gal = "\n".join(f'          <li class="{c} veil">{img(n, a, s)}</li>' for c, n, a, s in gallery)

    body = f"""
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <div class="hero-copy">
          <a class="verified hero-in" href="{NDIS_REG_URL}" target="_blank" rel="noopener"><span class="dot">{icon("shield")}</span>Registered NDIS provider{NEWTAB}</a>
          <h1 id="hero-title" class="hero-in d1">We're here for <span class="accent">every step</span> of your NDIS journey</h1>
          <p class="lead hero-in d2">Care United Group is a registered NDIS provider based in Auburn. We support people with disability across Sydney, at home and in the community, with our own wheelchair-accessible van to help you get there.</p>
          <div class="cta-row hero-in d3">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            <a class="btn btn--outline" href="tel:{PHONE1_TEL}">{icon("phone")}Call {PHONE1}</a>
          </div>
          <ul class="hero-facts hero-in d4">
            <li><span class="ico">{icon("shield")}</span><span>NDIS registered<small>Approved by the NDIS Commission</small></span></li>
            <li><span class="ico">{icon("van")}</span><span>Accessible van<small>Getting there, made easier</small></span></li>
            <li><span class="ico">{icon("clock")}</span><span>Open six days<small>Monday to Saturday</small></span></li>
          </ul>
        </div>
        <div class="hero-visual">
          <div class="hero-main veil">{img("hero-logo", "The Care United Group logo on a board, with three smiling people in front: a young woman in a wheelchair, an older man with a white cane and a man in a wheelchair", "(min-width: 900px) 40vw, 80vw", eager=True)}</div>
          <p class="hero-tag"><strong>13 supports</strong>approved on the NDIS Commission register</p>
        </div>
      </div>
    </section>

    <section class="reg-band on-dark" aria-labelledby="reg-title">
      <div class="wrap">
        <div class="seal">{icon("shield")}</div>
        <div>
          <h2 id="reg-title">A registered NDIS provider you can check</h2>
          <p>Care United Group Pty Ltd is approved by the NDIS Quality and Safeguards Commission for 13 registration groups, from daily personal activities to Supported Independent Living.</p>
        </div>
        <div class="links">
          <a class="text-link" href="{NDIS_REG_URL}" target="_blank" rel="noopener"><span>View us on the NDIS register{NEWTAB}</span>{icon("external")}</a>
          <a class="text-link" href="services.html#supports"><span>See every approved support</span>{icon("arrow")}</a>
        </div>
      </div>
    </section>

    <section class="section section--lilac" aria-labelledby="services-title">
      <div class="wrap">
        <div class="section-head section-head--split reveal">
          <h2 id="services-title">Support for everyday life, shaped around you</h2>
          <p>Four core services. Choose one, or combine them in a single plan. Not sure what you need yet? Tell us what a normal week looks like, and we'll help you work it out.</p>
        </div>
        <div class="svc-showcase" data-tabs>
          <div class="svc-tablist" aria-label="Our services">
{tabs}
          </div>
          <div class="svc-panels">
{panels}
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="van-title">
      <div class="wrap van">
        <div class="van-media">
          <div class="van-photos">
            <figure class="veil">{img("van-exterior", "The back of our white Toyota HiAce Commuter van, with a wheelchair access sign on the rear window", "(min-width: 900px) 17vw, 30vw")}<figcaption>Our van</figcaption></figure>
            <figure class="veil">{img("van-side", "Inside our van through the side door: grab rails, a non-slip step and rows of seats", "(min-width: 900px) 17vw, 30vw")}<figcaption>Side entry</figcaption></figure>
            <figure class="veil">{img("van-lift", "The rear doors of our van open to show the wheelchair lift", "(min-width: 900px) 17vw, 30vw")}<figcaption>Wheelchair lift</figcaption></figure>
          </div>
          <p class="van-badge"><span class="b-ico">{icon("check-circle")}</span>Travel and transport is one of our approved NDIS supports</p>
        </div>
        <div class="reveal">
          <h2 id="van-title">Our own wheelchair-accessible van</h2>
          <p class="lead">Getting there is part of the support. Our wheelchair-accessible van makes it easier to reach the places that matter to you.</p>
          <!-- TODO: confirm with the client how the van is used. -->
          <ul class="van-list">
            <li>{icon("calendar")}<span><strong>Appointments</strong><span class="sub">Help getting to and from your appointments.</span></span></li>
            <li>{icon("people")}<span><strong>Community events and activities</strong><span class="sub">Join in without worrying about how you'll get there.</span></span></li>
            <li>{icon("shop")}<span><strong>Everyday outings</strong><span class="sub">Errands, visits and the outings you enjoy.</span></span></li>
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html?service=transport#quote-form">Ask about transport {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="how-title">
      <div class="wrap process">
        <div class="process-media">
          <div class="a veil">{img("assess", "A support worker with a clipboard listens to a woman during a conversation at home", "(min-width: 900px) 38vw, 76vw")}</div>
          <div class="b veil">{img("planning", "Hands arranging photos and notes on a table while planning", "(min-width: 900px) 18vw, 40vw")}</div>
        </div>
        <div class="reveal">
          <h2 id="how-title">A personal plan, built properly</h2>
          <p>Every participant gets a personalised experience. Here is how it works.</p>
          {steps_html()}
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Start with a conversation {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark on-dark" aria-labelledby="values-title">
      <div class="wrap values">
        <div class="values-photo">
          <div class="frame veil">{img("friends", "Four friends, one of them in a wheelchair, smiling together on a sunny waterfront boardwalk", "(min-width: 900px) 36vw, 92vw")}</div>
          <div class="chain veil">{img("paper-chain", "A woman holds up a chain of pink paper people", "(min-width: 900px) 18vw, 46vw")}</div>
        </div>
        <div>
          <h2 id="values-title" class="reveal">What sets us apart</h2>
          <p class="lead reveal">The standards we hold ourselves to, with every participant, every day.</p>
          <div class="value-grid">
{values_html()}
          </div>
          <div class="cta-row reveal">
            <a class="btn btn--light" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="who-title">
      <div class="wrap audience-wrap">
        <div>
          <h2 id="who-title" class="reveal">Whoever is reaching out, we're glad you did</h2>
          <p class="lead reveal">You might be looking for support for yourself, for someone you love, or for a participant you work with.</p>
          <div class="audience reveal">
            <div><h3>Participants</h3><p>Tell us what you'd like help with and what matters to you. We'll explain your options in plain English, and you stay in charge of your support.</p></div>
            <div><h3>Families and carers</h3><p>Looking for support for someone you care about? We'll work with you as part of their team, with their consent.</p></div>
            <div><h3>Support coordinators</h3><p>Send us an enquiry with the participant's needs and suburb, and we'll come back to you with what we can offer.</p></div>
          </div>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Send an enquiry {ARROW}</a>
            {or_call()}
          </div>
        </div>
        <div class="audience-photo">
          <div class="frame veil">{img("greeting", "A support worker brings a cup to a smiling young man in a wheelchair working on a laptop at home", "(min-width: 900px) 44vw, 92vw")}</div>
        </div>
      </div>
    </section>

    <section class="section section--cream" aria-labelledby="gallery-title">
      <div class="wrap">
        <div class="section-head section-head--split reveal">
          <h2 id="gallery-title">At home, out and about, and everything in between</h2>
          <p>Support that fits into everyday life: a coffee with friends, a walk in the park, an afternoon doing the things you love.</p>
        </div>
        <ul class="gallery">
{gal}
        </ul>
        <div class="cta-row">
          <a class="btn btn--primary" href="services.html">Explore our services {ARROW}</a>
          {or_call()}
        </div>
      </div>
    </section>

    <!-- TODO: participant and family feedback. Add real quotes only, with written permission from each person. Never invent names, quotes or star ratings. (The quote from "Oliver Hartman" on the current site is website-template placeholder text, so it is not used.) Remove this block once real feedback is added. -->
    <section class="section section--tight" aria-labelledby="feedback-title">
      <div class="wrap">
        <div class="placeholder reveal">
          <span class="tag">Coming soon</span>
          <h2 id="feedback-title">In their own words</h2>
          <p>We'll share feedback from participants and families here, with their permission.</p>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="area-title">
      <div class="wrap area">
        <div class="area-media">
          <div class="frame tall veil">{img("bench", "A woman in a wheelchair and a friend share a laugh on a park bench", "(min-width: 900px) 24vw, 50vw")}</div>
          <div class="stack">
            <div class="frame veil">{img("health", "A support worker checks a woman's blood pressure at home", "(min-width: 900px) 20vw, 42vw")}</div>
            <div class="frame veil">{img("team", "A group of smiling people standing together in a bright office", "(min-width: 900px) 20vw, 42vw")}</div>
          </div>
        </div>
        <div class="reveal">
          <h2 id="area-title">Based in Auburn, supporting people across Sydney</h2>
          <p>We're based in {SUBURB} and support participants across Sydney, at home and out in the community. Not sure if we cover your suburb? Just ask.</p>
          <!-- TODO: list the suburbs or regions the client confirms they cover. Do not add areas until confirmed. -->
          <dl class="details">
            <div><dt>{icon("pin")}Based in</dt><dd>{SUBURB}, Sydney {STATE}</dd></div>
            <div><dt>{icon("clock")}Opening hours</dt><dd>{hours_list()}</dd></div>
            <div><dt>{icon("phone")}Phone</dt><dd><a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a></dd></div>
          </dl>
          <div class="cta-row">
            <a class="btn btn--primary" href="#quote">Ask if we cover your area {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--lilac" id="quote" aria-labelledby="quote-title">
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
    return (head("Registered NDIS Provider Sydney | Care United Group, Auburn",
                 "Registered NDIS provider in Auburn supporting people across Sydney: health assistance, home care, daily personal activities, community participation and a wheelchair-accessible van.", path="")
            + header("index.html") + body + footer())


SERVICE_DETAIL = {
    "health": {"inset": ("health", "A support worker checks a woman's blood pressure at home"),
               "list": ["Support to keep up the health routines that are part of your plan",
                        "Help getting ready for, and getting to, your appointments",
                        "Keeping your family or support team in the loop, with your permission"]},
    "home": {"inset": ("greeting", "A support worker brings a cup to a young man in a wheelchair at home"),
             "list": ["Household tasks around your home",
                      "Keeping your space safe, tidy and easy to move around",
                      "Support that follows your routine and the way you like things done"]},
    "daily": {"inset": None,
              "list": ["Help with personal routines, such as getting ready for the day",
                       "Support at the times of day that suit you",
                       "Care that respects your privacy, dignity and choices"]},
    "community": {"inset": ("cafe", "Friends, two of them in wheelchairs, chatting at an outdoor cafe"),
                  "list": ["Community events, groups and activities",
                           "Trying a new interest, or getting back to an old one",
                           "Building confidence when you're out and about"]},
}


def page_services():
    jump_items = [(s[1], s[3], s[2]) for s in SERVICES] + [("transport", "van", "Wheelchair-accessible transport"), ("supports", "check-circle", "All approved NDIS supports")]
    jump = "\n".join(f'            <li><a href="#{a}">{icon(ic, "ico")}{t}{icon("arrow-down", "arrow")}</a></li>' for a, ic, t in jump_items)
    blocks = []
    for i, s in enumerate(SERVICES):
        d = SERVICE_DETAIL[s[0]]
        ticks = "\n".join(f'              <li>{icon("check")}<span>{t}</span></li>' for t in d["list"])
        sec = "section section--white" if i % 2 else "section"
        flip = " service-block--flip" if i % 2 else ""
        inset = f'<div class="inset veil">{img(d["inset"][0], d["inset"][1], "(min-width: 900px) 18vw, 38vw")}</div>' if d["inset"] else ""
        blocks.append(f"""
    <section class="{sec}" id="{s[1]}" aria-labelledby="{s[1]}-title">
      <div class="wrap service-block{flip}">
        <div class="reveal">
          <div class="s-ico">{icon(s[3])}</div>
          <h2 id="{s[1]}-title">{s[2]}</h2>
          <p class="lead">{s[6]}</p>
          <p class="ticks-title">This can include:</p>
          <!-- TODO: confirm these examples with the client before launch. -->
          <ul class="ticks">
{ticks}
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html?service={s[0]}#quote-form">Ask about this service {ARROW}</a>
            {or_call()}
          </div>
        </div>
        <div class="media">
          <div class="frame veil">{img(s[4], s[5], "(min-width: 900px) 42vw, 92vw")}</div>
          {inset}
        </div>
      </div>
    </section>""")

    body = f"""
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <div>
          <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> Services</p>
          <h1 id="page-title" class="hero-in">NDIS support services in Sydney</h1>
          <p class="lead hero-in d1">As a registered NDIS provider, we offer four core services for participants across Sydney, plus transport in our own wheelchair-accessible van. Each one is tailored to the person, and you can combine them in one plan.</p>
          <div class="cta-row hero-in d2">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
        <nav class="hero-in d3" aria-label="On this page">
          <ul class="jump">
{jump}
          </ul>
        </nav>
      </div>
    </section>

    <div class="wrap wide-photo">
      <div class="frame veil">{img("kitchen", "A support worker and a young woman help an older woman in a wheelchair prepare vegetables at the kitchen table", "(min-width: 1280px) 1168px, 92vw")}</div>
    </div>
{"".join(blocks)}

    <section class="section section--lilac" id="transport" aria-labelledby="transport-title">
      <div class="wrap van">
        <div class="van-media">
          <div class="van-photos">
            <figure class="veil">{img("van-exterior", "The back of our white Toyota HiAce Commuter van, with a wheelchair access sign on the rear window", "(min-width: 900px) 17vw, 30vw")}<figcaption>Our van</figcaption></figure>
            <figure class="veil">{img("van-side", "Inside our van through the side door: grab rails, a non-slip step and rows of seats", "(min-width: 900px) 17vw, 30vw")}<figcaption>Side entry</figcaption></figure>
            <figure class="veil">{img("van-lift", "The rear doors of our van open to show the wheelchair lift", "(min-width: 900px) 17vw, 30vw")}<figcaption>Wheelchair lift</figcaption></figure>
          </div>
          <p class="van-badge"><span class="b-ico">{icon("check-circle")}</span>Assistance with travel and transport arrangements: NDIS approved</p>
        </div>
        <div class="reveal">
          <div class="s-ico" style="width:60px;height:60px;border-radius:50%;display:grid;place-items:center;background:var(--plum);color:#fff;margin-bottom:22px">{icon("van")}</div>
          <h2 id="transport-title">Wheelchair-accessible transport</h2>
          <p class="lead">We have our own wheelchair-accessible van, so getting to appointments, outings and community activities is simpler and safer.</p>
          <!-- TODO: confirm with the client how the van is used. -->
          <ul class="ticks">
            <li>{icon("check")}<span>Help getting to and from appointments</span></li>
            <li>{icon("check")}<span>Getting to community events, groups and activities</span></li>
            <li>{icon("check")}<span>Everyday outings, errands and visits</span></li>
          </ul>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html?service=transport#quote-form">Ask about transport {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="supports" aria-labelledby="supports-title">
      <div class="wrap">
        <div class="section-head section-head--split reveal">
          <h2 id="supports-title">Every support we're approved to provide</h2>
          <p>Care United Group Pty Ltd is approved by the NDIS Quality and Safeguards Commission for these 13 registration groups. If your plan includes any of them, ask us how we can help.</p>
        </div>
        <div class="reveal">
        {supports_html()}
        </div>
        <p class="source-note">Source: <a href="{NDIS_REG_URL}" target="_blank" rel="noopener">NDIS Quality and Safeguards Commission provider register{NEWTAB}</a>. Names simplified into plain English.</p>
        <div class="cta-row">
          <a class="btn btn--primary" href="contact.html#quote-form">Ask about a support {ARROW}</a>
          {or_call()}
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="start-title">
      <div class="wrap process">
        <div class="process-media">
          <div class="a veil">{img("assess", "A support worker with a clipboard listens to a woman during a conversation at home", "(min-width: 900px) 38vw, 76vw")}</div>
          <div class="b veil">{img("planning", "Hands arranging photos and notes on a table while planning", "(min-width: 900px) 18vw, 40vw")}</div>
        </div>
        <div class="reveal">
          <h2 id="start-title">Every service starts the same way</h2>
          <p>Whichever support you choose, we begin by understanding you.</p>
          {steps_html(short=True)}
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>
{cta_card("Not sure which support you need?", "Tell us about your week and what you'd like help with. We'll suggest options that fit you.", "dandelion", "A young man in a wheelchair smiles as a friend blows a dandelion in a park", top=True)}
  </main>
"""
    return (head("NDIS Home Care & Disability Support Services Sydney | Care United Group",
                 "Health assistance, home care, daily personal activities, community participation and wheelchair-accessible transport from a registered NDIS provider in Auburn, Sydney.", path="services")
            + header("services.html") + body + footer())


def page_about():
    body = f"""
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <div>
          <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> About</p>
          <h1 id="page-title" class="hero-in">About Care United Group</h1>
          <p class="lead hero-in d1">A registered NDIS provider based in Auburn, supporting people with disability and their families across Sydney.</p>
          <div class="cta-row hero-in d2">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
        <div class="ph-media hero-in d2"><div class="frame">{img("bench", "A woman in a wheelchair and a friend share a laugh on a park bench", "(min-width: 900px) 40vw, 92vw", eager=True)}</div></div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="story-title">
      <div class="wrap story">
        <div class="story-media">
          <div class="frame wide veil">{img("team", "A group of smiling people standing together in a bright office", "(min-width: 900px) 42vw, 92vw")}</div>
          <div class="frame sq veil">{img("cafe", "Friends, two of them in wheelchairs, chatting over drinks at an outdoor cafe", "(min-width: 900px) 20vw, 45vw")}</div>
          <div class="frame sq veil">{img("drawing", "Children and adults colouring pictures together at a table", "(min-width: 900px) 20vw, 45vw")}</div>
        </div>
        <div class="reveal">
          <h2 id="story-title">Our story</h2>
          <p>Care United Group is a team dedicated to reliable, high-quality disability support. We grew from modest beginnings, and every step has strengthened what we believe in: working together, acting with integrity, and real respect for the people we support.</p>
          <p>Our approach is simple. We start by understanding your needs, then we provide practical support, from a first conversation to hands-on help every day.</p>
          <p>We help with <a href="services.html#health-assistance">health assistance</a>, <a href="services.html#home-care">home care</a>, <a href="services.html#daily-living">daily personal activities</a> and <a href="services.html#community-participation">community participation</a>, and our own <a href="services.html#transport">wheelchair-accessible van</a> helps people get where they need to go.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark on-dark" aria-labelledby="values-title">
      <div class="wrap values">
        <div class="values-photo">
          <div class="frame veil">{img("friends", "Four friends, one of them in a wheelchair, smiling together on a sunny boardwalk", "(min-width: 900px) 36vw, 92vw")}</div>
          <div class="chain veil">{img("paper-chain", "A woman holds up a chain of pink paper people", "(min-width: 900px) 18vw, 46vw")}</div>
        </div>
        <div>
          <h2 id="values-title" class="reveal">What we value</h2>
          <p class="lead reveal">Four things shape how we work with every participant, every time.</p>
          <div class="value-grid">
{values_html()}
          </div>
          <div class="cta-row reveal">
            <a class="btn btn--light" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--lilac" aria-labelledby="details-title">
      <div class="wrap split">
        <div class="sticky reveal">
          <h2 id="details-title">Registration and business details</h2>
          <p>Our official details, for participants, families, plan managers and support coordinators. You can check our NDIS registration on the Commission's public register.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="{NDIS_REG_URL}" target="_blank" rel="noopener">Check our registration{NEWTAB} {icon("external")}</a>
          </div>
        </div>
        <div class="facts-card reveal">
          <dl>
            <div><dt>Legal name</dt><dd>{LEGAL}</dd></div>
            <div><dt>NDIS registration</dt><dd><span class="ok">{icon("check-circle")}Approved</span> by the NDIS Quality and Safeguards Commission</dd></div>
            <!-- TODO: the public register shows no registration number. Add it here if the client wants it shown. -->
            <div><dt>Registration groups</dt><dd><a href="services.html#supports">13 approved registration groups</a></dd></div>
            <div><dt>ABN</dt><dd>{ABN} (active since May 2021)</dd></div>
            <div><dt>Based in</dt><dd>{SUBURB}, {STATE}</dd></div>
            <div><dt>Service area</dt><dd>Sydney</dd></div>
            <div><dt>Transport</dt><dd>Our own wheelchair-accessible van</dd></div>
            <div><dt>Phone</dt><dd><a href="tel:{PHONE1_TEL}">{PHONE1}</a> or <a href="tel:{PHONE2_TEL}">{PHONE2}</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div><dt>Opening hours</dt><dd>{hours_list()}</dd></div>
          </dl>
        </div>
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
      </div>
    </section>
{cta_card("Let's talk about the support you need", "Call us, send a WhatsApp message or fill in the quote form. We'll take it from there together.", "greeting", "A support worker brings a cup to a smiling young man in a wheelchair at home")}
  </main>
"""
    return (head("About Care United Group | Registered NDIS Provider in Auburn, Sydney",
                 "Care United Group is a registered NDIS provider in Auburn, NSW. We assess each person's needs, build a tailored support plan and adapt it as needs change.", path="about")
            + header("about.html") + body + footer())


def page_contact():
    body = f"""
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <div>
          <p class="crumbs"><a href="index.html">Home</a> <span aria-hidden="true">/</span> Contact</p>
          <h1 id="page-title" class="hero-in">Contact us or request a quote</h1>
          <p class="lead hero-in d1">Call, send a message or fill in the form below. Tell us what you need, and we'll get back to you to talk it through.</p>
          <div class="cta-row hero-in d2">
            <a class="btn btn--primary" href="#quote-form">Go to the quote form {icon("arrow-down")}</a>
            {or_call()}
          </div>
        </div>
        <div class="ph-media ph-media--cutout hero-in d2">{img("ndis-people", "Four smiling NDIS participants, two using wheelchairs and one with a white cane, in front of a large NDIS logo", "(min-width: 900px) 40vw, 92vw", eager=True)}</div>
      </div>
    </section>

    <section class="section section--lilac" aria-labelledby="quote-form-title">
      <div class="wrap quote-grid">
        <div class="sticky">
          <h2>Talk to us directly</h2>
          <p>Prefer to speak to someone? Call or message us during opening hours.</p>
          {contact_options()}
          <dl class="details" style="margin-top:28px">
            <div><dt>{icon("pin")}Based in</dt><dd>{SUBURB}, Sydney {STATE}</dd></div>
            <div><dt>{icon("clock")}Opening hours</dt><dd>{hours_list()}</dd></div>
            <div><dt>{icon("shield")}NDIS registration</dt><dd><a href="{NDIS_REG_URL}" target="_blank" rel="noopener">Approved, view on the register{NEWTAB}</a></dd></div>
          </dl>
        </div>
        <div class="form-card">
{quote_form("quote-form", full=True)}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="area-title">
      <div class="wrap van">
        <div class="van-media">
          <div class="van-photos">
            <figure class="veil">{img("van-exterior", "The back of our white Toyota HiAce Commuter van, with a wheelchair access sign on the rear window", "(min-width: 900px) 17vw, 30vw")}<figcaption>Our van</figcaption></figure>
            <figure class="veil">{img("van-side", "Inside our van through the side door: grab rails, a non-slip step and rows of seats", "(min-width: 900px) 17vw, 30vw")}<figcaption>Side entry</figcaption></figure>
            <figure class="veil">{img("van-lift", "The rear doors of our van open to show the wheelchair lift", "(min-width: 900px) 17vw, 30vw")}<figcaption>Wheelchair lift</figcaption></figure>
          </div>
        </div>
        <div class="reveal">
          <h2 id="area-title">Across Sydney, at home and in the community</h2>
          <p>We're based in {SUBURB} and come to you, wherever you are in Sydney. Our own wheelchair-accessible van, with a rear wheelchair lift, helps people get where they need to go.</p>
          <div class="cta-row">
            <a class="btn btn--primary" href="#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
      </div>
    </section>
  </main>
"""
    return (head("Request a Quote | NDIS Home Care Auburn & Sydney | Care United Group",
                 "Contact Care United Group, a registered NDIS provider in Auburn. Call 0440 127 111, message us on WhatsApp or send a quote request online.", path="contact")
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
    <section class="page-hero notfound">
      <div class="wrap">
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
            <a class="btn btn--primary" href="contact.html#quote-form">Request a quote {ARROW}</a>
            {or_call()}
          </div>
        </div>
        <div class="ph-media"><div class="frame">{img("community", "A group of friends laughing together outdoors in a park", "(min-width: 900px) 40vw, 92vw")}</div></div>
      </div>
    </section>
  </main>
"""
    return (head("Page not found | Care United Group", "Sorry, this page could not be found. Find NDIS support services in Sydney from Care United Group.", extra=base)
            + header("") + body + footer())


PAGES = {"index.html": page_home, "services.html": page_services, "about.html": page_about,
         "contact.html": page_contact, "404.html": page_404}

def clean_urls(html):
    """GitHub Pages serves /services for services.html, so links drop the extension (24 Nov 2026)."""
    html = html.replace('href="index.html"', 'href="./"')
    return re.sub(r'href="(services|about|contact)\.html', r'href="\1', html)


if __name__ == "__main__":
    for name, fn in PAGES.items():
        (ROOT / name).write_text(clean_urls(fn()), encoding="utf-8")
        print("wrote", name)
