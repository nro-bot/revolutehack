# Revolute — Pelican site

A single-page Pelican site for the Revolute hackathon. **All content lives in
one plain-text data file — no HTML to edit.**

## What goes where

- `content/data/page.yaml` — **the only file you normally edit.** Every bit of
  copy (hero, footer, and all sections) is here as plain YAML. No tags, no
  closing elements.
- `content/images/` — logos and photos referenced from `page.yaml` live here
  (currently `fabfoundation.png`, `seeedstudio.png`, `miters.svg`). Drop a file
  in and point a `src:`/`img:`/`svg:` field at it by filename.
- `plugins/yaml_page.py` — reads the YAML and generates `index.html`.
- `theme/templates/page.html` — the layout plus one small macro per section
  type.
- `theme/static/css/style.css` — all styling.
- `pelicanconf.py` — Pelican config (wires in the plugin).

## The hero and footer

Top-level keys in `page.yaml` control the masthead and footer. Most are
optional — comment one out (prefix lines with `#`) and it simply disappears:

- `title`, `version`, `kicker` — the header/hero text.
- `apply_url` — target of the "Apply / register" button in the header.
- `intro:` — supporting lines under the title (a list).
- `facts:` — the fact tiles (`label` / `value` pairs).
- `photos:` — the photo strip (`src` / `alt` / `caption`), plus `photo_credit`.
- `footer:` — the lines at the bottom of the page (a list).

## Adding, removing, and reordering sections

Sections are a list under `sections:` in `page.yaml`. To **add** one, copy an
existing block and change its `id`, `title`, and content. To **remove** one,
delete its block. To **reorder**, move blocks up or down. The page order, the
sidebar Table of Contents, and the section numbers (01, 02, …) all follow this
list automatically — you never edit the ToC or the numbers by hand.

Each section has a `type` that picks how it renders:

| `type`     | For                          | Key fields                                          |
|------------|------------------------------|-----------------------------------------------------|
| `prose`    | paragraphs                   | `body:` (list); optional `button:`, `note_box:`, `partners:` |
| `list`     | simple bullets               | `items:` (list)                                     |
| `cards`    | tagged items w/ link + note  | `intro:`, `cards:`; optional `links:`               |
| `schedule` | timed agenda                 | `intro:`, `days:` → `rows:`                         |
| `faq`      | expandable Q&A               | `items:` (`q:`, `a:`, `open:`)                      |
| `sponsors` | logo wall, optional tiers    | `intro:`, `tiers:` (`label`, `size`, `logos:`), `note:` |

### Logos (partners and sponsors)

A `prose` section can end with a `partners:` band, and the `sponsors` section
shows a logo wall. In both, a single logo is one of:

- `img: "file.png"` — a raster logo, shown on a white chip.
- `svg: "file.svg"` — a vector logo, inlined and tinted to the accent color
  (give the SVG a `currentColor` stroke/fill to pick up the tint).
- `name: "Text"` — a text placeholder when there's no artwork yet.

`url:` (link) is optional on any logo. In a `sponsors` tier, `size:` may be
`lg`, `md` (default), or `sm` to scale the logos.

To support a brand-new section type, add a macro in
`theme/templates/page.html` and a branch in its `render_section` dispatcher.

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
