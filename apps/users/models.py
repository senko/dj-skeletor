from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    verify_code = models.CharField(
        _('verify code'),
        max_length=30,
        null=True,
        blank=True
    )
    email_verified = models.BooleanField(
        _('verified status'),
        default=False,
        help_text=_('Activation email check.')
    )
