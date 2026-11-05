#!/usr/bin/env python3
"""Check a built site for broken local links and missing files.

Run after building:

    pelican content -o output -s pelicanconf.py
    python scripts/check_links.py output

Every `href`, `src`, `poster` and `data-*` address that points inside the site
must exist in the output folder. Addresses on other sites are not checked.
Exits with status 1 if anything is missing.
"""

import os
import re
import sys

ATTRS = r"(?:href|src|poster|data-poster|data-thumb)"
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
SCRIPTS = re.compile(r"<script\b.*?</script>", re.S | re.I)


def main(root):
    missing = []
    pages = 0
    for folder, _, names in os.walk(root):
        for name in names:
            if not name.endswith(".html"):
                continue
            pages += 1
            page = os.path.join(folder, name)
            with open(page, encoding="utf-8") as fh:
                html = fh.read()
            # Scripts build addresses out of strings; those are not links.
            html = SCRIPTS.sub("", html)
            for address in re.findall(ATTRS + r'="([^"]*)"', html):
                path = address.split("#")[0].split("?")[0]
                if not path or EXTERNAL.match(path):
                    continue
                base = root if path.startswith("/") else folder
                target = os.path.normpath(os.path.join(base, path.lstrip("/")))
                if os.path.isdir(target):
                    target = os.path.join(target, "index.html")
                if not os.path.exists(target):
                    missing.append((os.path.relpath(page, root), address))
    for page, address in missing:
        print(f"{page}: {address} does not exist")
    print(f"Checked {pages} pages: {len(missing)} broken local links.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "output"))
