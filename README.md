# Revolute — Pelican site

A single-page Pelican site for the Revolute hackathon. **All content lives in
one plain-text data file — no HTML to edit.**

## What goes where

- `content/data/page.yaml` — **the only file you normally edit.** Every bit of
  copy (hero, facts, photos, and all sections) is here as plain YAML. No tags,
  no closing elements.
- `content/images/` — drop `robotarm.jpg`, `pasta.jpg`,
  `shenzhenhackathon.jpg`, and `hackathon.png` here.
- `plugins/yaml_page.py` — reads the YAML and generates `index.html`.
- `theme/templates/` — the scaffolding + one small macro per section type.
- `theme/static/css/style.css` — all styling.
- `pelicanconf.py` — Pelican config (wires in the plugin).

## Adding, removing, and reordering sections

Sections are a list under `sections:` in `page.yaml`. To **add** one, copy an
existing block and change its `id`, `title`, and content. To **remove** one,
delete its block. To **reorder**, move blocks up or down. The page order, the
sidebar Table of Contents, and the section numbers (01, 02, …) all follow this
list automatically — you never edit the ToC or the numbers by hand.

Each section has a `type` that picks how it renders:

| `type`     | For                          | Key fields                         |
|------------|------------------------------|------------------------------------|
| `prose`    | paragraphs                   | `body:` (list); optional `button:`, `note_box:` |
| `list`     | simple bullets               | `items:` (list)                    |
| `cards`    | tagged items w/ link + note  | `intro:`, `cards:`; optional `links:` |
| `schedule` | timed agenda                 | `intro:`, `days:` → `rows:`        |
| `faq`      | expandable Q&A               | `items:` (`q:`, `a:`, `open:`)     |

To support a brand-new type, add a macro in `theme/templates/page.html` and a
branch in its `render_section` dispatcher.

Inline HTML (like a link) is allowed inside any text value if you need it —
e.g. `value: '<a href="…">FabLab Kendall</a>, Cambridge'` — but it's optional.

## Build

    pip install -r requirements.txt
    pelican content -o output -s pelicanconf.py
    # output/index.html is the finished page

Live preview while editing:

    pelican --autoreload --listen content -o output -s pelicanconf.py

## Deploy (GitHub Pages)

`.github/workflows/deploy.yml` builds and publishes on every push to `main`.
One-time setup: **Settings → Pages → Build and deployment → Source: GitHub
Actions**. Dependencies are pinned in `requirements.txt` so local and CI builds
match.
