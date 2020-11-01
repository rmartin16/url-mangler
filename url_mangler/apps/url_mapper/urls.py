from django.urls import path
from url_mangler.apps.url_mapper.views import CreateSlugView, SlugRedirectView


app_name = "url_mapper"
urlpatterns = [
    path("", CreateSlugView.as_view(), name="create_slug"),
    path("<slug:slug>/", SlugRedirectView.as_view(), name="slug_redirect"),
]
