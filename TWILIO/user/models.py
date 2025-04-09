from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class user(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.IntegerField( null=True, blank=True)