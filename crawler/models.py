from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    house_nr = models.IntegerField(blank=True, null=True)
    flat_nr = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, default=None, null=True)
