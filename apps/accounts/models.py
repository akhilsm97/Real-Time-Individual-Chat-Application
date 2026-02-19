
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_online=False, last_seen=None):
        if not username:
            raise ValueError('The username must be set')
        if not email:
            raise ValueError('The email must be set')

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
        user = self.create_user(
            username=username, 
            email=email,
            password=password
            )
        user.is_admin = True
        user.save(using=self._db)
        return user

        


class CustomUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150, 
        help_text = ("Required. 150 characters or fewer. Letters, and digits only."),
        validators = [username_validator],
        unique=True,
         error_messages = {
            'unique': ("A user with that username already exists."),
        },
        )
    email = models.EmailField(validators=[EmailValidator()],unique=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    




