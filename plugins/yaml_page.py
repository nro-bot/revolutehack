"""Data-driven page generator for Revolute.

Reads content/data/page.yaml and renders it through the `page.html` template,
then lets Pelican write it as index.html. All editable content lives in that
one plain-text YAML file — no HTML — so adding, removing, or reordering a
section is just editing the file.
"""

import os

import yaml
from pelican import signals
from pelican.generators import Generator


class YamlPageGenerator(Generator):
    def generate_context(self):
        path = os.path.join(self.path, "data", "page.yaml")
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        # The sidebar Table of Contents is just the ordered list of sections,
        # derived here so it can never drift from the content.
        data["toc"] = [
            {"id": s["id"], "title": s["title"]} for s in data.get("sections", [])
        ]

        # Inline any SVG logo referenced by an `svg:` key (partner/sponsor
        # logos) so it can inherit the accent color via `currentColor`. The
        # file lives in content/images/. Walk the whole tree so this works
        # wherever a logo appears.
        self._inline_svgs(data)

        self.page_data = data

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
        writer.write_file(
            name="index.html",
            template=self.get_template("page"),
            context={**self.context, "page": self.page_data},
            relative_urls=self.settings["RELATIVE_URLS"],
        )


def get_generators(pelican_object):
    return YamlPageGenerator


def register():
    signals.get_generators.connect(get_generators)
