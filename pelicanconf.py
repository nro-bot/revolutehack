AUTHOR = "Boston Robot Hackers"
SITENAME = "Revolute"
SITEURL = ""

PATH = "content"
OUTPUT_PATH = "output"
TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"

# Custom theme (templates + static css).
THEME = "theme"

# The whole page is generated from content/data/page.yaml by our plugin.
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["yaml_page"]

# This is a single generated landing page, not a blog: turn off the article and
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
