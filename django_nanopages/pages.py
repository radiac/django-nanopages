from pathlib import Path

from django.dispatch import receiver
from django.urls import URLResolver, include, path, re_path
from django.utils.autoreload import autoreload_started, file_changed, get_reloader

from .views import Page

try:
    from django_browser_reload.views import trigger_reload_soon
except ImportError:
    trigger_reload_soon = None


registry = []


class Pages(tuple):
    #: Path to the source dir
    path: Path

    #: Name of this instance
    name: str

    #: Template context
    context: dict | None

    def __init__(
        self,
        path: str | Path,
        name: str | None = None,
        *,
        context: dict | None = None,
    ):
        """
        Initialise a set of pages from the specified path

        Args:
            path (str, Path):
                Path to the directory containing source pages. Relative paths are
                relative to django.settings.BASE_DIR.
            name (str, None):
                Name of this group of pages. Used for reverse URL lookups, must be
                unique.
                Defaults to the dir name of ``path``.
            context (dict, None):
                Common template context for all pages - can be overridden by page
                context frontmatter.
        """
        from django.conf import settings

        if isinstance(path, str):
            path = Path(path)

        if not path.is_absolute():
            path = Path(settings.BASE_DIR) / path

        self.path = path.resolve()
        self.name = name or self.path.stem
        self.context = context
        super().__init__()

        # Check name uniqueness
        for pages in registry:
            if pages.name == self.name:
                raise ValueError(
                    f"Pages name {self.name} for {self.path} also used for {pages.path}"
                )

        registry.append(self)
        self.autoreload()

    @property
    def urls(self) -> tuple[list[URLResolver], str | None, str | None]:
        """
        Return the URL patterns for the pages

        Supports django-distill if installed
        """
        # Import here due to potential load order conflicts with nanodjango
        try:
            from django_distill import distill_path, distill_re_path
        except ImportError:
            distill_path = None
            distill_re_path = None

        # Determine which path fns we're going to use
        if distill_path and distill_re_path:
            return include(
                [
                    distill_path(
                        "",
                        view=Page.as_view(pages=self, extra_context=self.context),
                        name=self.name,
                    ),
                    distill_re_path(
                        r"^(.*)/$",
                        Page.as_view(pages=self, extra_context=self.context),
                        name=self.name,
                        distill_func=self.get_request_paths,
                    ),
                ],
            )

        return include(
            [
                path(
                    "",
                    Page.as_view(pages=self, extra_context=self.context),
                    name=self.name,
                ),
                re_path(
                    r"^(.*)/$",
                    Page.as_view(pages=self, extra_context=self.context),
                    name=self.name,
                ),
            ]
        )

    def get_request_paths(self) -> list[str]:
        """
        Get all request paths for the pages
        """
        paths: list[str] = []

        if not self.path.is_dir():
            return paths

        for file_path in self.path.rglob("*"):
            if file_path.suffix not in [".md", ".html"]:
                continue

            if file_path.name in ["index.md", "index.html"]:
                request_path = f"{file_path.parent.relative_to(self.path)}"
            else:
                abs_path = file_path.with_name(file_path.name[: -len(file_path.suffix)])
                request_path = f"{abs_path.relative_to(self.path)}"

            if request_path == ".":
                continue

            paths.append(request_path)

        return paths

    def __getitem__(self, index):
        return self.urls[index]

    def __len__(self):
        return len(self.urls)

    def __iter__(self):
        return iter(self.urls)

    def autoreload(self):
        """
        Attempt to register the page dir with Django's autoreloader
        """
        if trigger_reload_soon is None:
            return

        # Try to register with autoreloader if it's already running
        reloader = get_reloader()
        if reloader is not None:
            reloader.watch_dir(self.path, "**/*")


if trigger_reload_soon is not None:

    @receiver(autoreload_started, dispatch_uid="nanopages_autoreload_started")
    def watch_pages_directories(sender, **kwargs):
        """
        Register all Pages directories with Django's autoreloader
        """
        for pages in registry:
            sender.watch_dir(pages.path, "**/*")

    @receiver(file_changed, dispatch_uid="nanopages_file_changed")
    def nanopages_file_changed(sender, file_path, **kwargs):
        """
        Handle file changes in registered directories
        """
        for pages in registry:
            if file_path.is_relative_to(pages.path):
                # File is in one of our directories, tell django-browser-reload
                trigger_reload_soon()

                # Prevent server restart
                return True

        # Not our file
        return None
