from pathlib import Path

from django.urls import URLResolver, include, path, re_path

from .views import Page


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
                Name of this group of pages. Used for reverse URL lookups.
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
                        r"^(?P<request_path>.*)/$",
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
                    r"^(?P<request_path>.*)/$",
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
