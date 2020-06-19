from django.contrib.auth.models import User
from django.db import models
from Shops.models import ShopDetails

# Create your models here.

class UserRoles(models.Model):
    #delivery boy
    #vendor
    user = models.ForeignKey(User,null= False,blank= False,on_delete= models.CASCADE)
    shop = models.ForeignKey(ShopDetails,null= False,blank= False,on_delete= models.CASCADE)
    role = models.CharField(max_length= 50,unique= True,choices= [
        ("delivery","delivery"),
        ("order_management","order_management"),
        ("stock_management","stock_management")]
    )
    is_active = models.BooleanField(default= True)


class Address(models.Model):
    user  = models.ForeignKey(User,null= False,blank= False,on_delete= models.CASCADE)
    address1 = models.CharField("Address line 1",max_length=1024,)
    address2 = models.CharField("Address line 2",max_length=1024,null=True)
    land_mark = models.CharField("Land mark",max_length=1024,null=True)
    latitude = models.CharField("Latitude",max_length=255)
    longitude = models.CharField("Latitude",max_length=255)
    zip_code = models.CharField("ZIP / Postal code",max_length=12,)
    city = models.CharField("City",max_length=1024,)
    state = models.CharField("State", max_length=20, )
    country = models.CharField("Country",max_length=20,)


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=False,unique=True)
    referance = models.CharField(max_length=6,null=True,default=None)
