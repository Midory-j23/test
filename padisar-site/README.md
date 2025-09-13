# Padisar Inc — Static Site

A modern, responsive multi-page website with a clean UI inspired by the information on `www.padisarinc.com`.

## Structure
- `index.html`: Landing page
- `about.html`: Company overview
- `services.html`: Services (with section anchors)
- `news.html`: News grid (placeholders)
- `contact.html`: Contact details and form (static demo)
- `assets/css/styles.css`: Small polish and accessibility helpers

## Quick Start (local)
Open `index.html` directly in a browser, or serve the folder:

```bash
cd padisar-site
python3 -m http.server 8000
# then open http://localhost:8000
```

## Customize Content
Replace placeholder copy with official text from `www.padisarinc.com`. Update images by swapping the `src` URLs. Navigation uses relative links; keep filenames as-is or update links accordingly.

## Branding
Colors use Tailwind (indigo). To change brand color, replace `indigo-*` classes in HTML with your preferred palette (e.g., `sky`, `emerald`, `violet`). You can also add custom CSS to `assets/css/styles.css`.

## Deploy
- GitHub Pages: Push the `padisar-site` folder to a `gh-pages` branch or enable Pages on `main` and set root to `/ (root)`.
- Netlify/Vercel: Drag-and-drop the folder or connect the repo; set the publish directory to `padisar-site`.

## Notes
- The contact form is static. Integrate a form backend (e.g., Netlify Forms, Formspree) for submissions.
- Tailwind is loaded via CDN for simplicity. For production hardening, a build step is recommended to tree-shake CSS.