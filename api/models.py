# from datetime import *
import datetime
from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(email=self.normalize_email(email),
                          is_active=True,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(email, password, is_staff,
                                 is_superuser, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, is_staff=True,
                                 is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=254, blank=True)
    last_name = models.CharField(('last name'), max_length=254, blank=True)
    date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(('is_staff'), default=True)
    phone = models.CharField(("phone"), max_length=11, blank=True)
    primary_user = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        full_name = '%s %s ' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def Info(self):
        return {
            "email": self.email,
            "first_name": self.first_name

        }


class Zone(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notification(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=True)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='from_user')


class Activity(models.Model):
    name = models.CharField(max_length=245)
    description = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Score(models.Model):
    score = models.IntegerField()
    hours = models.IntegerField()
    minitus = models.IntegerField()
    seconds = models.FloatField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Package(models.Model):
    name = models.CharField(max_length=254)
    price = models.IntegerField()
    account = models.IntegerField()
    activity = models.IntegerField()


class Purchasepackage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


class Invitation(models.Model):
    from_to = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
