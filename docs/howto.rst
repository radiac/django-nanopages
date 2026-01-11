=======
How-tos
=======

Helpful hints and common patterns.


Minimal nanodjango site
=======================

`Nanodjango <https://nanodjango.dev/>`_ is a perfect way to build a minimal static site
generator.

Create a ``mysite.py``:

.. code-block:: python

    # /// script
    # dependencies = ["nanodjango", "django-nanopages", "django-browser-reload"]
    # ///
    from nanodjango import Django

    app = Django()
    pages = app.pages("/", "pages/")

    if  __name__ == "__main__":
      app.run()


Run it using ``uv`` (or ``pipx`` or similar) - this will listen on port 8000:

.. code-block:: bash

    uv run mysite.py 0:8000

Build it to a static site using the :doc:`django-distill integration <static>`:

.. code-block:: bash

    pip install nanodjango django-nanopages
    nanodjango manage mysite.py distill-local static_site/


.. _breadcrumbs:

Breadcrumbs
===========

You can create breadcrumbs by walking the the page hierarchy.

.. warning::

   This will need to load every file in the path to get the page title, so could be
   quite slow if used directly in production. You would either want to use the
   ``django-distill`` integration to build it as a :doc:`static site <static>`, or
   write a management command to loop over your pages and generate an index.


You could implement this as a template tag:

.. code-block:: python

    from django import template
    from django.utils.safestring import mark_safe

    register = template.Library()


    @register.simple_tag(takes_context=True)
    def breadcrumbs(context):
        page = context.get("page")
        if not page:
            return ""

        # Split the request path into parts
        parts = [p for p in page.request_path.split("/") if p]
        if not parts:
            # Root index page has no breadcrumbs
            return ""

        links = []
        # Build breadcrumbs by walking up the path
        for i, part in enumerate(parts):
            # Get the path to this level
            path_parts = parts[: i + 1]
            request_path = "/".join(path_parts)

            # Get the page at this level
            crumb_page = page.pages.get_page(request_path)
            if crumb_page:
                url = crumb_page.get_absolute_url()
                title = crumb_page.title
                links.append(f'<a href="{url}">{title}</a>')

        return mark_safe(f"<ul><li>{'</li><li>'.join(links)}</li></ul>")
