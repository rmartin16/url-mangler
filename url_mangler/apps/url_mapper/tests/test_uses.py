from collections import defaultdict
from datetime import datetime
from typing import Optional

import pytest

from url_mangler.apps.url_mapper.uses import GenerateAndSaveSlugMappingUseCase
from url_mangler.apps.url_mapper.uses import RetrieveSlugMappingUseCase
from url_mangler.apps.url_mapper.uses import SlugMapping
from url_mangler.apps.url_mapper.uses import SlugMappingRepo

url = "http://example.com"


class TestSlugMappingRepo(SlugMappingRepo):
    """This is an alternative implementation if pytest didn't make db access so easy"""

    def __init__(self):
        self._db = defaultdict(dict)

    def get(self, slug: str) -> Optional[SlugMapping]:
        if rec := self._db.get(slug):
            return SlugMapping(
                slug=slug,
                destination_url=rec["destination_url"],
                created_at=rec["created_at"],
            )
        return None

    def save(self, destination_mapping: str) -> SlugMapping:
        if destination_mapping:
            now = datetime.now()
            slug = self.generate_slug()
            self._db[slug] = dict(destination_url=destination_mapping, created_at=now)
            return SlugMapping(
                slug=slug, destination_url=destination_mapping, created_at=now
            )

    def generate_slug(self, destination_mapping: str = None) -> str:
        return "1234567890"


@pytest.mark.django_db
def test_generate_and_save_mapping():
    mapping = GenerateAndSaveSlugMappingUseCase().save(destination_mapping=url)

    assert isinstance(mapping, SlugMapping)
    assert mapping.destination_url == url


@pytest.mark.django_db
def test_retrieve_mapping():
    mapping_created = GenerateAndSaveSlugMappingUseCase().save(destination_mapping=url)

    mapping_retrieved = RetrieveSlugMappingUseCase().retrieve(slug=mapping_created.slug)

    assert mapping_created == mapping_retrieved
    assert mapping_retrieved.destination_url == url


@pytest.mark.django_db
def test_retrieve_mapping_fail():
    mapping = RetrieveSlugMappingUseCase().retrieve(slug="")

    assert mapping is None


def test_slug_mapping_repo_interface():
    with pytest.raises(NotImplementedError):
        SlugMappingRepo.get(slug="")

    with pytest.raises(NotImplementedError):
        SlugMappingRepo.save(destination_mapping="")

    with pytest.raises(NotImplementedError):
        SlugMappingRepo.generate_slug(destination_mapping="")
