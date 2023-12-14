from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from .constants import (
    SUPER_USER,
    ORDINARY_USER,
)


class UserManager(BaseUserManager):
    """
    Custom user manager for User model.
    """

    def create_user(self, phone_number, password=None, user_roles=ORDINARY_USER, **extra_fields):
        """Create and save a regular User with the given phone number and password."""
        if not phone_number:
            raise ValueError(_('The phone number must be set.'))

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, user_roles, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_roles', SUPER_USER)
        return self._create_user(phone_number, password, **extra_fields)

    def _create_user(self, phone_number, password, user_roles, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone number must be set.'))

        user = self.model(phone_number=phone_number,
                          user_roles=user_roles, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
