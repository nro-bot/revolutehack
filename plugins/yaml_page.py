"""Data-driven page generator for Revolute.

Reads every *.yaml file in content/data/ and renders each through the
`page.html` template. All editable content lives in those plain-text YAML
files — no HTML — so adding, removing, or reordering a section is just
editing a file. `page.yaml` is the homepage and writes to index.html; any
other file, e.g. `sponsorship.yaml`, writes to `<slug>/index.html` so it
gets a clean URL like `/sponsorship/`.
"""

import logging
import os
import re
import shutil

import yaml
from PIL import Image, ImageOps
from pelican import signals
from pelican.generators import Generator

log = logging.getLogger(__name__)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v"}
WEB_MAX_PX = 1800  # longest side of the lightbox copy of a gallery photo
THUMB_MAX_PX = 640  # longest side of the grid thumbnail
GITHUB_FILE_LIMIT = 100 * 1024 * 1024


class YamlPageGenerator(Generator):
    def generate_context(self):
        data_dir = os.path.join(self.path, "data")
        self.pages_data = []
        self.gallery_jobs = []

        # _site.yaml holds site-wide settings (e.g. the floating banner) shared
        # by every page. Files starting with "_" are never pages themselves.
        site_path = os.path.join(data_dir, "_site.yaml")
        self.site = {}
        if os.path.exists(site_path):
            with open(site_path, encoding="utf-8") as fh:
                self.site = yaml.safe_load(fh) or {}

        for filename in sorted(os.listdir(data_dir)):
            if not filename.endswith(".yaml") or filename.startswith("_"):
                continue
            with open(os.path.join(data_dir, filename), encoding="utf-8") as fh:
                data = yaml.safe_load(fh)

            # The sidebar Table of Contents is just the ordered list of
            # sections, derived here so it can never drift from the content.
            data["toc"] = [
                {"id": s["id"], "title": s["title"]} for s in data.get("sections", [])
            ]

            # Inline any SVG logo referenced by an `svg:` key (partner/sponsor
            # logos) so it can inherit the accent color via `currentColor`.
            # The file lives in content/images/. Walk the whole tree so this
            # works wherever a logo appears.
            self._inline_svgs(data)

            # A gallery section with `folder: <name>` shows everything in
            # content/images/<name>/ — see _collect_gallery.
            for sec in data.get("sections", []):
                if sec.get("type") == "gallery" and sec.get("folder"):
                    sec["items"] = (sec.get("items") or []) + self._collect_gallery(sec["folder"])

            slug = os.path.splitext(filename)[0]
            is_home = slug == "page"
            data["is_home"] = is_home
            data["slug"] = slug
            output_name = "index.html" if is_home else f"{slug}/index.html"
            self.pages_data.append((output_name, data))

    def _collect_gallery(self, folder):
        """List every photo/video in content/images/<folder>/, by filename.

        Photos get a small grid thumbnail plus a larger lightbox copy, both made
        at build time (originals stay out of the site); videos are copied as-is. Queued in self.gallery_jobs and written
        to the output dir in generate_output.
        """
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
            alt = "Revolute hackathon " + ("video" if ext in VIDEO_EXTS else "photo")
            if ext in IMAGE_EXTS:
                full = f"{folder}/web/{safe}.jpg"
                thumb = f"{folder}/thumb/{safe}.jpg"
                items.append({"src": thumb, "full": full, "alt": alt})
                self.gallery_jobs.append((src, full, WEB_MAX_PX))
                self.gallery_jobs.append((src, thumb, THUMB_MAX_PX))
            else:
                rel = f"{folder}/web/{safe}{ext}"
                item = {"video": rel, "alt": alt}
                # Optional still frame: posters/<same name>.jpg in the folder.
                poster_src = os.path.join(src_dir, "posters", stem + ".jpg")
                if os.path.exists(poster_src):
                    item["poster"] = f"{folder}/web/{safe}-poster.jpg"
                    self.gallery_jobs.append((poster_src, item["poster"], WEB_MAX_PX))
                items.append(item)
                if os.path.getsize(src) > GITHUB_FILE_LIMIT:
                    log.warning("gallery video %s is over GitHub's 100MB file limit — compress it", name)
                self.gallery_jobs.append((src, rel, None))
        return items

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
        for output_name, data in self.pages_data:
            writer.write_file(
                name=output_name,
                template=self.get_template("page"),
                context={**self.context, "page": data, "site": self.site},
                relative_urls=self.settings["RELATIVE_URLS"],
            )


def get_generators(pelican_object):
    return YamlPageGenerator


def register():
    signals.get_generators.connect(get_generators)
