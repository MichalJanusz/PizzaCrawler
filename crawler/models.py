from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Adress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=128, blank=True)
    street = models.CharField(max_length=256, blank=True)
    house_nr = models.IntegerField(blank=True)
    flat_nr = models.IntegerField(blank=True)
