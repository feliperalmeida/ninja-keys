import pytest
from django.test import Client
from test_project.heroes.models import Hero, HeroAPIKey


@pytest.mark.django_db
def test_test_project_routes() -> None:
    batman = Hero.objects.create(name="Batman")
    _, key = HeroAPIKey.objects.create_key(name="test", hero=batman)
    headers = {"HTTP_X-API-Key": key}

    client = Client()

    response = client.get("/api/public", format="json")
    assert response.status_code == 200

    response = client.get("/api/protected", format="json", **headers)
    assert response.status_code == 200

    # response = client.get("/api/protected/object/", format="json", **headers)
    # assert response.status_code == 200


@pytest.mark.django_db
def test_test_project_routes_with_empty_key() -> None:
    headers = {"HTTP_X-API-Key": ""}

    client = Client()

    response = client.get("/api/public", format="json", **headers)
    assert response.status_code == 200

    response = client.get("/api/protected", format="json", **headers)
    assert response.status_code == 401
