from django.db import models
from django.contrib.auth.models import User
from items.models import TblItems

# Create your models here.

class TblCart(models.Model):

    user = models.ForeignKey(User,null= False,blank= False,on_delete= models.CASCADE)
    date = models.DateTimeField(null= False,blank= False)
    item = models.ForeignKey(TblItems,null= False,blank= False,on_delete= models.CASCADE)
