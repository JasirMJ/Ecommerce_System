from django.db import models

# Create your models here.

class TblAccountGroups(models.Model):

    name = models.CharField(max_length= 200,null= False,blank= False,unique= True)
    parent = models.ForeignKey('self', null= True,blank= False,on_delete= models.PROTECT)

class TblAccounts(models.Model):

    name = models.CharField(max_length= 200,null= False,blank= False)
    description = models.CharField(max_length= 300, null= True,blank= True)
    group = models.ForeignKey(TblAccountGroups,null= False,blank= False,on_delete= models.PROTECT)


class TblGeneralLedger(models.Model):

    ref_no = models.CharField(max_length= 50,null= False,blank= False)
    transaction_type = models.CharField(max_length= 100,null= False,blank= False)
    account = models.ForeignKey(TblAccounts,null= False,blank= False,on_delete= models.PROTECT)
    db_amt = models.FloatField(null= False,blank= False,default= 0)
    cr_amt = models.FloatField(null= False,blank= False,default= 0)
    discription = models.CharField(max_length= 300, null= True,blank= True)

