===========
Get started
===========

Using with nanodjango
=====================

1. Install nanodjango along with its dependencies for static site generation, including
   django-nanopages and django-distill:

   .. code-block:: bash

       pip install nanodjango[static]

2. In your nanodjango script, register your directory of pages at a URL, at the end of
   your script:

   .. code-block:: python

       app.pages(url="", path="pages/")

3. Put your markdown, HTML, or Django template files under the ``path`` - in this case,
   a dir next to your script called ``pages``.

4. Optional: build to a static site with django-distill:

   .. code-block:: bash

       nanodjango manage myscript.py distill-local static_site/

   (see `django-distill docs <https://django-distill.com>`_ for more configuration and
   deployment options)


Using with full Django
======================

1. Install:

   .. code-block:: bash

       pip install django-nanopages

2. Add it to your ``INSTALLED_APPS`` in ``settings.py``:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           "django_nanopages",
       ]

3. In your ``urls.py``, register your directory of pages at a URL:

   .. code-block:: python

       from django_nanopages import Pages

       urlpatterns = [
           ...
           path("", include(Pages("pages/"))),
       ]
   ```

4. Put your markdown, HTML, or Django template files under the ``path`` - in this case,
   a dir called ``pages``.

5. Optional: build to a static site with django-distill:

   .. code-block:: bash

       ./manage.py distill-local static_site/

   (see `django-distill docs <https://django-distill.com>`_ for more configuration and
   deployment options)
