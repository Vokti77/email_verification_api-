from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    contract = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email
