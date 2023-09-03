import uuid
import random
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, UserManager

from rest_framework_simplejwt.tokens import RefreshToken


ORDINARY_USER, SUPER_USER = (
    "ordinary_user",
    "super_user"
)

VIA_PHONE, VIA_GOOGLE, VIA_TELEGRAM, VIA_APPLE = (
    "via_phone",
    "via_google",
    "via_telegram",
    "via_apple"
)

NEW, CODE_VERIFIED, DONE = (
    "NEW",
    "CODE_VERIFIED",
    "DONE"
)

PHONE_EXPIRE = 2


class UserManagerWithRandomUsername(UserManager):
    """
    Custom user manager that generates random usernames if not provided.
    """

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            username = self.generate_random_username()
        return super().create_user(username, email, password, **extra_fields)

    @staticmethod
    def generate_random_username():
        temp_username = f"SurxonBazar-{uuid.uuid4().hex[:8]}"
        while User.objects.filter(username=temp_username).exists():
            temp_username += str(random.randint(0, 9))
        return temp_username


class UserConfirmation(models.Model):
    """
    Model to store user verification codes and related information.
    """
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_GOOGLE, VIA_GOOGLE),
        (VIA_TELEGRAM, VIA_TELEGRAM),
        (VIA_APPLE, VIA_APPLE)
    )

    code = models.CharField(max_length=4)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='verify_codes')
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        """
        Override the save method to set expiration time for phone verification codes.
        """
        if not self.pk and self.verify_type == VIA_PHONE:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class User(AbstractUser):
    """
    Custom user model with extended fields and methods.
    """
    _validate_phone = RegexValidator(
        regex=r"^\+998([378]{2}|(9[013-57-9]))\d{7}$",
        message="Your phone number must be connected with 9 and 12 characters! For example: 998998887766"
    )
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (SUPER_USER, SUPER_USER)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_GOOGLE, VIA_GOOGLE),
        (VIA_TELEGRAM, VIA_TELEGRAM),
        (VIA_APPLE, VIA_APPLE)
    )

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user_roles = models.CharField(
        max_length=31, choices=USER_ROLES, default=ORDINARY_USER
    )
    auth_status = models.CharField(
        max_length=31, choices=AUTH_STATUS, default=NEW)
    profile_image = models.FileField(
        upload_to='uploads/user', blank=True, null=True
    )
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=12, unique=True, validators=[_validate_phone])
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManagerWithRandomUsername()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def profile_image_url(self):
        if self.profile_image:
            return f"{settings.HOST}{self.profile_image.url}"

    def create_verify_code(self, verify_type):
        """
        Create and store a verification code for the user.
        """
        code = "".join(str(random.randint(0, 9)) for _ in range(4))
        UserConfirmation.objects.create(
            user=self,
            verify_type=verify_type,
            code=code
        )
        return code

    def check_email(self):
        """
        Normalize the email address to lowercase.
        """
        if self.email:
            self.email = self.email.lower()

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
        """
        Normalize email, hash password, and then save the user.
        """
        self.check_email()
        self.hashing_password()
        super(User, self).save(*args, **kwargs)
