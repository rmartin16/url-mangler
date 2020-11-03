from bs4 import BeautifulSoup
from django import urls
import pytest
from pytest_django.asserts import assertTemplateUsed

from url_mangler.apps.url_mapper.uses import GenerateAndSaveSlugMappingUseCase

url = "http://example.com"


def test_get_home_page(client):
    resp = client.get(urls.reverse("url_mapper:homepage"))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_get_with_valid_slug(client):
    mapping = GenerateAndSaveSlugMappingUseCase().save(destination_mapping=url)

    resp = client.get(urls.reverse("url_mapper:slug_redirect", args=(mapping.slug,)))
    assert resp.status_code == 302
    assert resp.url == url


@pytest.mark.django_db
def test_get_with_invalid_slug(client):
    resp = client.get(urls.reverse("url_mapper:slug_redirect", args=("234567",)))
    assert resp.status_code == 200
    assertTemplateUsed("url_mapper/url_mapping_form.html")


@pytest.mark.django_db
def test_get_catch_all(client):
    resp = client.get("/asdf/asdf/")
    assert resp.status_code == 200
    assertTemplateUsed("url_mapper/url_mapping_form.html")


@pytest.mark.django_db
def test_submitting_mapping(client):
    resp = client.get(urls.reverse("url_mapper:homepage"))
    soup = BeautifulSoup(resp.content, "html.parser")

    csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    resp = client.post(
        urls.reverse("url_mapper:homepage"),
        data={"csrfmiddlewaretoken": csrf, "destination_url": url},
        follow=True,
    )
    assert resp.status_code == 200
    soup = BeautifulSoup(resp.content, "html.parser")
    mapping_url = soup.find("div", {"id": "id_slug_url"}).a["href"]

    resp = client.get(mapping_url)
    assert resp.url == url
