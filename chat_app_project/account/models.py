from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        if not username:
            raise ValueError(_("You must provide an user name"))

        user = self.model(
            email=self.normalize_email(email), 
            username=username,
            is_active=True,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        
        if other_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must be assigned to is_staff=True.")
            )
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must be assigned to is_superuser=True.")
            )
        return self.create_user(email, username, password, **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser and self.is_active

    def has_module_perms(self, app_label):
        return self.is_superuser and self.is_active