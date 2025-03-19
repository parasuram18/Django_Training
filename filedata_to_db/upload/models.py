from django.db import models

# Create your models here.

class speciality_master(models.Model):
    speciality_desc = models.CharField(max_length=50, blank=True, null=True)
    speciality_amount = models.IntegerField(null=True, blank=True)
    speciality_currency = models.CharField(max_length=50, blank=True, null=True)
    speciality_currency_symbol = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    iu_id_id = models.IntegerField(null=True, blank=True)
