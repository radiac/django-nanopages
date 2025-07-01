# Django Nanopages

Generate Django pages from Markdown, HTML, and Django template files.

Integrates well with:

- nanodjango, to build a simple site with a single Python script
- [django-distill](https://django-distill.com/), to generate a static site
- django-style, for clean base templates

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
[context documentation]()

## Quickstart

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
