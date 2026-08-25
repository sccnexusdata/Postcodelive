# PostcodeLive

A postcode-first local publishing platform for UK towns: map, directory, calendar, useful local information and upload-ready social media output.

## What this repo gives you

- Static public site ready for GitHub Pages or Hostinger `public_html` upload.
- Postcode/radius-style discovery model with sample Lewes/Brighton/Newhaven town configuration.
- Events, directory, map cards and social-media campaign output from the same data.
- Repository structure designed to become the shared base for LewesLive, BrightonLive and future town sites.

## Quick deploy

### GitHub Pages
1. Use this repository as the shared PostcodeLive base.
2. In GitHub: Settings → Pages → Source: GitHub Actions.
3. Push to `main`; the included workflow publishes `public_html`.

### Hostinger / normal web host
Upload the contents of `public_html/` into the site's web root.

## Structure

```text
public_html/
  index.html
  assets/css/site.css
  assets/js/app.js
  assets/data/config.json
  assets/data/directory.json
  assets/data/events.json
  assets/data/social.json
  assets/img/icons/*.svg
.github/workflows/pages.yml
scripts/validate.js
```

## Data model

The site is deliberately data-led. Edit the JSON files in `public_html/assets/data/` first; the front end then renders town cards, events, directory listings and social posts.

## Validation

```bash
npm test
```
