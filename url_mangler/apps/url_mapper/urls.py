from django.urls import path, re_path
from url_mangler.apps.url_mapper.views import CreateSlugView


app_name = "url_mapper"
urlpatterns = [
    path("", CreateSlugView.as_view(), name="create_slug"),
    path("<slug:slug>/", CreateSlugView.as_view(), name="slug_redirect"),
    re_path(r"^.*/$", CreateSlugView.as_view(), name="catch_all"),
]
