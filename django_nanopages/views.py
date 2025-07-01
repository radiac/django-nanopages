from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import markdown
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.views import View

if TYPE_CHECKING:
    from .pages import Pages


class Page(View):
    #: Reference to the Pages object for this page
    pages: Pages | None = None

    #: Extra template context for the view; define with Page.as_view(extra_context=...)
    extra_context: dict | None = None

    def get(
        self,
        request,
        request_path: str = "",
        **kwargs,
    ) -> HttpResponse:
        src = self.find_src(request_path)

        if src.suffix == ".md":
            return self.render_md(src)
        else:
            return self.render_html(src)

    def find_src(self, request_path: str) -> Path:
        # Build path stem - we'll look under it the a file
        if not self.pages:
            raise ValueError("Cannot render a Page without an associated Pages object")
        root = self.pages.path
        path_stem = (root / request_path).resolve()

        # Must be relative to the root
        if not path_stem.is_relative_to(root):
            raise Http404()

        # Look for file
        search = [
            path_stem.with_suffix(".html"),
            path_stem.with_suffix(".md"),
            path_stem / "index.html",
            path_stem / "index.md",
        ]
        for file_path in search:
            if file_path.is_file():
                return file_path

        raise Http404()

    def parse_context(self, raw: str) -> tuple[str, dict[str, Any]]:
        """
        Parse context front matter
        """
        context = {
            "base": "base.html",
        }
        if self.extra_context:
            context.update(self.extra_context)

        if not raw.startswith("---"):
            return raw, context

        raw_lines = raw.splitlines()
        try:
            end_index = raw_lines.index("---", 1)
        except ValueError:
            # Not context
            return raw, context

        # Split the context off
        lang = raw_lines[0][3:].strip()
        raw_context = "\n".join(raw_lines[1:end_index])
        raw = "\n".join(raw_lines[end_index + 1 :])

        # Parse it
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
        return raw, context

    def render_md(self, src: Path) -> HttpResponse:
        raw = src.read_text()
        raw, context = self.parse_context(raw)
        context["content"] = markdown.markdown(raw)

        response = render(self.request, "django_nanopages/page.html", context=context)
        response.context_data = context
        return response

    def render_html(self, src: Path) -> HttpResponse:
        # The template isn't in a template dir, so need to read it manually anyway
        raw = src.read_text()
        raw, context = self.parse_context(raw)
        template = Template(raw)
        request_context = RequestContext(self.request, context)
        response = HttpResponse(template.render(request_context))
        response.context_data = context
        return response
