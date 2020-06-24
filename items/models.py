from django.db import models
from Shops.models import ShopDetails

# Create your models here.

class TblItemCategory(models.Model):

    shop = models.ForeignKey(ShopDetails, null= False,blank= False,on_delete= models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False)
    parent = models.CharField(max_length=10, null=True, blank=False)

class TblBrand(models.Model):

    shop = models.ForeignKey(ShopDetails,null= False,blank= False,on_delete= models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False)

class TblItems(models.Model):

    shop = models.ForeignKey(ShopDetails,null= False,blank= False, on_delete= models.CASCADE)
    name = models.CharField(max_length= 200,null= False, blank= False)
    description = models.CharField(max_length= 200,null= False,blank= False)
    category = models.ForeignKey(TblItemCategory,null= True,blank= False,on_delete= models.SET_NULL)
    brand = models.ForeignKey(TblBrand, null= True,blank= False,on_delete= models.PROTECT)
    rate = models.FloatField(null= False,blank= False,default= 0)
    subcategory = models.ForeignKey(TblItemCategory,null= True,blank= False,on_delete= models.SET_NULL,related_name="subcategory")

class TblInventory(models.Model):

    shop = models.ForeignKey(ShopDetails,null= False,blank= False,on_delete= models.CASCADE)
    date = models.DateTimeField(null= False,blank= False)
    item = models.ForeignKey(TblItems,null= False,blank= False,on_delete= models.CASCADE)
    v_type = models.CharField(max_length= 50,null= False,blank= False)
    ref_no = models.IntegerField(null= False,blank= False)
    in_qty = models.FloatField(null= False,blank= False,default= 0)
    out_qty = models.FloatField(null= False,blank= False,default= 0)