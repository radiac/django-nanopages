=============
Page contexts
=============

When rendering a page, it's sometimes useful to have a context - variables and values
which can be used to control templates.

For example, lets assume we have a ``blog.html`` Django template which looks like:

.. code-block:: html

    {% extends "base.html" %}

    {% block header %}

      <h1>{{ title }}</h1>
      <p>By {{ author }}</p>
    {% endblock %}

    {% block content %}
      This block will be replaced by the markdown content
    {% endblock %}

    {% block article %}
      or we could put the content in a different block like this:<hr>
      {{ content }}
    {% endblock %}

This page template uses several template variables - ``title``, ``author`` and
``content``.


We can define this context in the page file between two ``---`` lines, which must appear
at the very top of the document:


.. code-block:: markdown

    ---
    extends: blog.html
    title: Hello world
    author: Richard
    ---
    Page contents


This will look familiar to you if you have used other static site generators -
django-nanopages uses a similar approach to front matter in Jekyll, Hugo or 11ty.


Configure nanopages
===================

The variables defined are then available in the context for the base template. There are
some special keys:

- ``extends`` - the name of the base template - file content will be put in the
  ``{% block content %}`` if it exists. Defaults to ``"base.html"``.
- ``content`` - django-nanopages will set this to the markdown file content, so do not
  set this yourself.


Context languages
=================

The default context format is a simple ``key: value`` pairs, where all values are
strings without newlines - it is not YAML.

If ``pyyaml`` is installed, you can specify the YAML context parser:

.. code-block:: yaml

    ---yaml
    extends: blog.html
    title: "Hello world"
    lede: |
      In this article we explore the warmth and positivity
      that a simple greeting can bring.
    authors:
      - Richard
      - Murgatroyd
      - Persephone
    ---
    Page contents

For this to work, you will need to install ``pyyaml`` first::

    pip install pyyaml
    # or
    pip install django-nanopages[full]

You can also use JSON, where the top level are key/value pairs for an object:

.. code-block:: json

    ---json
    "extends": "blog.html",
    "title": "Hello world",
    "authors": ["Richard", "Murgatroyd", "Persephone"]
    ---
    Page contents


HTML files
==========

HTML files are treated as Django templates, so you should manually extend a template.
You can then override blocks and use template tags as you would any template.
