# Revolute — Pelican site

A Pelican site for the Revolute hackathon. **All content lives in plain-text
data files — no HTML to edit.**

The site is built like an app: a floating bar at the bottom moves between four
pages, each page has a row of tick-box tabs for its sections, and sign-up,
social accounts, photos and maps open in popups. Each page is still a real
page with its own address.

## What goes where

- `content/data/*.yaml` — **the files you normally edit.** One file per page,
  plus two shared files whose names start with `_`. Each file starts with a
  comment explaining its fields.
- `content/images/` — every picture and clip the site publishes. Web-sized
  files only: keep camera originals out of the repo (`content/raw/` is ignored
  by git for that purpose).
- `plugins/yaml_page.py` — turns the YAML files into pages.
- `theme/templates/app_*.html` — the app pages: one shared shell
  (`app_base.html`), one template per page, and shared pieces
  (`app_macros.html`).
- `theme/static/css/app.css`, `theme/static/js/app.js` — their styling and
  behaviour. Fonts are in `theme/static/fonts/`.
- `scripts/check_links.py` — checks a built site for broken local links.
- `pelicanconf.py` — Pelican config (wires in the plugin).

## Pages

| File                            | URL                  | What it is |
|---------------------------------|----------------------|------------|
| `content/data/page.yaml`        | `/`                  | The upcoming hackathon: Overview, Hardware, Agenda, FAQ |
| `content/data/previous.yaml`    | `/previous/`         | The last hackathon: Winners, Entries, Agenda, Photos, About |
| `content/data/gallery.yaml`     | `/gallery/`          | Every photo and video, filtered by All, Photos, Videos |
| `content/data/community.yaml`   | `/community/`        | Social, Events, Affiliates, Team |
| `content/data/_projects.yaml`   | `/projects/<slug>/`  | One page per hackathon entry |
| `content/data/_site.yaml`       | —                    | Shared by every page: the bottom bar, the Register link, social accounts |

A file with a `layout:` line is an app page. The older pages below have no
`layout:` line and still use the original design. See "Legacy pages".

| File                            | URL             |
|---------------------------------|-----------------|
| `content/data/events.yaml`      | `/events/`      |

## Common edits

**Change the Register link.** In `_site.yaml`, under `register:`, set `url` to
the event's Luma page and `embed` to its "Embed Event Page" address (on Luma:
the event's manage page, More, "Embed Registration Button"). Every Register
button on the site follows.

**Change the upcoming hackathon.** Edit `page.yaml`: `title`, the `facts`
tiles, `hardware`, `agenda`, `faq`. Each tab's card is sized to fit one
screen, so keep the lists short.

**Add a hackathon entry.** Add a block to `_projects.yaml` and put its media
in `content/images/projects/<slug>/`: `poster.jpg` (required) and
`preview.mp4` (optional, a silent 6 to 8 second loop). The entry appears on
`/previous/` and gets its own page.

**Add photos or videos to the gallery.** Drop them into an album folder in
`content/images/`, such as `hackday/`. Photos are resized when the site is
built. Videos are published as they are, so compress them first. Captions are
optional and go in `gallery.yaml`. A new album folder needs two lines: an
entry under `albums:` in `gallery.yaml`, and its folder in
`STATIC_EXCLUDE_PATHS` in `pelicanconf.py`.

**Add an event or an affiliate.** Edit `community.yaml`. Past events drop off
the page the next time the site is built.

**Add a social account.** Add it under `social:` in `_site.yaml`. It appears
in the row of icons on every page and on the Community page.

## How the app pages work

- **Tabs are links.** Each tab points at a section's id, such as `#agenda`,
  and the stylesheet shows the section the address points at. This works with
  JavaScript turned off, and every section has its own shareable address.
- **Popups are links too.** A Register button is a link to Luma, a gallery
  tile is a link to the photo. The script opens them in a popup instead. Open
  one in a new tab and you get the real page.
- **Sites shown in popups** (Luma, Instagram, YouTube, a map, affiliates) are
  loaded in a frame only when the popup opens. The build collects their
  addresses from every `embed:` line in the YAML and allows exactly those in
  the page's Content Security Policy. A site that refuses to be framed should
  have its `embed:` line removed: the popup then shows a short description
  and a button to the site.
- **Moving between pages** uses the browser's own page transitions, and pages
  start loading when a link is hovered or touched.

## Legacy pages

Everything from here to "Build" describes the original design, still used by
`events.yaml`. That page is rendered by `theme/templates/page.html` and
styled by `theme/static/css/style.css`. The app pages do not use any of it.
The organizers are now the Team tab on `/community/` (`team:` in
`community.yaml`), and `/sponsorship/` is an app page.

To surface a legacy page in the legacy sidebar, add it to `NAV_LINKS` in
`pelicanconf.py`.

## The header announcement

`content/data/_site.yaml` holds site-wide settings shared by every page (files
starting with `_` are never pages). Its `banner:` block is the announcement
line in the header of every page (desktop only): edit `text` and the optional
`url` it links to, or comment the block out to hide it.

## The hero and footer

Top-level keys in a page's YAML control its masthead and footer. Most are
optional — comment one out (prefix lines with `#`) and it simply disappears:

- `title`, `version` — the header/hero text.
- `apply_url` — target of the "Apply / register" button in the header.
- `intro:` — supporting lines under the title (a list).
- `photos:` — the photo strip (`src` / `alt` / `caption`), plus `photo_credit`.
- `footer:` — the lines at the bottom of the page (a list).

Two things live on individual *sections*, not the page root: `facts:`
(fact tiles, `prose` sections only — see the type table below) and
`bg_image:` (a faded illustration spanning the content column, desktop only,
any section type — a filename in `content/images/`).

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
| `prose`    | paragraphs                   | `body:` (list); optional `facts:`, `button:`, `qr:` (`img`, `caption`, `url`), `note_box:`, `partners:` |
| `list`     | simple bullets               | `items:` (list)                                     |
| `cards`    | tagged items w/ link + note  | `intro:`, `cards:`; optional `links:`, `photos:`    |
| `schedule` | timed agenda                 | `intro:`, `days:` → `rows:`                         |
| `faq`      | expandable Q&A               | `items:` (`q:`, `a:`, `open:`)                      |
| `sponsors` | logo wall, optional tiers    | `intro:`, `tiers:` (`label`, `size`, `logos:`), `note:` |
| `table`    | comparison grid              | `columns:` (`label`, `price`), `rows:` (`label`, `cells:` — booleans) |
| `people`   | profile grid (judges, organizers) | `intro:`, `people:` (`name`, `title`; optional `role`, `affiliation`, `photo`, `url`, `bio`) |
| `gallery`  | photo/video grid             | `folder:` (a folder in `content/images/`, shown in full) and/or `items:`; optional `intro:`, `album:` (`label`, `url`) |
| `calendar` | month calendar of events     | `events:` (`title`, `date`, optional `end_date`, `time`, `location`, `poster`, `info`, `url`, `button`) |

### Logos (partners and sponsors)

A `prose` section can end with a `partners:` band, and the `sponsors` section
shows a logo wall. In both, a single logo is one of:

- `img: "file.png"` — a raster logo, shown on a white chip.
- `svg: "file.svg"` — a vector logo, inlined and tinted to the accent color
  (give the SVG a `currentColor` stroke/fill to pick up the tint).
- `name: "Text"` — a text placeholder when there's no artwork yet.

`url:` (link) is optional on any logo. In a `sponsors` tier, `size:` may be
`lg`, `md` (default), or `sm` to scale the logos.

### Photos (cards sections)

A `cards` section can end with a `photos:` strip — each entry is `src:`
(a filename in `content/images/`), `alt:`, and an optional `caption:`.
Captions don't show in the strip itself; clicking (or Enter/Space on) a photo
opens it larger in a lightbox, where the caption appears underneath.

To support a brand-new section type, add a macro in
`theme/templates/page.html` and a branch in its `render_section` dispatcher.

Inline HTML (like a link) is allowed inside any text value if you need it —
e.g. `value: '<a href="…">FabLab Kendall</a>, Cambridge'` — but it's optional.

## Build (pip)

    pip install -r requirements.txt
    pelican content -o output -s pelicanconf.py
    # output/index.html is the finished page

Live preview while editing:

    pelican --autoreload --listen content -o output -s pelicanconf.py

## Build (uv)
    curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv (once)
    uv venv --python 3.12                             # create .venv (once)
    uv pip install -r requirements.txt                # install deps (once)
  
  Live preview while editing:

    uv run pelican --autoreload --listen content -o output -s pelicanconf.py
    # open http://127.0.0.1:8000/

Check the built site for broken local links:

    uv run python scripts/check_links.py output

Preview through the local server, not by opening the files directly: the app
pages load their script as a module, which browsers only allow over http.

## Deploy (GitHub Pages)

`.github/workflows/deploy.yml` builds and publishes on every push to `main`.
`.github/workflows/build.yml` builds every other branch and every pull request
and checks the links, without publishing.
One-time setup: **Settings → Pages → Build and deployment → Source: GitHub
Actions**. Dependencies are pinned in `requirements.txt` so local and CI builds
match.
