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
7. **Their van**: confirm how it's used (appointments, community activities, outings) and send a real photo. The current van photo is a licence-free stand-in.
8. **Adobe Stock images (client is licensing them)**: #1057606701, #1238389313, #1246633814, #1499957809, #1548763731. When the licensed downloads arrive, save them in `_build/adobe/` named `<ID>.jpg`, run `python3 _build/swap_adobe.py` then `python3 _build/build.py`, and push. See `_build/adobe/README.md`. Until then the site shows licence-free stand-ins.
9. **Photos**: every other image is either from their current site (Pexels) or Pexels. Replace with real photos, with consent.
10. **Feedback**: home page "In their own words" placeholder. Real quotes only, with written permission. (The "Oliver Hartman" quote on their current site is Webador template text.)
11. **Team**: About page placeholder (names, roles, photos, with permission).
12. **Languages spoken**: About page placeholder.
13. **Service areas**: suburbs/regions they cover beyond "Sydney".
14. **Service examples**: confirm the "This can include" lists on services.html.
15. **Socials / Google Business Profile**: none found. A Google Business Profile at 126 Cardigan St would help local SEO a lot.
