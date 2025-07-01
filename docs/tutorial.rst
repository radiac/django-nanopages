========
Tutorial
========

Lets build a simple static site. We're going to use nanodjango to keep things simple,
but the principles will work just as well with a full Django project - see the
:doc:`installation instructions <get_started>` for the differences.

You can see this working in the ``examples`` directory of the git repository for this
project.


Installing
==========

First lets install the dependencies for our project:

.. code-block:: bash

    pip install nanodjango django-nanopages django-distill django-style


Nanodjango has a dependency group for building static sites, so we can shorten this to:

.. code-block:: bash

    pip install nanodjango[static] django-style


The Python
==========

Now lets create a simple Django script, called ``website.py``:

.. code-block:: python

    from nanodjango import Django

    app = Django(
        EXTRA_APPS=["django_style"],
    )
    app.pages("/", path="pages", context={"site_title": "nanopages example"})

Django-nanopages uses nanodjango's plugin system to automatically register itself, and
add an ``app.pages`` method.

This lets us define our pages at ``/``, and it will look for source files in a ``pages``
dir.

We're also passing a ``site_title`` context variable to every page in this section
- that's used by django-style to set the header title.

If we were using full Django rather than nanodjango, we'd define this in our
``urls.py``:


.. code-block:: python

    from django_nanopages import Pages

    urlpatterns = [
        ...
        path("", include(Pages('pages'))),
    ]

Create pages
============

We're going to create some files - our project dir is going to look like this::

    website.py
    pages/
      index.html
      about.md
      blog/
        index.md
        cookies.md
        work.html

You can see all these files in the ``examples`` dir in this project's git repository,
but lets look at a couple of these files in more detail.


``pages/index.html``
--------------------

This will be served at the top level of this page section - so at ``/``.

.. code-block:: html

    ---
    title: Welcome
    ---
    {% extends "base.html" %}

    {% block content %}
      <p>Welcome to the example site.</p>

      <p><a href="/about/">About</a></p>
      <p><a href="/blog/">Blog</a></p>
    {% endblock %}
    ```

This will extend the django-style base template, and override the ``content`` block.

We've got a standard Django template here, except for the context frontmatter at the top
- see :doc:`contexts`  for more details. This will set the page title variable in the
django-style template.


``pages/about.md``
------------------

This will be served at ``/about/``:

.. code-block:: markdown

    ---
    title: About this example
    ---

    This is an extremely simple and contrived example.

    - [Return to home](/)

This is a markdown file, which again defines a ``title`` frontmatter, and then some
content.

This will extend ``base.html`` by default and render into the ``{% block content %}``.
Behind the scenes, this content is actually put in the ``content`` template variable,
and we use a shim template to render into the block - but you only need to think about
that if you don't want to extend ``base.html``.

Take a look through all the example files to see some other tricks like overriding the
context variables set in ``app.pages(..)``.


Serve the site
==============

You can now serve the site as normal:

.. code-block:: bash

    nanodjango run website.py


Generate static HTML files
==========================

Lastly we can use the ``django-distill`` integration to generate a static site:

.. code-block:: bash

    nanodjango manage website.py distill-local static_site/

See [django-distill docs](https://django-distill.com/) for more configuration and
deployment options.
