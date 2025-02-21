from datetime import timedelta

from django.utils import timezone

NOW = timezone.now()
TOMORROW = NOW + timedelta(days=1)
YESTERDAY = NOW - timedelta(days=1)
