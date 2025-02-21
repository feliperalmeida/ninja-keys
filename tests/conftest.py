from django.conf import settings


def pytest_configure() -> None:
    settings.configure(
        **{
            "SECRET_KEY": "abcd",
            "INSTALLED_APPS": [
                # Mandatory
                "django.contrib.contenttypes",
                # Permissions
                "django.contrib.auth",
                # Admin
                "django.contrib.admin",
                "django.contrib.messages",
                "django.contrib.sessions",
                # Project
                "ninja_keys",
                "test_project.heroes",
            ],
            "TEMPLATES": [
                # Admin
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "OPTIONS": {
                        "context_processors": [
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ]
                    },
                }
            ],
            "MIDDLEWARE": [
                # Admin
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
            ],
            "ROOT_URLCONF": "test_project.project.urls",
            "DATABASES": {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                },
                "test": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                },
            },
        }
    )
