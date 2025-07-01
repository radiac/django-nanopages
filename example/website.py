# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
# ]
# ///
from nanodjango import Django

app = Django(
    EXTRA_APPS=["django_style"],
)
app.pages("/", path="pages", context={"site_title": "nanopages example"})
