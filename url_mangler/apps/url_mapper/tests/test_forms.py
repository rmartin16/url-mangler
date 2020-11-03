from url_mangler.apps.url_mapper.forms import UrlMappingForm


def test_url_form_structure():
    form = UrlMappingForm()
    assert "destination_url" in form.fields
