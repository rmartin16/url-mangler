from datetime import datetime

import pytest

from url_mangler.apps.url_mapper.models import UrlMapping
from url_mangler.apps.url_mapper.apps import UrlMapperConfig


@pytest.mark.django_db
def test_url_mapping_create():
    slug = "zxcvasdfwer"
    url = "http://example.com"

    mapping = UrlMapping(slug=slug, destination_url=url)
    assert isinstance(mapping, UrlMapping)

    mapping.save()
    assert mapping.slug == slug
    assert mapping.destination_url == url
    assert isinstance(mapping.created_at, datetime)


def test_app():
    assert UrlMapperConfig.name == "url_mapper"
