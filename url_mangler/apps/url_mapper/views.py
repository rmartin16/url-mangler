from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic.edit import FormView

from url_mangler.apps.url_mapper.forms import UrlMappingForm
from url_mangler.apps.url_mapper.uses import GenerateAndSaveSlugMappingUseCase
from url_mangler.apps.url_mapper.uses import RetrieveSlugMappingUseCase


class CreateSlugView(FormView):
    form_class = UrlMappingForm
    template_name = "url_mapper/url_mapping_form.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests. All GET requests are funneled through here."""

        # redirect to the destination URL if valid slug
        if slug := kwargs.get("slug", None):
            if mapping := RetrieveSlugMappingUseCase().retrieve(slug=slug):
                # TODO: perhaps log redirections
                return redirect(mapping.destination_url, permanent=False)

        # if a slug wasn't found or if a non-slug path was provided, send error to user
        if request.path.rstrip("/"):
            messages.error(
                self.request,
                f"Whoops!! That address isn't currently redirected anywhere...",
            )

        # render homepage
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Load form and other data in to context for homepage."""
        context = super().get_context_data(**kwargs)

        # if a mapping was successfully created, pass to template
        if dest_url := self.request.session.get("destination_url"):
            context["destination_url"] = dest_url
            context["slug_url"] = self.request.session["slug_url"]
            if context["slug_url"].startswith("http://"):
                context["slug_url_label"] = context["slug_url"][7:]
            elif context["slug_url"].startswith("https://"):
                context["slug_url_label"] = context["slug_url"][8:]
            else:
                context["slug_url_label"] = context["slug_url"]

        # clear session cache to prevent any bleeding
        self.request.session.pop("destination_url", None)
        self.request.session.pop("slug_url", None)

        return context

    def form_valid(self, form: UrlMappingForm):
        """Create a new mapping and return it to the user"""
        dest_url = form.cleaned_data["destination_url"]
        try:
            mapping = GenerateAndSaveSlugMappingUseCase().save(
                destination_mapping=dest_url
            )
        except Exception as e:
            messages.error(self.request, f"Failed to mangle URL... Error: {repr(e)}")
        else:
            # use the domain information of the current request to build the mangled URL for the user
            slug_url: str = self.request.build_absolute_uri(
                reverse("url_mapper:slug_redirect", args=(mapping.slug,))
            )
            # preserve urls to display to user after submit
            self.request.session["destination_url"] = dest_url
            self.request.session["slug_url"] = slug_url

        return redirect("url_mapper:homepage")
