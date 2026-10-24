# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
#   "django-browser-reload",
#   "django-distill",
# ]
# ///
#
# Run with:
#
#    git clone https://github.com/radiac/django-nanopages.git
#    cd django-nanopages/example
#    uv run website.py
#
# Build to a static site with django-distill:
#
#    uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
#
from django.db import models
from django.views.generic import DetailView, ListView
from nanodjango import Django

app = Django(
    EXTRA_APPS=["django_style"],
)

# Register our blog post model and views before registering django-nanopages - as with
# standard Django urls.py, order of URL definition matters


@app.admin(list_display=["title", "created"], prepopulated_fields={"slug": ("title",)})
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


@app.path("blog/", name="post_list", distill=True)
class PostList(ListView):
    model = Post


@app.path(
    "blog/<slug:slug>/",
    name="post_detail",
    distill_func=lambda: list(Post.objects.values_list("slug", flat=True)),
)
class PostDetail(DetailView):
    model = Post


app.templates = {
    "website/post_list.html": """
        {% extends "base.html" %}
        {% block content %}
          <h1>Blog</h1>
          {% for post in object_list %}
            <h2><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a></h2>
          {% empty %}
            <p>No posts yet.</p>
          {% endfor %}
        {% endblock %}
    """,
    "website/post_detail.html": """
        {% extends "base.html" %}
        {% block content %}
          <p><a href="{% url 'post_list' %}">All posts</a></p>
          <h1>{{ object.title }}</h1>
          <p>{{ object.created|date:"j M Y" }}</p>
          {{ object.body|linebreaks }}
        {% endblock %}
    """,
}

# Now register django-nanopages as a catch-all for any URLs not already matched
app.pages("/", path="pages", context={"site_title": "nanopages example"})


if __name__ == "__main__":
    app.invoke(default="run")
