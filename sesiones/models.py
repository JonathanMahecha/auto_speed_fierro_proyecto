from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    # Agrega campos adicionales aquí
    age = models.IntegerField(null=True, blank=True)
    identification = models.CharField(max_length=20, null=True, blank=True)
    cellphone_number = models.CharField(max_length=20, null=True, blank=True)

