from django.contrib.auth.models import User
from django.db import models
# Create your models here.



class ShopDetails(models.Model):

    shop_name = models.CharField(max_length= 100,null= False,blank= False)
    super_manager = models.ForeignKey(User,null= False,blank= False,on_delete= models.PROTECT,related_name= "super_manager")
    is_approved = models.BooleanField(null= False,blank= False)
    is_active = models.BooleanField(null= False,blank= False)


class ShopAddress(models.Model):

    shop = models.ForeignKey(ShopDetails,null= False,blank= False,on_delete= models.CASCADE)
    place = models.CharField(max_length= 100,null= False,blank= False)
    city = models.CharField(max_length= 100,null= False,blank= False)
    pin = models.CharField(max_length= 10,null= False,blank= False)
    district = models.CharField(max_length= 100,null= False,blank= False)
    state = models.CharField(max_length= 100,null= False,blank= False)
    latitude = models.CharField(max_length= 100,null= True,blank= False)
    longitude = models.CharField(max_length= 100,null= True,blank= False)