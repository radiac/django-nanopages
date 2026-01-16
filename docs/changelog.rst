=========
Changelog
=========

0.3.1 - 2026-01-16
------------------

Bugfix:

* URLs with suffix resolved correctly


0.3.0 - 2026-01-11
------------------

Features:

* Add ``Pages.registry`` dict to retrieve a ``Pages`` instance
* Add ``Pages.get_page(request_path)`` to get a ``Page`` object
* Add ``Page`` object, to work with page data in templates or outside the page view
* Template context now has ``page``, a reference to the current ``Page`` object

Changes:

* ``Pages`` names must be unique
* nanodjango ``app.pages(...)`` call now returns a ``Pages`` object
* Renamed view from ``views.Page`` to ``views.PageView``


Docs:

* Add :doc:`howto` and :doc:`static` documentation


0.2.0 - 2026-01-03
------------------

Features:

* Add support for auto-reloading with django-browser-reload


Docs:

* Add :doc:`usage` documentation
* Add ``{% url %}`` usage pattern to usage and tutorial


Changes:

* Page URL paths are now positional, not named
* Pages instance name must now be unique (required for URL resolution)


0.1.0 - 2025-07-02
------------------

Initial release
