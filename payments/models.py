from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TblPayments(models.Model):

    date = models.DateTimeField(null= False,blank= False)
    user = models.ForeignKey(User,null= False,blank= False,on_delete= models.PROTECT)
    transaction_id = models.CharField(max_length= 100,null= False,blank= False)
    transaction_date = models.DateTimeField(null= False,blank= False)
    amount = models.FloatField(null= False,blank= False)
    status = models.CharField(max_length= 300,null= False,blank= False)