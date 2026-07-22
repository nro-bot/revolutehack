"""Data-driven page generator for Revolute.

Reads every *.yaml file in content/data/ and renders each through the
`page.html` template. All editable content lives in those plain-text YAML
files — no HTML — so adding, removing, or reordering a section is just
editing a file. `page.yaml` is the homepage and writes to index.html; any
other file, e.g. `sponsorship.yaml`, writes to `<slug>/index.html` so it
gets a clean URL like `/sponsorship/`.
"""

import os

import yaml
from pelican import signals
from pelican.generators import Generator


class YamlPageGenerator(Generator):
    def generate_context(self):
        data_dir = os.path.join(self.path, "data")
        self.pages_data = []
        for filename in sorted(os.listdir(data_dir)):
            if not filename.endswith(".yaml"):
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

            slug = os.path.splitext(filename)[0]
            is_home = slug == "page"
            data["is_home"] = is_home
            data["slug"] = slug
            output_name = "index.html" if is_home else f"{slug}/index.html"
            self.pages_data.append((output_name, data))

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

    def generate_output(self, writer):
        for output_name, data in self.pages_data:
            writer.write_file(
                name=output_name,
                template=self.get_template("page"),
                context={**self.context, "page": data},
                relative_urls=self.settings["RELATIVE_URLS"],
            )


def get_generators(pelican_object):
    return YamlPageGenerator


def register():
    signals.get_generators.connect(get_generators)
