import pytest
from django_test_migrations.migrator import Migrator

pytestmark = pytest.mark.skipif(
    Migrator is None,
    reason="django-test-migrations is not available",
)


@pytest.mark.django_db
def test_migrations_0001_initial(migrator: Migrator) -> None:
    old_state = migrator.apply_initial_migration(("ninja_keys", None))

    with pytest.raises(LookupError):
        old_state.apps.get_model("ninja_keys", "APIKey")

    new_state = migrator.apply_tested_migration(("ninja_keys", "0001_initial"))
    APIKey = new_state.apps.get_model("ninja_keys", "APIKey")
    assert APIKey.objects.count() == 0
