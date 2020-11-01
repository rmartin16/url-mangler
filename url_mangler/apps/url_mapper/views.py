from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from url_mangler.apps.url_mapper.forms import UrlMappingForm
from url_mangler.apps.url_mapper.uses import GenerateAndSaveSlugMappingUseCase
from url_mangler.apps.url_mapper.uses import RetrieveSlugMappingUseCase


class SlugRedirectView(RedirectView):
    """Redirect aliased URL to destination URL"""

    is_permanent = False

    def get_redirect_url(self, slug: str, *args, **kwargs):
        if record := RetrieveSlugMappingUseCase().retrieve(slug=slug):
            return record.destination_url

        # upon failure, redirect to the homepage with an error
        messages.error(
            self.request,
            f'Whoops!! the URL "{self.request.build_absolute_uri()}" isn\'t redirected anywhere...',
            extra_tags="safe",
        )
        return redirect("url_mapper:create_slug").url


class CreateSlugView(FormView):
    form_class = UrlMappingForm
    template_name = "url_mapper/url_mapping_form.html"

    def get_success_url(self):
        return reverse("url_mapper:create_slug")

    def form_valid(self, form: UrlMappingForm):
        slug_url = form.cleaned_data["destination_url"]
        try:
            mapping = GenerateAndSaveSlugMappingUseCase().save(
                destination_mapping=slug_url
            )
            # use the domain information of the current request to build the mangled URL for the user
            slug_url = self.request.build_absolute_uri(
                reverse("url_mapper:slug_redirect", args=(mapping.slug,))
            )
            messages.success(
                self.request, f"Your mangled URL: {slug_url}", extra_tags="safe"
            )
        except Exception as e:
            messages.error(f"Failed to mangle URL... Error: {repr(e)}")
        return render(
            self.request, self.template_name, context=dict(form=self.form_class())
        )
