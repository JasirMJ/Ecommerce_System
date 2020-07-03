from django.contrib.auth.models import User
from users.models import Address
from payments.models import TblPayments
from django.db import models
from Shops.models import ShopDetails
from items.models import TblItems
# Create your models here.

class TblStatus(models.Model):
    name = models.CharField(max_length= 50,null= False,blank= False)

class TblOrderDetails(models.Model):

    date = models.DateTimeField(null= True,blank= False)
    shop = models.ForeignKey(ShopDetails,null= False,blank= False,on_delete= models.PROTECT)
    user = models.ForeignKey(User,null= True,blank= False,on_delete= models.PROTECT)
    description = models.CharField(max_length= 500,null= False,blank= False)
    address = models.ForeignKey(Address,null= True,blank= False,on_delete= models.PROTECT,)
    amount = models.FloatField(null= False,blank= False,default= 0)
    payment = models.ForeignKey(TblPayments,null= True,blank= False,on_delete= models.PROTECT)
    status = models.ForeignKey(TblStatus,null= True,blank= False,on_delete= models.PROTECT)
    is_new = models.BooleanField(null= False,blank= False,default= True)
    ref_no = models.CharField(max_length= 100, null= False,blank= False,)

class TblIssuedItems(models.Model):

    order = models.ForeignKey(TblOrderDetails,null= False,blank= False,on_delete= models.CASCADE)
    item = models.ForeignKey(TblItems,null= False,blank= False,on_delete= models.PROTECT)
    qty = models.FloatField(null= False,blank= False,default= 0)
    rate = models.FloatField(null= False,blank= False,default= 0)
    total = models.FloatField(null= False,blank= False,default= 0)
    disc_perc = models.FloatField(null= False,blank= False,default= 0)
    discount = models.FloatField(null= False,blank= False,default= 0)
    net_amt = models.FloatField(null= False,blank= False,default= 0)


class TblStatusHistory(models.Model):

    date = models.DateTimeField(null= False,blank= False)
    order = models.ForeignKey(TblOrderDetails,null= False,blank= False,on_delete= models.CASCADE)
    status = models.ForeignKey(TblStatus,null= False,blank= False,on_delete= models.PROTECT)
    description = models.CharField(max_length= 500,null= False,blank= False)
