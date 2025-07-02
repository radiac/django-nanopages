# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
# ]
# ///
#
# Run with:
#
#    git clone https://github.com/radiac/django-nanopages.git
#    cd django-nanopages/example
#    uv run example/website.py
#
from nanodjango import Django

app = Django(
    EXTRA_APPS=["django_style"],
)
app.pages("/", path="pages", context={"site_title": "nanopages example"})


if __name__ == "__main__":
    app.run()
