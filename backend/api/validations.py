from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_list(value):
    if value:
        raise ValidationError(
          _("Полу Ингредиенты н может быть пустым")
        )
