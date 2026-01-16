# Django Nanopages

[![PyPI](https://img.shields.io/pypi/v/django-nanopages.svg)](https://pypi.org/project/django-nanopages/)
[![Documentation](https://readthedocs.org/projects/django-nanopages/badge/?version=latest)](https://django-nanopages.readthedocs.io/en/latest/)
[![Tests](https://github.com/radiac/django-nanopages/actions/workflows/ci.yml/badge.svg)](https://github.com/radiac/django-nanopages/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/radiac/django-nanopages/branch/main/graph/badge.svg?token=BCNM45T6GI)](https://codecov.io/gh/radiac/django-nanopages)

Generate Django pages from Markdown, HTML, and Django template files.

Integrates well with:

- [nanodjango](https://github.com/radiac/nanodjango), to build a simple site with a single Python script
- [django-distill](https://django-distill.com/), to generate a static site
- [django-style](https://github.com/radiac/django-style), for clean base templates
- [django-browser-reload](https://github.com/adamchainz/django-browser-reload/), for automatic browser reloading

Read the [documentation](https://django-nanopages.readthedocs.io/en/latest/) or find the project on [PyPI](https://pypi.org/project/django-nanopages/).

## Creating pages

Nanopages supports

- `page.md` - markdown
- `page.html` - Django template

Where two files have the same name, the markdown file will be used. These would both be
served at `/page/`

HTML files are treated as Django templates, so you can also override blocks.

Files called `index` are special - they are the default content for their path, eg

- `section/index.md` will be served at `/section/`
- `section/page.md` will be served at `/section/page/`

Source pages can also provide context for your Django templates - see
[context documentation](https://django-nanopages.readthedocs.io/en/latest/contexts/)

## Quickstart

### Try the example

Try out [the example site](https://github.com/radiac/django-nanopages/tree/main/example) using nanodjango:

```
git clone https://github.com/radiac/django-nanopages.git
cd django-nanopages/example
uv run example/website.py
```

### Using with nanodjango

1. Install nanodjango along with its optional dependencies, including django-nanopages
   and django-distill:

   ```bash
   pip install nanodjango[full]
   ```

2. In your nanodjango script, register your directory of pages at a URL, at the end of
   your script:

   ```python
   app.pages(url="", path="pages/")
   ```

3. Put your markdown, HTML, or Django template files under the `path` - in this case, a
   dir next to your script called "pages".

4. Optional: build to a static site with django-distill:

   ```bash
   nanodjango manage myscript.py distill-local static_site/
   ```

   (see [django-distill docs](https://django-distill.com/) for more configuration and
   deployment options)

### Using with full Django

1. Install:

   ```bash
   pip install django-nanopages
   ```

2. Add it to your `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       "django_nanopages",
   ]
   ```

3. In your `urls.py`, register your directory of pages at a URL:

   ```python
   from django_nanopages import Pages

   urlpatterns = [
       ...
       path("", Pages("pages/")),
   ]
   ```

4. Put your markdown, HTML, or Django template files under the `path` - in this case, a
   dir called "pages".

5. Optional: build to a static site with django-distill:

   ```bash
   ./manage.py distill-local static_site/
   ```

   (see [django-distill docs](https://django-distill.com/) for more configuration and
   deployment options)
