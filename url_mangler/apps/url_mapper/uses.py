import abc
from datetime import datetime
from typing import Optional

from django.utils.crypto import get_random_string
from django.utils.text import slugify

import attr
from werkzeug.urls import url_fix

from url_mangler.apps.url_mapper.models import UrlMapping


@attr.s(auto_attribs=True)
class SlugMapping:
    """UrlMapping Model abstraction"""

    slug: str
    destination_url: str
    created_at: datetime


class SlugMappingRepo(abc.ABC):
    """Abstract Repository for SlugMappings. This allows for trivial replacement of the database for testing."""

    @classmethod
    @abc.abstractmethod
    def get(cls, slug: str) -> Optional[SlugMapping]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def save(cls, destination_mapping: str) -> SlugMapping:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_slug(cls, destination_mapping: str) -> str:
        raise NotImplementedError


class DjangoSlugMappingRepo(SlugMappingRepo):
    """Django implementation for returning SlugMappings for UrlMappings and saving SlugMappings as UrlMappings."""

    @classmethod
    def get(cls, slug: str) -> Optional[SlugMapping]:
        """Return a SlugMapping for a UrlMapping based on a slug."""
        try:
            mapping: UrlMapping = UrlMapping.objects.get(slug=slug)
            return SlugMapping(
                slug=slug,
                destination_url=mapping.destination_url,
                created_at=mapping.created_at,
            )
        except UrlMapping.DoesNotExist:
            return None

    @classmethod
    def save(cls, destination_mapping: str) -> SlugMapping:
        """Save a destination mapping as a UrlMapping and return the SlugMapping."""
        record = UrlMapping(
            slug=cls.generate_slug(destination_mapping=destination_mapping),
            destination_url=url_fix(destination_mapping),
        )
        record.save()
        return SlugMapping(
            slug=record.slug,
            destination_url=record.destination_url,
            created_at=record.created_at,
        )

    @classmethod
    def generate_slug(cls, destination_mapping: str) -> str:
        """Generate a slug for a destination mapping."""
        while 1:
            slug = slugify(get_random_string().lower())
            if not UrlMapping.objects.filter(slug=slug).exists():
                break
        return slug


class SlugMappingBaseUseCase:
    """Overly abstracted Base Use Case to interact with SlugMappings"""

    def __init__(self, slug_mapping_repo: SlugMappingRepo = DjangoSlugMappingRepo()):
        self._slug_mapping_repo = slug_mapping_repo


class RetrieveSlugMappingUseCase(SlugMappingBaseUseCase):
    """Given an arbitrary slug, retrieve the SlugMapping"""

    def retrieve(self, slug: str) -> Optional[SlugMapping]:
        return self._slug_mapping_repo.get(slug=slug)


class GenerateAndSaveSlugMappingUseCase(SlugMappingBaseUseCase):
    """Given an arbitrary destination mapping, generate, save, and return a SlugMapping"""

    def save(self, destination_mapping: str) -> SlugMapping:
        return self._slug_mapping_repo.save(destination_mapping=destination_mapping)
