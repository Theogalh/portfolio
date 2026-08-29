# portfolio

Projects showcase for theogalh.dev — plain static HTML, in French and English.

Styling comes from the hosted design system
(`https://theogalh.github.io/design-system/styles.css`); page-specific rules live in
`assets/site.css`.

## Layout

```
index.html                    FR — home: hero, stats, project cards (canonical)
projects/<slug>.html          FR — one standalone page per project
en/index.html                 EN — home
en/projects/<slug>.html       EN — one standalone page per project
assets/site.css               page-specific CSS shared by every page
assets/site.js                mobile drawer, copy-to-clipboard, bilingual UI strings
assets/avatar.webp            hero illustration
.claude/skills/portfolio-page/  the edit checklist — read it before touching a page
.nojekyll                     serve the files as-is
```

There is no build step and no CI here: the repo *is* the site. Serving it is handled
externally, from the files as they are committed.

**The invariant:** both trees mirror each other file for file. `projects/ytp.html` and
`en/projects/ytp.html` are the same page in two languages, and the language switcher in
the topbar is a plain path swap between them. Never rename a slug on one side only.

## Preview locally

```bash
python3 -m http.server 8080
```

## Add a project

1. Copy an existing pair: `projects/ytp.html` → `projects/newthing.html`, and
   `en/projects/ytp.html` → `en/projects/newthing.html`.
2. In each: fix `<html lang>`, the title, breadcrumb, eyebrow number, sections and footer.
3. Cross-link the two: the `hreflang` pair in `<head>` and the `.langsw` switcher in the
   topbar.
4. Add a card to the `.apps-grid` in **both** `index.html` and `en/index.html`, and bump
   the projects counter in the stats.

The full checklist — including what stays in English on both sides and the shared
glossary — lives in `.claude/skills/portfolio-page/SKILL.md`.
