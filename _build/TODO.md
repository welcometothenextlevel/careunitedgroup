# Care United Group site: open items

Search the HTML for `TODO` to find each spot. Rebuild with `python3 _build/build.py` after editing.

## Must do before launch
1. **Formspree ID**: replace `YOUR_FORM_ID` (`FORM_ACTION` in `_build/build.py`). Create the form at formspree.io with cug.ndis@gmail.com as the recipient. Until then both quote forms show the thank-you message but send nothing.
2. **Remove noindex**: delete the `<meta name="robots" content="noindex, nofollow">` line (in `head()`), and switch `robots.txt` to `Allow: /` plus the Sitemap line.
3. **Final domain**: confirm it (www.cugndis.com is assumed). Then:
   - add `<link rel="canonical">` and `og:url` (absolute) to `head()`
   - make `og:image` absolute: `https://DOMAIN/images/og-image.jpg`
   - add `"url"` and `"image"` to the LocalBusiness JSON-LD (`schema()`)
   - check the domain in `sitemap.xml`, then submit it in Google Search Console
4. **Business name**: the brief said "Unitrd"; the ABN register lists CARE UNITED GROUP PTY LTD, so the site uses "Care United Group". Confirm with the client.
5. **NDIS registration**: status and registration number (footer and About page). Make no registration claim until confirmed.

## Content from the client
6. **Real photos**: every image is a stock placeholder (some reused from their current site's Pexels images). Replace with real photos, with consent.
7. **Logo**: header uses a one-colour (green/terracotta) trace of their purple logo mark. Confirm, or supply the original vector logo.
8. **Favicon**: placeholder made from the mark (`favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`).
9. **Feedback**: home page "In their own words" placeholder. Real quotes only, with written permission.
10. **Team**: About page placeholder (names, roles, photos, with permission).
11. **Languages spoken**: About page placeholder.
12. **Service areas**: suburbs/regions they cover beyond "Sydney" (home page area section).
13. **Service examples**: confirm the "This can include" lists on services.html.

## Notes
- The current cugndis.com site uses five Adobe Stock watermarked preview images (not licensed). None of them are used here.
