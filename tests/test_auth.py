import datetime
from typing import Callable

import pytest
from ninja import NinjaAPI
from ninja.responses import Response
from ninja.testing import TestClient

from ninja_keys.auth import ApiKeyAuth, BaseApiKeyAuth
from ninja_keys.models import APIKey
from tests.dateutils import NOW, TOMORROW

pytestmark = pytest.mark.django_db

api = NinjaAPI(version="2.0.0", auth=ApiKeyAuth())


@api.get("/test/")
def test_endpoint(request) -> Response:
    return Response(data={})


class ApiKeyWithoutXAuth(BaseApiKeyAuth):
    param_name = "Api-Key"
    model = APIKey


@api.get("/test_no_x/", auth=ApiKeyWithoutXAuth())
def test_new(request) -> Response:
    return Response(data={})


client = TestClient(api)


def test_if_valid_api_key_then_permission_granted() -> None:
    _, key = APIKey.objects.create_key(name="test")
    headers = {"X-API-Key": key}
    response = client.get("/test/", headers=headers)
    assert response.status_code == 200


def test_if_no_api_key_then_permission_denied() -> None:
    response = client.get("/test/")
    assert response.status_code == 401


def _scramble_prefix(key: str) -> str:
    prefix, _, secret_key = key.partition(".")
    truncated_prefix = prefix[:-1]
    return truncated_prefix + "." + secret_key


@pytest.mark.parametrize(
    "modifier",
    [
        lambda _: "",
        lambda _: "abcd",
        lambda _: "foo.bar",
        lambda key: " " + key,
        lambda key: key.upper(),
        lambda key: key.lower(),
        lambda key: _scramble_prefix(key),
    ],
)
def test_if_invalid_api_key_then_permission_denied(
    modifier: Callable[[str], str],
) -> None:
    _, key = APIKey.objects.create_key(name="test")
    headers = {"X-API-Key": modifier(key)}
    response = client.get("/test/", headers=headers)
    assert response.status_code == 401


def test_if_revoked_then_permission_denied() -> None:
    _, key = APIKey.objects.create_key(name="test", revoked=True)
    headers = {"X-API-Key": key}
    response = client.get("/test/", headers=headers)
    assert response.status_code == 401


TWO_DAYS_AGO = NOW - datetime.timedelta(days=2)


@pytest.mark.parametrize("expiry_date, ok", [(TOMORROW, True), (TWO_DAYS_AGO, False)])
def test_expiry_date(expiry_date: datetime.datetime, ok: bool) -> None:
    _, key = APIKey.objects.create_key(name="test", expiry_date=expiry_date)
    headers = {"X-API-Key": key}
    response = client.get("/test/", headers=headers)

    status_code = 200 if ok else 401
    assert response.status_code == status_code


def test_auth_param_name_override() -> None:
    _, key = APIKey.objects.create_key(name="test")
    headers = {"Api-Key": key}
    response = client.get("/test_no_x/", headers=headers)

    assert response.status_code == 200


def test_auth_param_name_override_with_x() -> None:
    _, key = APIKey.objects.create_key(name="test")
    headers = {"X-Api-Key": key}
    response = client.get("/test_no_x/", headers=headers)

    assert response.status_code == 401
