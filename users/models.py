from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserRoles(models.Model):
    #delivery boy
    #vendor
    name = models.CharField(max_length=20,unique=True)
    is_active = models.BooleanField(default=True)
    status =models.CharField(default="active",max_length=10,choices=[
        ('active', 'active'),
        ('inactive','inactive'),
        ('blocked','blocked')]
    )


class Address(models.Model):
    address1 = models.CharField("Address line 1",max_length=1024,)
    address2 = models.CharField("Address line 2",max_length=1024,null=True)
    land_mark = models.CharField("Land mark",max_length=1024,null=True)
    latitude = models.CharField("Latitude",max_length=255)
    longitude = models.CharField("Latitude",max_length=255)
    zip_code = models.CharField("ZIP / Postal code",max_length=12,)
    city = models.CharField("City",max_length=1024,)
    state = models.CharField("State", max_length=20, )
    country = models.CharField("Country",max_length=20,)


    # country = models.CharField("Country",max_length=3,choices=ISO_3166_CODES,)
class Pages(models.Model):
    name = models.CharField(max_length=255,null=False,unique=True)

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=False,unique=True)
    referance = models.CharField(max_length=6,null=True,default=None)

    created_by = models.ForeignKey(User,on_delete=models.PROTECT,related_name='created_by',null=True,default=None)
    role = models.ManyToManyField(UserRoles)
    address = models.ManyToManyField(Address)
    pages = models.ManyToManyField(Pages)