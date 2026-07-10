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
        self.page_data = data

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
