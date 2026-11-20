"""Data-driven page generator for Revolute.

Every page is described by a plain-text YAML file in content/data/. No HTML
lives there, so editing copy, adding a project, or reordering a section is a
text edit.

Two kinds of page are built:

* **App pages** carry a `layout:` key (`upcoming`, `previous`, `gallery`,
  `community`, `sponsorship`). Each renders through
  `theme/templates/app_<layout>.html` and shares one shell: section tabs, the
  floating bottom bar, and the popups. `page.yaml` is the homepage; any other
  file writes to `/<name>/`.
* **Legacy pages** have no `layout:` key and still render through
  `page.html`, section by section.

Files whose name starts with `_` are data, never pages:

* `_site.yaml`      site-wide settings: navigation, sign-up, social links.
* `_projects.yaml`  hackathon entries. Each also gets a page at
                    `/projects/<slug>/`.
* `_tutorial.yaml`  the Tutorial tab on the homepage: the order of the steps,
                    which are Markdown files in content/docs/.
"""

import datetime
import logging
import os
import re
import shutil
from urllib.parse import urlsplit

import markdown
import yaml
from PIL import Image, ImageOps
from pelican import signals
from pelican.generators import Generator

log = logging.getLogger(__name__)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v"}
WEB_MAX_PX = 1800  # longest side of the popup copy of a gallery photo
THUMB_MAX_PX = 640  # longest side of the grid thumbnail
GITHUB_FILE_LIMIT = 100 * 1024 * 1024
APP_LAYOUTS = {"upcoming", "previous", "gallery", "community", "sponsorship"}
# GitHub-style alerts in the tutorial files: "> [!CAUTION]" and so on.
ALERT = re.compile(r"^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:>.*\n?)*)", re.M)


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _origin(url):
    parts = urlsplit(url or "")
    return f"{parts.scheme}://{parts.netloc}" if parts.scheme in ("http", "https") else None


class YamlPageGenerator(Generator):
    def generate_context(self):
        data_dir = os.path.join(self.path, "data")
        self.pages_data = []  # (output name, template name, page data)
        self.gallery_jobs = []

        def data_file(name):
            path = os.path.join(data_dir, name)
            return _load(path) if os.path.exists(path) else {}

        self.site = data_file("_site.yaml")
        self._prepare_social(self.site)
        self.projects = self._prepare_projects(data_file("_projects.yaml"))
        self.tutorial = data_file("_tutorial.yaml")
        self._prepare_tutorial(self.tutorial)

        raw = {
            os.path.splitext(name)[0]: _load(os.path.join(data_dir, name))
            for name in sorted(os.listdir(data_dir))
            if name.endswith(".yaml") and not name.startswith("_")
        }
        for slug, data in raw.items():
            data["slug"] = slug
            data["is_home"] = slug == "page"
            output_name = "index.html" if data["is_home"] else f"{slug}/index.html"
            layout = data.get("layout")
            if layout in APP_LAYOUTS:
                self._prepare_app_page(data, raw)
                self.pages_data.append((output_name, f"app_{layout}", data))
            else:
                if layout:
                    log.warning("%s.yaml: unknown layout %r, using the legacy template", slug, layout)
                self._prepare_legacy_page(data)
                self.pages_data.append((output_name, "page", data))

        for project in self.projects.get("projects", []):
            page = {
                "layout": "project",
                "slug": f"projects/{project['slug']}",
                "title": project["name"],
                "description": project.get("tagline", ""),
                "og_image": project.get("poster"),
                "project": project,
            }
            self.pages_data.append((f"projects/{project['slug']}/index.html", "app_project", page))

        # Every site the pages may load in a frame, for the Content Security
        # Policy: anything named `embed` or `map_embed` in the data files.
        origins = set()
        self._collect_origins([self.site, self.projects, raw], origins)
        self.site["frame_origins"] = sorted(origins)

    # ---- app pages -------------------------------------------------------

    @staticmethod
    def _as_date(value):
        return value if isinstance(value, datetime.date) else datetime.date.fromisoformat(str(value))

    def _prepare_social(self, site):
        """Split an account's `events:` into upcoming (soonest first) and
        past (newest first), for the list in its popup."""
        today = datetime.date.today()
        for account in site.get("social") or []:
            events = account.get("events")
            if not events:
                continue
            for event in events:
                day = self._as_date(event["date"])
                event["day"] = day
                event["label"] = f"{day:%A}, {day:%B} {day.day}, {day.year}"
                event["month"] = f"{day:%b}"
                # The short line on a card with a poster: "Fri, Nov 6 · 6:00 PM".
                when = f"{day:%a}, {day:%b} {day.day}"
                if day.year != today.year:
                    when += f", {day.year}"
                if event.get("time"):
                    when += f" · {event['time']}"
                event["when"] = when
            account["upcoming"] = sorted((e for e in events if e["day"] >= today), key=lambda e: e["day"])
            account["past"] = sorted((e for e in events if e["day"] < today), key=lambda e: e["day"], reverse=True)

    def _prepare_tutorial(self, data):
        """Read each step's Markdown file from content/docs/, in the order
        `steps` gives. The file's first heading is the step's title. Each
        step is a page inside the Tutorial card, with the id `tutorial-<name>`."""
        docs_dir = os.path.join(self.path, "docs")
        # `steps` is a list of groups ({group: title, files: [...]}) or, for a
        # list without headings, of file names.
        # Within a group, a file name is one step; a list of names is a set of
        # alternatives that share one number.
        def entries(files):
            return [[str(f) for f in e] if isinstance(e, list) else [str(e)] for e in files or []]

        groups = []
        for item in data.get("steps") or []:
            if isinstance(item, dict):
                groups.append({"title": item.get("group") or "", "entries": entries(item.get("files"))})
            elif groups and not groups[-1]["title"]:
                groups[-1]["entries"] += entries([item])
            else:
                groups.append({"title": "", "entries": entries([item])})
        names = [f for g in groups for e in g["entries"] for f in e]

        read = lambda name: self._read_doc(docs_dir, name, "_tutorial.yaml")  # noqa: E731

        steps = [s for s in (read(n) for n in names) if s]
        by_file = {s["file"]: s for s in steps}
        number = 0
        for g in groups:
            g["steps"] = []
            for e in g["entries"]:
                number += 1
                for k, f in enumerate(e):
                    if f in by_file:
                        by_file[f]["number"] = number
                        by_file[f]["label"] = f"{number}{'abcdefgh'[k]}" if len(e) > 1 else str(number)
                        g["steps"].append(by_file[f])
        data["groups"] = groups
        # The About entries: pages like the steps, but not numbered.
        about_names = data.get("about") or []
        if isinstance(about_names, str):
            about_names = [about_names]
        about = [a for a in (read(str(n)) for n in about_names) if a]
        data["about"] = about
        data["pages"] = about + steps
        if os.path.isdir(docs_dir):
            for name in sorted(os.listdir(docs_dir)):
                if name.endswith(".md") and name not in names and name not in [str(n) for n in about_names]:
                    log.warning("content/docs/%s is not listed in _tutorial.yaml, so it is not built", name)
        total = number
        for i, step in enumerate(steps):
            step["total"] = total
            step["prev"] = steps[i - 1] if i else None
            step["next"] = steps[i + 1] if i + 1 < total else None
        data["steps_data"] = steps

    def _read_doc(self, folder, name, listed_in):
        """A Markdown file as a page: its first heading is the title, the rest
        is rendered. None, with an error logged, if the file is missing."""
        path = os.path.join(folder, name)
        if not os.path.exists(path):
            log.error("%s lists %s, but there is no such file in %s", listed_in, name, folder)
            return None
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        heading = re.match(r"\s*#\s+(.+?)\s*\n", text)
        slug = os.path.splitext(name)[0]
        title = heading.group(1).strip() if heading else slug.replace("-", " ").title()
        body = text[heading.end():] if heading else text
        return {"slug": slug, "id": f"tutorial-{slug}", "file": name, "title": title, "html": self._render_markdown(body)}

    @staticmethod
    def _render_markdown(text):
        """Markdown to HTML, the way GitHub shows it: fenced code blocks (each
        with a Copy button), tables, and "> [!CAUTION]" alerts as callouts."""

        def alert(match):
            kind = match.group(1).lower()
            inner = "\n".join(line[1:].lstrip() for line in match.group(2).splitlines())
            body = markdown.markdown(inner)
            return f'<div class="callout {kind}" role="note"><b>{kind.capitalize()}</b>{body}</div>\n'

        text = ALERT.sub(alert, text + "\n")
        html = markdown.markdown(text, extensions=["fenced_code", "sane_lists", "tables"])
        # Links to other sites open in a new tab, as everywhere on the site.
        html = re.sub(r'<a href="(https?://[^"]*)">', r'<a href="\1" target="_blank" rel="noopener">', html)
        # Every code block gets a Copy button, wired up by app.js.
        return re.sub(
            r"<pre>(.*?)</pre>",
            r'<div class="code"><pre>\1</pre><button class="mini copy" type="button" data-copy>Copy</button></div>',
            html,
            flags=re.S,
        )

    def _prepare_projects(self, data):
        """Fill in each project's poster, optional preview clip, and neighbours."""
        projects = data.get("projects") or []
        for i, project in enumerate(projects):
            folder = os.path.join(self.path, "images", "projects", project["slug"])
            project["poster"] = f"projects/{project['slug']}/poster.jpg"
            self._add_youtube(project)
            if os.path.exists(os.path.join(folder, "preview.mp4")):
                project["preview"] = f"projects/{project['slug']}/preview.mp4"
            if not os.path.exists(os.path.join(folder, "poster.jpg")):
                log.warning("project %s has no poster.jpg in %s", project["slug"], folder)
            project["prev"] = projects[i - 1]
            project["next"] = projects[(i + 1) % len(projects)]
        return data

    @staticmethod
    def _add_youtube(item):
        """Turn a `youtube:` video id into the two addresses the templates use."""
        video = item.get("youtube")
        if video:
            start = int(item.get("youtube_start") or 0)
            # The privacy-friendly player address, shown in a popup.
            item["embed"] = f"https://www.youtube-nocookie.com/embed/{video}?autoplay=1&rel=0" + (f"&start={start}" if start else "")
            item["watch"] = f"https://www.youtube.com/watch?v={video}" + (f"&t={start}s" if start else "")

    def _prepare_app_page(self, data, raw):
        layout = data["layout"]
        if layout == "upcoming":
            for item in (data.get("hardware") or {}).get("items") or []:
                self._add_youtube(item)
            # The tracks under the agenda: Markdown files in content/tracks/.
            tracks_dir = os.path.join(self.path, "tracks")
            files = (data.get("tracks") or {}).get("files") or []
            data["tracks_data"] = [t for t in (self._read_doc(tracks_dir, str(f), "page.yaml") for f in files) if t]
        elif layout == "previous":
            photos = data.get("photos") or {}
            if photos.get("folder"):
                items = [i for i in self._collect_gallery(photos["folder"], photos) if i["kind"] == "photo"]
                picks = photos.get("pick")
                if picks:
                    items = [next(i for i in items if p in i["name"]) for p in picks if any(p in i["name"] for i in items)]
                data["photo_items"] = items[: photos.get("count", 8)]
        elif layout == "gallery":
            items = []
            for album in data.get("albums") or []:
                items += self._collect_gallery(album["folder"], album)
            data["items"] = items
        elif layout == "community":
            for person in (data.get("team") or {}).get("people") or []:
                parts = person["name"].split()
                person["initials"] = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()
                if person.get("url"):
                    person["link_label"] = self._link_label(person["url"])
            # Past events drop off the list. This is decided at build time,
            # so the list is as fresh as the last deploy.
            today = datetime.date.today()
            data["events"] = [e for e in data.get("events") or [] if self._event_date(e) >= today]
            for event in data["events"]:
                start = event["date"]
                if not isinstance(start, datetime.date):
                    start = datetime.date.fromisoformat(str(start))
                event["label"] = f"{start:%b} {start.day}"

        elif layout == "sponsorship":
            tiers = data.get("tiers") or []
            names = [tier["name"] for tier in tiers]
            for tier in tiers:
                tier["benefits"] = []
            for benefit in data.get("benefits") or []:
                if benefit.get("from") not in names:
                    log.error("sponsorship.yaml: benefit %r starts at %r, which is not a tier", benefit.get("label"), benefit.get("from"))
                    continue
                first = names.index(benefit["from"])
                for index, tier in enumerate(tiers[first:], first):
                    tier["benefits"].append({"label": benefit["label"], "new": index == first})

    @staticmethod
    def _link_label(url):
        """What to call a link to someone's own page: "LinkedIn" or the site's name."""
        host = urlsplit(url).netloc.lower().removeprefix("www.")
        known = {"linkedin.com": "LinkedIn", "github.com": "GitHub", "instagram.com": "Instagram"}
        return known.get(host, host)

    @staticmethod
    def _event_date(event):
        value = event.get("end_date") or event.get("date")
        if isinstance(value, datetime.date):
            return value
        return datetime.date.fromisoformat(str(value))

    def _collect_origins(self, node, found):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("embed", "map_embed") and isinstance(value, str):
                    origin = _origin(value)
                    if origin:
                        found.add(origin)
                elif key not in ("prev", "next"):  # projects link to each other in a ring
                    self._collect_origins(value, found)
        elif isinstance(node, list):
            for item in node:
                self._collect_origins(item, found)

    # ---- legacy pages ----------------------------------------------------

    def _prepare_legacy_page(self, data):
        # The sidebar Table of Contents is just the ordered list of sections,
        # derived here so it can never drift from the content.
        data["toc"] = [{"id": s["id"], "title": s["title"]} for s in data.get("sections", [])]

        # Inline any SVG logo referenced by an `svg:` key (partner/sponsor
        # logos) so it can inherit the accent color via `currentColor`.
        self._inline_svgs(data)

        # A gallery section with `folder: <name>` shows everything in
        # content/images/<name>/. See _collect_gallery.
        for sec in data.get("sections", []):
            if sec.get("type") == "gallery" and sec.get("folder"):
                sec["items"] = (sec.get("items") or []) + self._collect_gallery(sec["folder"])

    def _inline_svgs(self, node):
        if isinstance(node, dict):
            if node.get("svg"):
                svg_path = os.path.join(self.path, "images", node["svg"])
                with open(svg_path, encoding="utf-8") as fh:
                    node["svg_markup"] = fh.read()
            for value in node.values():
                self._inline_svgs(value)
        elif isinstance(node, list):
            for item in node:
                self._inline_svgs(item)

    # ---- media -----------------------------------------------------------

    def _collect_gallery(self, folder, options=None):
        """List every photo and video in content/images/<folder>/, by filename.

        Photos get a small grid thumbnail plus a larger popup copy, both made
        at build time, so originals stay out of the published site. Videos
        are copied as they are. A video shows a still frame if
        `posters/<same name>.jpg` exists in the folder.

        `options` may carry, all optional:
          credit   text shown with every item, e.g. the photographer
          alt      fallback description for items without a caption
          first    name fragments of items to move to the front, in order
          meta     {name fragment: {caption: ..., duration: ...}}
        """
        options = options or {}
        meta = options.get("meta") or {}
        src_dir = os.path.join(self.path, "images", folder)
        items = []
        for name in sorted(os.listdir(src_dir)):
            stem, ext = os.path.splitext(name)
            ext = ext.lower()
            if ext not in IMAGE_EXTS | VIDEO_EXTS:
                continue
            # Safe URL-friendly output name (originals have spaces, parens).
            safe = re.sub(r"[^A-Za-z0-9_-]+", "-", stem).strip("-")
            src = os.path.join(src_dir, name)
            is_video = ext in VIDEO_EXTS
            info = next((v for k, v in meta.items() if k in stem), {}) or {}
            fallback = options.get("alt") or "Revolute hackathon " + ("video" if is_video else "photo")
            item = {
                "name": stem,
                "kind": "video" if is_video else "photo",
                "caption": info.get("caption") or fallback,
                "alt": info.get("caption") or fallback,
                "credit": options.get("credit", ""),
                "duration": info.get("duration", ""),
            }
            if not is_video:
                item["full"] = f"{folder}/web/{safe}.jpg"
                item["src"] = f"{folder}/thumb/{safe}.jpg"
                self.gallery_jobs.append((src, item["full"], WEB_MAX_PX))
                self.gallery_jobs.append((src, item["src"], THUMB_MAX_PX))
            else:
                item["video"] = f"{folder}/web/{safe}{ext}"
                poster_src = os.path.join(src_dir, "posters", stem + ".jpg")
                if os.path.exists(poster_src):
                    item["poster"] = f"{folder}/web/{safe}-poster.jpg"
                    self.gallery_jobs.append((poster_src, item["poster"], WEB_MAX_PX))
                if os.path.getsize(src) > GITHUB_FILE_LIMIT:
                    log.warning("gallery video %s is over GitHub's 100MB file limit: compress it", name)
                self.gallery_jobs.append((src, item["video"], None))
            items.append(item)

        first = options.get("first") or []

        def rank(item):
            for position, fragment in enumerate(first):
                if fragment in item["name"]:
                    return position
            return len(first)

        return sorted(items, key=rank)  # stable: the rest keep filename order

    def _write_gallery_files(self):
        for src, rel, max_px in self.gallery_jobs:
            dest = os.path.join(self.output_path, "images", *rel.split("/"))
            if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src):
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if max_px:
                with Image.open(src) as im:
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    im.thumbnail((max_px, max_px))
                    im.save(dest, "JPEG", quality=82, optimize=True)
            else:
                shutil.copyfile(src, dest)

    def generate_output(self, writer):
        self._write_gallery_files()
        for output_name, template, data in self.pages_data:
            writer.write_file(
                name=output_name,
                template=self.get_template(template),
                context={
                    **self.context,
                    "page": data,
                    "site": self.site,
                    "projects": self.projects.get("projects", []),
                    "projects_event": self.projects.get("event", ""),
                    "tutorial": self.tutorial,
                },
                relative_urls=self.settings["RELATIVE_URLS"],
            )


def get_generators(pelican_object):
    return YamlPageGenerator


def register():
    signals.get_generators.connect(get_generators)
