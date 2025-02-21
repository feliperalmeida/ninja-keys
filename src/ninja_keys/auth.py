import typing

from ninja.security import APIKeyHeader

from ninja_keys.models import AbstractAPIKey, APIKey


class BaseApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"
    model: typing.Optional[typing.Type[AbstractAPIKey]] = None

    def authenticate(self, request, key):
        if not key:
            return None
        return self.model.objects.is_valid(key)


class ApiKeyAuth(BaseApiKeyAuth):
    model = APIKey
