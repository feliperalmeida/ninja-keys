from ninja_keys.auth import ApiKeyAuth
from test_project.heroes.models import HeroAPIKey


class HeroAPIKeyAuth(ApiKeyAuth):
    model = HeroAPIKey
