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

RELATIVE_URLS = True

# Site-wide links shown in the sidebar (and mobile menu) on every page,
# alongside that page's own Table of Contents. `slug` matches a
# content/data/<slug>.yaml file so the current page can hide its own link.
NAV_LINKS = [
    {"label": "Organizers", "url": "/organizers/", "slug": "organizers"},
    {"label": "Sponsorship", "url": "/sponsorship/", "slug": "sponsorship"},
]
