# Revolute — Pelican site

A Pelican site for the Revolute hackathon. **All content lives in plain-text
data files — no HTML to edit.**

## What goes where

- `content/data/*.yaml` — **the files you normally edit.** Every bit of copy
  (hero, footer, and all sections) is plain YAML, one file per page. No tags,
  no closing elements. `page.yaml` is the homepage; any other file, e.g.
  `sponsorship.yaml`, becomes its own page at `/<filename>/` (see below).
- `content/images/` — logos and photos referenced from a YAML file live here.
  Drop a file in and point a `src:`/`img:`/`svg:`/`photo:` field at it by
  filename.
- `plugins/yaml_page.py` — reads every `content/data/*.yaml` file and
  generates a page for each.
- `theme/templates/page.html` — the layout plus one small macro per section
  type.
- `theme/static/css/style.css` — all styling.
- `pelicanconf.py` — Pelican config (wires in the plugin).

## Pages

| File                              | URL             |
|------------------------------------|-----------------|
| `content/data/page.yaml`           | `/` (homepage)  |
| `content/data/sponsorship.yaml`    | `/sponsorship/` |
| `content/data/organizers.yaml`     | `/organizers/`  |

To add a new page, drop a new `content/data/<slug>.yaml` file with the same
top-level shape as the others (`title`, `sections:`, etc.) — it'll build to
`/<slug>/` automatically. To surface it in the sidebar (and the mobile menu)
on every page, add it to `NAV_LINKS` in `pelicanconf.py`; a page never lists
itself, since each entry's `slug` is compared against the current page's.

## The hero and footer

Top-level keys in a page's YAML control its masthead and footer. Most are
optional — comment one out (prefix lines with `#`) and it simply disappears:

- `title`, `version`, `kicker` — the header/hero text.
- `apply_url` — target of the "Apply / register" button in the header.
- `intro:` — supporting lines under the title (a list).
- `facts:` — the fact tiles (`label` / `value` pairs). Note: these render
  inside the section whose `id` is `details`, not in the hero itself — that
  placement is hardcoded in `page.html`'s section loop.
- `photos:` — the photo strip (`src` / `alt` / `caption`), plus `photo_credit`.
- `footer:` — the lines at the bottom of the page (a list).

## Adding, removing, and reordering sections

Sections are a list under `sections:` in a page's YAML file. To **add** one,
copy an existing block and change its `id`, `title`, and content. To
**remove** one, delete its block. To **reorder**, move blocks up or down. The
page order, the sidebar Table of Contents, and the section numbers (01, 02, …)
all follow this list automatically — you never edit the ToC or the numbers by
hand.

Each section has a `type` that picks how it renders:

| `type`     | For                          | Key fields                                          |
|------------|------------------------------|-----------------------------------------------------|
| `prose`    | paragraphs                   | `body:` (list); optional `button:`, `note_box:`, `partners:` |
| `list`     | simple bullets               | `items:` (list)                                     |
| `cards`    | tagged items w/ link + note  | `intro:`, `cards:`; optional `links:`               |
| `schedule` | timed agenda                 | `intro:`, `days:` → `rows:`                         |
| `faq`      | expandable Q&A               | `items:` (`q:`, `a:`, `open:`)                      |
| `sponsors` | logo wall, optional tiers    | `intro:`, `tiers:` (`label`, `size`, `logos:`), `note:` |
| `table`    | comparison grid              | `columns:` (`label`, `price`), `rows:` (`label`, `cells:` — booleans) |
| `people`   | profile grid (judges, organizers) | `intro:`, `people:` (`name`, `title`; optional `affiliation`, `photo`, `url`, `bio`) |

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
