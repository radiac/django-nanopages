=====
Usage
=====

The ``Pages`` class
===================

In the :doc:`get_started`  guide we created and registered a ``Pages`` instance at a
path:

.. code-block:: python

    from django_nanopages import Pages

    urlpatterns = [
        ...
        path("", include(Pages("pages/"))),
    ]


The ``Pages`` class takes up to three arguments:

``Pages(path, name, context)``

``path``:
  The path to the directory containing source pages. Can be either a string path or a
  ``Path`` object.

  Relative paths are relative to ``django.settings.BASE_DIR``.

``name``:
  Optional string name for this ``Pages`` instance. Used for reverse URL lookups, so
  must be unique.

  Defaults to the dir name of ``path``, eg ``Pages("content/microsite")`` is the same as
  ``Pages("content/microsite", name="microsite")``.

``context``:
  Optional dict containing a common template context for all pages. Values can be
  overridden by :doc:`contexts` frontmatter.


.. _links:

Linking to pages
================

The ``Pages`` instance is registered to the URLs using its ``name``, so you can link to
pages using Django's standard ``{% url %}`` template tag and ``reverse()`` method.

For example, if your ``pages`` dir is registered as ``pages``, as above, to link to the
root index file ``pages/index.html``::

    {% url "pages" %}

To link to the file ``pages/blog/cookies.md``::

    {% url "pages" "blog/cookies" %}

or in Python:

.. code-block:: python

    from django.urls import reverse

    index_path = reverse("pages")
    cookies_path = reverse("pages", args=["blog/cookies"])
