import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import is_naive
from django.utils.translation import gettext_lazy as _


def validate_timezone_aware(value: datetime.datetime) -> None:
    if settings.USE_TZ and is_naive(value):
        raise ValidationError(
            _("The expiry date must be timezone aware when USE_TZ is True.")
        )
