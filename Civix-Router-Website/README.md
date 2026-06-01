# Civix-Router Website

Marketing and documentation site for **Civix-Router** — Smart Governance AI bridging Tamil civic complaints to English government systems.

## Structure

```
Civix-Router-Website/
├── index.html
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── main.js
│   └── chart.js
├── assets/
│   └── images/
└── README.md
```

## Local preview

No build step required. Serve the folder with any static file server.

**Python:**

```bash
cd Civix-Router-Website
python -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

**Node (npx):**

```bash
npx serve Civix-Router-Website
```

**VS Code:** Use the “Live Server” extension and open `index.html`.

## Live demo link

The Streamlit app lives in the parent repo. From the project root:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Update the hero “View Live Demo” button in `index.html` to your deployed Streamlit URL when available.

## Deployment

### GitHub Pages

1. Push this folder to a repo (or use a `docs/` or `gh-pages` branch).
2. In repository **Settings → Pages**, set source to the branch/folder containing `index.html`.
3. Site URL: `https://<username>.github.io/<repo>/`

### Netlify / Vercel

- **Build command:** none  
- **Publish directory:** `Civix-Router-Website` (or repo root if only the site is published)

### Custom domain

Point DNS to your host and add your domain in the host’s dashboard.

## Dependencies

- [Chart.js 4.4.1](https://www.chartjs.org/) (loaded via CDN in `index.html`)
- No npm or bundler required

## Accessibility

- Skip link, semantic landmarks, ARIA on navigation toggle
- Keyboard: Escape closes mobile menu; focusable controls throughout
- `prefers-reduced-motion` disables gradient, typing, and hover transforms

## License

Same as the [Civix-Router](https://github.com/Dharun4264/Civix-Router) repository.
