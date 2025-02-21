from django.contrib import admin

from ninja_keys.admin import APIKeyModelAdmin

from .models import Hero, HeroAPIKey


@admin.register(HeroAPIKey)
class HeroAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


@admin.register(Hero)
class HeroModelAdmin(admin.ModelAdmin):
    pass
