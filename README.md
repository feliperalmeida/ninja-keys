# ninja-keys

[![PyPI version](https://badge.fury.io/py/ninja-keys.svg)](https://badge.fury.io/py/ninja-keys)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/ninja-keys.svg)](https://pypi.python.org/pypi/ninja-keys/)
[![tests](https://github.com/feliperalmeida/ninja-keys/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/feliperalmeida/ninja-keys/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/feliperalmeida/ninja-keys/graph/badge.svg?token=F8O6BPUYPH)](https://codecov.io/github/feliperalmeida/ninja-keys)

API Keys for Django Ninja. 🔐

Based on [djangorestframework-api-key](https://github.com/florimondmanca/djangorestframework-api-key).

## Introduction

This package provides a simple and secure way to add API keys to your Django Ninja APIs.

You can easily customize API keys to your needs, such as tying them to specific users or organizations, setting
expiration dates, and more.

## Quickstart

Install the package using pip:

```bash
pip install ninja-keys
```

Add `ninja_keys` to your `INSTALLED_APPS` in your Django project's settings file:

```python
INSTALLED_APPS = [
    ...
    "ninja_keys",
]
```

Run the migrations:

```bash
python manage.py migrate
```

## Usage

### API Key creation

API keys can be created via the Django admin interface (/admin) or programmatically via the `.create_key()` method on
`APIKey` objects. By doing this, you'll have only one-time access to the key. Once it's hashed and stored, you cannot
access the raw key anymore.

```python
from ninja_keys.models import APIKey

api_key, key = APIKey.objects.create_key(name="my-remote-service")
# Proceed with `api_key` and `key`... The `key` value is the raw key that should be provided to the client.
```

### API Key authentication

API keys can be used to authenticate requests to your API. To do this, you'll need to add the `ApiKeyAuth` class to
your API's `auth` attribute. It can be added globally or per view/router.

```python
from ninja_keys.auth import ApiKeyAuth

# global
api = NinjaAPI(auth=ApiKeyAuth())
```

```python
from ninja_keys.auth import ApiKeyAuth


# Per view/router
@api.get("/protected", auth=ApiKeyAuth())
def protected(request):
    return "Hello, protected!"
```

#### Requests with API keys

To make requests with an API key, you'll need to send the key in the `X-API-Key` header.

```bash
# Using curl
curl -X GET -H "X-API-Key: my-api-key" http://localhost:8000/api/protected

# Using HTTPie
http http://localhost:8000/api/protected X-API-Key:"my-api-key"
```

By default, the API key is required to be sent in the `X-API-Key` header. You can change this behavior by overriding
the `param_name` attribute on the `ApiKeyAuth` class.

```python
class MyApiKeyAuth(ApiKeyAuth):
    param_name = "Api-Key"
```

