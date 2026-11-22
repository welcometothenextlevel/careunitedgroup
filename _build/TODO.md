# Care United Group site: open items

Search the HTML for `TODO` to find each spot. Rebuild with `python3 _build/build.py` after editing.

## Must do before launch
1. **Formspree ID**: replace `YOUR_FORM_ID` (`FORM_ACTION` in `_build/build.py`). Create the form at formspree.io with cug.ndis@gmail.com as the recipient. Until then both quote forms show the thank-you message but send nothing.
2. **Remove noindex**: delete the `<meta name="robots" content="noindex, nofollow">` line (in `head()`), and switch `robots.txt` to `Allow: /` plus the Sitemap line.
3. **Final domain**: they own both www.cugndis.com and cugndis.com.au (both currently serve the Webador site). Pick one, then:
   - add `<link rel="canonical">` and `og:url` (absolute) to `head()`
   - make `og:image` absolute: `https://DOMAIN/images/og-image.jpg`
   - add `"url"` and `"image"` to the LocalBusiness JSON-LD (`schema()`)
   - check the domain in `sitemap.xml`, then submit it in Google Search Console
4. **Business name**: the brief and their current homepage say "Unitrd"; the ABN register and the NDIS Commission register both say CARE UNITED GROUP PTY LTD, so the site uses "United". Confirm with the client.
5. **NDIS registration renewal**: the Commission register says registration is in force until **19 December 2026**. The site says "registered" and links to the live register entry. Check renewal with the client. The public entry shows no registration number; add one to the About page if they want it shown.
6. **NDIS register website field**: their register entry lists `www.careuntited.com.au` (misspelt, and the domain doesn't resolve). The client should update it to their real domain via the NDIS Commission portal.

## Content from the client
- **Street address removed** at the client's request (22 Nov 2026): the site now says "Based in Auburn" only, with no map. Their NDIS register entry still shows the full address (that's the Commission's public register, not ours).
- **NDIS logo image** on the contact page was supplied by the client. It shows the NDIA's "ndis" logo; check the NDIA's brand rules allow a provider to use it, or swap for the Commission's registered-provider logo.
- **Phone numbers / WhatsApp** (updated 21 Nov 2026 from the client: 0440 127 111 and 0411 394 111; their old site still shows 0405 785 338 / 0404 726 260). The WhatsApp button points at 0440 127 111: confirm that's the WhatsApp number. Also update the numbers on their NDIS Commission register entry if they changed.
- **Logo**: new round badge supplied 21 Nov 2026 (`images/logo-badge-*.webp`, favicons). It's a raster image with white corners cut to a circle; ask for the original file (ideally SVG or a large transparent PNG) for sharper print and small sizes.
7. **Their van**: their own photos are in (exterior, side entry, rear wheelchair lift; number plate blurred). They arrived as 260px Messenger previews, so they're shown small. Ask for the full-size originals (send as a file or by email) to show them bigger. Also confirm how the van is used (appointments, community activities, outings).
8. **Adobe Stock images (client is licensing them)**: #1238389313, #1246633814, #1499957809, #1548763731. When the licensed downloads arrive, save them in `_build/adobe/` named `<ID>.jpg`, run `python3 _build/swap_adobe.py` then `python3 _build/build.py`, and push. See `_build/adobe/README.md`. Until then the site shows licence-free stand-ins.
9. **Photos**: every other image is either from their current site (Pexels) or Pexels. Replace with real photos, with consent.
10. **Feedback**: home page "In their own words" placeholder. Real quotes only, with written permission. (The "Oliver Hartman" quote on their current site is Webador template text.)
11. **Team**: About page placeholder (names, roles, photos, with permission).
12. **Languages spoken**: About page placeholder.
13. **Service areas**: suburbs/regions they cover beyond "Sydney".
14. **Service examples**: confirm the "This can include" lists on services.html.
15. **Socials / Google Business Profile**: none found. A Google Business Profile at 126 Cardigan St would help local SEO a lot.
