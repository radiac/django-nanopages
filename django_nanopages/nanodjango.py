from pathlib import Path

from nanodjango import Django, hookimpl


@hookimpl
def django_pre_setup(app):
    """
    Install nanopages
    """
    from django.conf import settings

    if "nanopages" not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append("django_nanopages")


@hookimpl
def django_post_setup(app):
    """
    Add ``app.pages(..)`` method to nanodjango.Django
    """

    def pages(
        self,
        pattern: str,
        path: str | Path,
        *,
        re: bool = False,
        name: str | None = None,
        context: dict | None = None,
    ):
        """
        django-nanopages integration
        """
        from django_nanopages import Pages

        self.route(
            pattern,
            include=Pages(path, name=name, context=context),
            re=re,
        )

    Django.pages = pages
