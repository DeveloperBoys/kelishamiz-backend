import uuid
import random
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from rest_framework_simplejwt.tokens import RefreshToken

from .constants import (
    MANAGER,
    VIA_PHONE,
    VIA_SOCIAL,
    SUPER_USER,
    ORDINARY_USER,
)


PHONE_EXPIRE = 2


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


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserConfirmation(models.Model):
    """
    Model to store user verification codes and related information.
    """

    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        """
        Override the save method to set expiration time for phone verification codes.
        """
        if not self.pk:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class User(AbstractUser, BaseModel):
    """
    Custom user model with extended fields and methods.
    """
    _validate_phone = RegexValidator(
        regex=r"^998([378]{2}|(9[013-57-9]))\d{7}$",
        message="Your phone number must be connected with +9 and 12 characters! For example: 998998887766"
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_SOCIAL, VIA_SOCIAL)
    )
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (SUPER_USER, SUPER_USER)
    )

    user_roles = models.CharField(
        max_length=31, choices=USER_ROLES, default=ORDINARY_USER
    )
    auth_type = models.CharField(
        max_length=31, choices=AUTH_TYPE_CHOICES)
    profile_image = models.FileField(
        upload_to='uploads/user', blank=True, null=True
    )
    father_name = models.CharField(
        _("father name"), max_length=150, blank=True
    )
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=13, unique=True, validators=[_validate_phone])
    birth_date = models.DateField(blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def profile_image_url(self):
        if self.profile_image:
            return f"{settings.HOST}{self.profile_image.url}"

    def create_verify_code(self):
        """
        Create and store a verification code for the user.
        """
        code = "".join(
            [str(random.randint(0, 100) % 10) for _ in range(6)])
        UserConfirmation.objects.create(
            user=self, code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f"Kelishamiz-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temp_username):
                temp_username = f'{temp_username}{random.randint(0, 9)}'
            self.username = temp_username

    def check_email(self):
        """
        Normalize the email address to lowercase.
        """
        if self.email:
            self.email = self.email.lower()

    def check_pass(self):
        if not self.password:
            temp_password = f"password{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        """
        Hash the password if not already hashed.
        """
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def tokens(self):
        """
        Generate JWT tokens for the user.
        """
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        """
        Normalize email, hash password the user.
        """
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()
