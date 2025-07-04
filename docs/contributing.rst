============
Contributing
============

Contributions are welcome, preferably via pull request. Check the github issues to see
what needs work, or if you have an idea for a new feature it may be worth raising an
issue to discuss it first.


Installing
==========

The easiest way to work on this is to fork the project on GitHub, then run the example
using your local copy of django-style:

.. code-block:: bash

    git clone https://github.com/radiac/django-nanopages.git
    cd django-nanopages/example
    uv run example/website.py


Testing
=======

It's always easier to merge PRs when they come with tests.

Run the tests with pytest:

.. code-block:: bash

    pip install -r tests/requirements.txt
    pytest
