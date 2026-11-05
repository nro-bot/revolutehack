AUTHOR = "Boston Robot Hackers"
SITENAME = "Revolute"
SITEURL = ""

PATH = "content"
OUTPUT_PATH = "output"
TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"

# Custom theme (templates + static css).
THEME = "theme"

# Every page is generated from a content/data/*.yaml file by our plugin.
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["yaml_page"]

# This is a small set of generated pages, not a blog: turn off the article and
# page machinery so nothing else gets written.
ARTICLE_PATHS = ["_unused"]
PAGE_PATHS = ["_unused"]
DIRECT_TEMPLATES = []

# No feeds for a landing page.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Copy images straight through to output/images/.
STATIC_PATHS = ["images"]
# Gallery albums are not copied as they are: the plugin writes web-sized
# copies and thumbnails of each instead. List every album folder here.
STATIC_EXCLUDE_PATHS = ["images/hackday", "images/arms"]

RELATIVE_URLS = True

# Legacy pages only (those without a `layout:` key in their YAML file).
# The app pages take their navigation from content/data/_site.yaml.
# Site-wide links shown in the sidebar (and mobile menu) on every page,
# alongside that page's own Table of Contents. `slug` matches a
# content/data/<slug>.yaml file so the current page can hide its own link.
NAV_LINKS = [
    {"label": "Events", "url": "/events/", "slug": "events"},
    {"label": "Gallery", "url": "/gallery/", "slug": "gallery"},
    {"label": "Sponsorship", "url": "/sponsorship/", "slug": "sponsorship"},
]
