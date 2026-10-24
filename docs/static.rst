======================
Static site generation
======================

Django Nanopages integrates with
`django-distill <https://github.com/meeb/django-distill/blob/master/README.md>`_
to generate a fully static HTML site from your pages.

This is perfect for blogs, documentation sites, or any content that doesn't need dynamic
server-side rendering. Your pages can still be edited locally through Django admin,
but the public site is served as pre-rendered static files.


Installation
============

Install django-distill next to django-nanopages:

.. code-block:: bash

    pip install django-distill

Nanopages will detect if django-distill is installed, and will automatically register
urls so they're ready to be built to static content.


With nanodjango
===============

If you're using nanodjango, generate your static site with ``nanodjango manage``:

.. code-block:: bash

    nanodjango manage website.py distill generate --output-directory=output/ --collectstatic

See the :docs:howto: for a full example.


With standard Django
====================

For a standard Django project:

.. code-block:: bash

    python manage.py distill generate --output-directory=output/ --collectstatic



Build options
=============

The ``distill-local`` command supports several useful options. See the
`django-distill documentation <https://github.com/meeb/django-distill/blob/master/README.md>`_
for full details, but as a quick reference:

Collect static files automatically:

.. code-block:: bash

    python manage.py distill generate --output-directory=output/ --collectstatic


Force overwrite - skip confirmation prompts when overwriting existing files:

.. code-block:: bash

    python manage.py distill generate --output-directory=output/ --collectstatic --force


Deployment
==========

Once you've generated your static site, you can deploy it anywhere that serves static
files. See the `django-distill documentation <https://django-distill.com/deployment>`_
for full details, but as a quick reference for common deployments:


GitHub Pages
------------

Push your generated ``output/`` directory to a ``gh-pages`` branch:

.. code-block:: bash

    python manage.py distill generate --output-directory=output/ --collectstatic
    cd output/
    git init
    git add .
    git commit -m "Deploy static site"
    git push -f origin main:gh-pages


Cloud storage
-------------

Django-distill can publish directly to cloud storage providers.

For example, to publish directly to Amazon S3, install boto3:

.. code-block:: bash

    pip install boto3

Then configure your deployment target in settings:

.. code-block:: python

    # settings.py
    DISTILL_PUBLISH = {
      'default': {
          'ENGINE': 'django_distill.backends.amazon_s3',
          'PUBLIC_URL': 'http://.../',
          'ACCESS_KEY_ID': os.environ['AWS_ACCESS_KEY_ID'],
          'SECRET_ACCESS_KEY': os.environ['AWS_SECRET_ACCESS_KEY'],
          'BUCKET': '...',
          'region': 'us-east-1',
      },
    }

Then publish:

.. code-block:: bash

    python manage.py distill publish --collectstatic

This automatically syncs your static site to S3, removing old files and uploading new
ones.

Google Cloud Storage and Azure use similar configuration.
