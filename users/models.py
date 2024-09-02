from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


STATE = (
    ("received", "Qabul qilindi"),
    ("rejected", "Rad etildi"),
    ("optional", "Ixtiyoriy"),
    ("admin", "Admin"),
)


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=100, choices=STATE, null=True, blank=True, default="admin")

    objects = UserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
