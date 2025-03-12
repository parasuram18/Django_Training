from django.db import models

# Create your models here.

class uploads(models.Model):
    img_url = models.URLField(max_length=200)