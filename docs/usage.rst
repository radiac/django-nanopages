=====
Usage
=====

See :doc:`contexts` for working with templates while writing content.


``Pages`` definitions
=====================

Pages are loaded from a path by the ``Pages`` class, which lets Django discover the
pages, and gives us helpful ways to interact with them (see :ref:`pages`).

To set it up, we instantiate it when we add it to our urls:

.. code-block:: python

    # urls.py
    from django_nanopages import Pages

    urlpatterns = [
        ...
        path("", include(Pages("pages/"))),
    ]


We can then access it later via the registry, using its ``name`` - it will default to
the dir name of the path (so here ``pages`` - or you can :ref:`override it <pages>` when
instantiating the class):

.. code-block:: python

    # views.py
    from django_nanopages import registry
    pages = registry['pages']


If you are using nanodjango, the ``app.pages(...)`` function returns the ``Pages``
instance directly:

.. code-block:: python

    from nanodjango import Django

    app = Django()
    pages = app.pages("/", "pages/")


.. _links:

Linking to pages
================

The ``Pages`` instance is registered to the URLs using its ``name``, so you can link to
pages using Django's standard ``{% url %}`` template tag and ``reverse()`` method.

For example, if your ``pages`` dir is registered as ``pages``:

.. code-block:: python

    from django_nanopages import Pages

    urlpatterns = [
        ...
        path("", include(Pages("pages/"))),
    ]


to link to the root index file ``pages/index.html``::

    {% url "pages" %}

To link to the file ``pages/blog/cookies.md``::

    {% url "pages" "blog/cookies" %}

or in Python:

.. code-block:: python

    from django.urls import reverse

    index_path = reverse("pages")
    cookies_path = reverse("pages", args=["blog/cookies"])



.. _pages_class:

The ``Pages`` class
===================

The ``Pages`` class takes up to three arguments:

``Pages(path, name, context)``

``path``
  The path to the directory containing source pages. Can be either a string path or a
  ``Path`` object.

  Relative paths are relative to ``django.settings.BASE_DIR``.

``name``
  Optional string name for this ``Pages`` instance. Used for registry and reverse URL
  lookups, so must be unique.

  Defaults to the dir name of ``path``, eg ``Pages("content/microsite")`` is the same as
  ``Pages("content/microsite", name="microsite")``.

``context``
  Optional dict containing a common template context for all pages. Values can be
  overridden by :doc:`contexts` frontmatter.

It has the following functions:

``get_page(request_path:str) -> Page | None``
  Return the ``Page`` object for a given requested path (under the pages root), or None
  if no suitable file exists.



.. _page_class:

The ``Page`` class
==================

The ``pages.get_page(request_path)`` returns a ``Page`` class instance. This has the
following attributes and methods:

``page.request_path``
  The path under the ``Pages`` root

``page.src``
  The local file path

``page.name``
  The name of the page - the final slug in the request path

``page.title``
  The ``title`` of the page from the ``page.context`` if it is set, or the ``page.name``
  in title case.

``page.pages``
  The ``Pages`` class this is from

``page.body``
  The raw content. Cached for the request by ``page.read()``.

``page.context``
  The frontmatter context - see :doc:`contexts` for details.

  Cached for the request by ``page.read()``.

``body, context = page.read(reload=False)``
  Get the raw content and context.

  This is cached for the duration of the request, in case the body or context are
  requested again separately.

  Pass ``reload=True`` to bypass the cache and force a reload.

``rendered = page.as_html()``
  Return the page body as HTML - if it is markdown it will be rendered to HTML,
  otherwise it will return the raw template HTML.

``page.get_absolute_url()``
  The URL to the page
