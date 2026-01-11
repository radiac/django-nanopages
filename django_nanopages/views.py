from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.views import View

from .page import Page

if TYPE_CHECKING:
    from .pages import Pages


class PageView(View):
    """
    Django view for rendering pages.
    """

    #: Reference to the Pages object for this page
    pages: Pages | None = None

    #: Extra template context for the view; define with PageView.as_view(extra_context=...)
    extra_context: dict | None = None

    def get(
        self,
        request,
        request_path: str = "",
        **kwargs,
    ) -> HttpResponse:
        if not self.pages:
            raise ValueError("Cannot render a Page without an associated Pages object")

        # Get the page using Pages.get_page
        page = self.pages.get_page(request_path)
        if page is None:
            raise Http404()

        if page.src.suffix == ".md":
            return self.render_md(page)
        else:
            return self.render_html(page)

    def render_md(self, page: Page) -> HttpResponse:
        context = page.context
        context["page"] = page
        context["content"] = page.as_html()

        return render(self.request, "django_nanopages/page.html", context=context)

    def render_html(self, page: Page) -> HttpResponse:
        # The template isn't in a template dir, so need to read it manually anyway
        context = page.context
        context["page"] = page

        template = Template(page.as_html())
        request_context = RequestContext(self.request, context)
        return HttpResponse(template.render(request_context))
