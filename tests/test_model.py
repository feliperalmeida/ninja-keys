import datetime as dt
import string

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import override_settings
from test_project.heroes.models import Hero, HeroAPIKey

from ninja_keys.models import APIKey

from .dateutils import NOW, TOMORROW, YESTERDAY

pytestmark = pytest.mark.django_db


def test_key_generation() -> None:
    api_key, generated_key = APIKey.objects.create_key(name="test")
    prefix = api_key.prefix
    hashed_key = api_key.hashed_key

    assert prefix and hashed_key

    charset = set(string.ascii_letters + string.digits + ".")
    assert all(c in charset for c in generated_key)

    # The generated key must be valid…
    assert api_key.is_valid(generated_key) is True

    # But not the hashed key.
    assert api_key.is_valid(hashed_key) is False


def test_name_is_required() -> None:
    with pytest.raises(IntegrityError):
        APIKey.objects.create()


def test_cannot_unrevoke() -> None:
    api_key, _ = APIKey.objects.create_key(name="test", revoked=True)

    # Try to unrevoke the API key programmatically.
    api_key.revoked = False

    with pytest.raises(ValidationError):
        api_key.save()

    with pytest.raises(ValidationError):
        api_key.clean()


@pytest.mark.parametrize(
    "expiry_date, has_expired",
    [(None, False), (NOW, True), (TOMORROW, False), (YESTERDAY, True)],
)
def test_has_expired(expiry_date: dt.datetime, has_expired: bool) -> None:
    api_key, _ = APIKey.objects.create_key(name="test", expiry_date=expiry_date)
    assert api_key.has_expired is has_expired


def test_timezone_naive_with_use_tz_true() -> None:
    with pytest.raises(ValidationError):
        APIKey.objects.create_key(name="test", expiry_date=dt.datetime.now(tz=None))


@override_settings(USE_TZ=False)
def test_timezone_aware_with_use_tz_false() -> None:
    with pytest.raises(ValueError):
        APIKey.objects.create_key(
            name="test", expiry_date=dt.datetime.now(tz=dt.timezone.utc)
        )


def test_custom_api_key_model() -> None:
    hero = Hero.objects.create()
    hero_api_key, generated_key = HeroAPIKey.objects.create_key(name="test", hero=hero)
    assert hero_api_key.is_valid(generated_key)
    assert hero_api_key.hero.id == hero.id
    assert hero.api_keys.first() == hero_api_key


@pytest.mark.django_db
def test_api_key_manager_get_from_key() -> None:
    api_key, generated_key = APIKey.objects.create_key(name="test")
    retrieved_key = APIKey.objects.get_from_key(generated_key)
    assert retrieved_key == api_key


@pytest.mark.django_db
def test_api_key_manager_get_from_key_missing_key() -> None:
    with pytest.raises(APIKey.DoesNotExist):
        APIKey.objects.get_from_key("foobar")


@pytest.mark.django_db
def test_api_key_manager_get_from_key_invalid_key() -> None:
    api_key, generated_key = APIKey.objects.create_key(name="test")
    prefix, _, _ = generated_key.partition(".")
    invalid_key = f"{prefix}.foobar"
    with pytest.raises(APIKey.DoesNotExist):
        APIKey.objects.get_from_key(invalid_key)


def test_api_key_str() -> None:
    _, generated_key = APIKey.objects.create_key(name="test")
    retrieved_key = APIKey.objects.get_from_key(generated_key)
    assert str(retrieved_key) == "test"


@pytest.mark.django_db
def test_api_key_manager_is_valid_missing_key() -> None:
    assert APIKey.objects.is_valid("foobar") is False


@pytest.mark.django_db
def test_api_key_manager_is_valid_expired_key() -> None:
    _, key = APIKey.objects.create_key(name="test", expiry_date=YESTERDAY)
    assert APIKey.objects.is_valid(key) is False
