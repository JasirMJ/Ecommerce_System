from EcommerceSystem.Imports import *
from .models import TblPayments

def getIsUsed(obj_payment):

    return False


def savePayment(obj_user,transaction_id,transaction_date,transaction_amt,status_str):

    if transaction_id == "":
        return False
    if transaction_date == "":
        return False
    if getFloatOfObject(transaction_amt) <= 0:
        return False
    if status_str == "":
        return False


    obj_payment = TblPayments()
    obj_payment.date = datetime.now()
    obj_payment.user = obj_user
    obj_payment.transaction_id = transaction_id
    obj_payment.transaction_date = transaction_date
    obj_payment.amount = transaction_amt
    obj_payment.status = status_str
    obj_payment.save()

    return obj_payment