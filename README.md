# portfolio

Projects showcase for theogalh.dev — plain static HTML.

Styling comes from the hosted design system
(`https://theogalh.github.io/design-system/styles.css`); page-specific rules live in
`assets/site.css`.

## Layout

```
index.html                  home: hero, stats, project cards
projects/<slug>.html        one standalone page per project — edit freely
assets/site.css             page-specific CSS shared by every page
assets/site.js              mobile drawer + copy-to-clipboard
assets/avatar.webp          hero illustration
.nojekyll                   serve the files as-is
```

There is no build step and no CI here: the repo *is* the site. Serving it is handled
externally, from the files as they are committed.

## Preview locally

```bash
python3 -m http.server 8080
```

## Add a project

1. Copy an existing page: `cp projects/ytp.html projects/newthing.html`.
2. Edit the title, breadcrumb, footer and sections.
3. Add a card to the `.apps-grid` in `index.html`, pointing at `projects/newthing.html`.
