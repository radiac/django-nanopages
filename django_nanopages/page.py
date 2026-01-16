from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import markdown
from django.urls import reverse

if TYPE_CHECKING:
    from .pages import Pages


class Page:
    """
    Represents a single page, handling file discovery, context parsing, and rendering.
    """

    request_path: str
    pages: Pages
    extra_context: dict
    name: str

    _body: str | None = None
    _context: dict | None = None

    def __init__(
        self,
        request_path: str,
        pages: Pages,
        extra_context: dict[str, Any] | None = None,
    ):
        """
        Initialize a Page with a request path.

        Args:
            request_path: The URL path being requested
            pages: The Pages instance containing configuration and root path
            extra_context: Additional context to merge with page frontmatter
        """
        self.request_path = request_path
        self.pages = pages
        self.extra_context = extra_context or {}
        self.name = request_path.split("/")[-1]

        src = self.find_src()
        if src is not None:
            self.exists = True
            self.src = src
        else:
            self.exists = False
            self.src = Path("")

    @property
    def title(self) -> str:
        title = self.context.get("title", None)
        if title is not None:
            return title
        return self.name.replace("-", " ").replace("_", " ").title()

    def find_src(self) -> Path | None:
        """
        Find the source file for the request path.

        Returns:
            Path to the source file, or None if not found or path is outside root
        """
        # Build path stem - we'll look under it for a file
        path_stem = (self.pages.path / self.request_path).resolve()

        # Must be relative to the root
        if not path_stem.is_relative_to(self.pages.path):
            return None

        # Look for file
        search = [
            Path(f"{path_stem}.html"),
            Path(f"{path_stem}.md"),
            path_stem / "index.html",
            path_stem / "index.md",
        ]
        for file_path in search:
            if file_path.is_file():
                return file_path

        return None

    def read(self, reload=False) -> tuple[str, dict[str, Any]]:
        """
        Read the page file and parse frontmatter context.

        Data is cached on the Page object for its lifetime.

        Args:
            reload: If True, forces a reload

        Returns:
            Tuple of (raw body content without frontmatter, context dict)

        Raises:
            ValueError: If the page doesn't exist
        """
        if not self.exists:
            raise ValueError("Cannot read a page that doesn't exist")

        if reload or not self._body or not self._context:
            self._body, self._context = self._read()

        return self._body, self._context

    def _read(self) -> tuple[str, dict[str, Any]]:
        raw = self.src.read_text()

        # Parse frontmatter
        context = {
            "base": "base.html",
        }
        context.update(self.extra_context)

        if not raw.startswith("---"):
            return raw, context

        raw_lines = raw.splitlines()
        try:
            end_index = raw_lines.index("---", 1)
        except ValueError:
            # Not valid frontmatter
            return raw, context

        # Split the frontmatter off
        lang = raw_lines[0][3:].strip()
        raw_context = "\n".join(raw_lines[1:end_index])
        body = "\n".join(raw_lines[end_index + 1 :])

        # Parse frontmatter based on language
        if lang == "":
            for line in raw_context.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    context[key.strip()] = value.strip()
                else:
                    context[line] = ""

        elif lang == "json":
            context.update(json.loads(raw_context))

        elif lang in ["yml", "yaml"]:
            try:
                import yaml
            except ImportError:
                raise ValueError("Cannot load YAML context, PyYAML is not installed")
            data = yaml.safe_load(raw_context)
            if not isinstance(data, dict):
                raise ValueError("Cannot load YAML context, not a dict")
            context.update(data)

        else:
            raise ValueError(f"Unsupported context language {lang}")

        return body, context

    @property
    def body(self) -> str:
        body = self._body
        if body is None:
            body, _ = self.read()
        return body

    @property
    def context(self) -> dict:
        context = self._context
        if context is None:
            _, context = self.read()
        return context

    def as_html(self) -> str:
        """
        Return the page content as HTML - either render the markdown, or as the raw
        template HTML.

        Returns:
            Rendered HTML content

        Raises:
            ValueError: If the page doesn't exist
        """
        body, context = self.read()

        if self.src.suffix == ".md":
            content = markdown.markdown(body)
        else:
            # For HTML files, the body is already HTML
            content = body

        return content

    def get_absolute_url(self) -> str:
        return reverse(self.pages.name, args=[self.request_path])
