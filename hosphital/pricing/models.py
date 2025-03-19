from django.db import models
# Create your models here.

class treatment_charges(models.Model):
    treatment_name = models.CharField(max_length=50, null=True, blank=True)
    out_patient = models.IntegerField(null=True, blank=True)
    in_patient = models.IntegerField(null=True, blank=True)
    daycare = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    
class lab_charges(models.Model):
    test_name = models.CharField(max_length=50, null=True, blank=True)
    out_patient = models.IntegerField(null=True, blank=True)
    in_patient = models.IntegerField(null=True, blank=True)
    daycare = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    
class consultant_charges(models.Model):
    doctor_speciality = models.CharField(max_length=50, null=True, blank=True)
    out_patient = models.IntegerField(null=True, blank=True)
    in_patient = models.IntegerField(null=True, blank=True)
    daycare = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    
class room_master(models.Model):
    room_type = models.CharField(max_length=50, null=True, blank=True)
    out_patient = models.IntegerField(null=True, blank=True)
    in_patient = models.IntegerField(null=True, blank=True)
    daycare = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    
class change_prices(models.Model):
    rate_plan = models.CharField(max_length=20, null=True, blank=True)
    increase_by_amount = models.BooleanField(default=False)
    decrease_by_amount = models.BooleanField(default=False)
    increase_by_percentage = models.BooleanField(default=False)
    decrease_by_percentage = models.BooleanField(default=False)
    amount = models.FloatField(null=True, blank=True)
    
class hosphital_details(models.Model):
    hosphital_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    
class finance(models.Model):
    field1 = models.CharField(max_length=50, blank=True, null=True)
    field2 = models.CharField(max_length=50, blank=True, null=True)
    field3 = models.CharField(max_length=50, blank=True, null=True)
    field4 = models.CharField(max_length=50, blank=True, null=True)
    
