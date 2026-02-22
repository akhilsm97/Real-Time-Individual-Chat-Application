from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
     Manager for the CustomUser model.

    offers helper methods for handling normalization and default field values,
    as well as for creating regular users and superusers.
    """

    def create_user(
        self, username, email, password=None, is_online=False, last_seen=None
    ):
        """
        Create and return a regular user.

        Args:
            username (str): Unique username for the user.
            email (str): User's email address.
            password (str, optional): Raw password to set for the user.
            is_online (bool, optional): Online status flag. Defaults to False.
            last_seen (datetime, optional): Last seen timestamp. Defaults to now.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If username or email is not provided.
        """
        if not username:
            raise ValueError("The username must be set")
        if not email:
            raise ValueError("The email must be set")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        if last_seen is None:
            last_seen = timezone.now()

        user = self.model(
            username=username,
            email=email,
            is_online=is_online,
            last_seen=last_seen,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Create and return a superuser with full permissions.

        Args:
            username (str): Unique username for the superuser.
            email (str): Superuser's email address.
            password (str, optional): Raw password to set for the superuser.

        Returns:
            CustomUser: The created superuser instance.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.

    Uses `username` as the primary identifier instead of Django's default
    `username` field on the built-in User model. Includes additional fields
    for online status and last seen tracking.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150, validators=[username_validator], unique=True
    )

    email = models.EmailField(validators=[EmailValidator()], unique=True)

    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        """
        Generate a user-friendly string that represents the user.
        """
        return str(self.username)
