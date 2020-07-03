from EcommerceSystem.Imports import *
from .models import TblAccountGroups
from .models import TblAccounts
from .models import TblGeneralLedger

def saveOrFetchGroups(name,obj_parent= None):

    qs = TblAccountGroups.objects.filter(name= name)
    if qs.count() > 0:
        return qs.first()

    obj_group = TblAccountGroups()
    obj_group.name = name
    obj_group.parent = obj_parent
    obj_group.save()

    return obj_group

def saveOrFetchAccounts(name,obj_group,description):

    qs = TblAccounts.objects.filter(name= name)
    if qs.count() > 0:
        return qs.first()

    obj_account = TblAccounts()
    obj_account.name = name
    obj_account.group = obj_group
    obj_account.description = description
    obj_account.save()

    return obj_account

def addDefaultGroups():

    grp_customer = saveOrFetchGroups("customer",None)
    grp_shop = saveOrFetchGroups("shop",None)
    grp_bank = saveOrFetchGroups("bank",None)
    grp_cash = saveOrFetchGroups("cash",None)
    grp_expense = saveOrFetchGroups("expense",None)
    grp_income = saveOrFetchGroups("income",None)
    grp_direct_expense = saveOrFetchGroups("direct expense",grp_expense)
    grp_direct_income = saveOrFetchGroups("direct income",grp_income)
    grp_indirect_expense = saveOrFetchGroups("indirect expense", grp_expense)
    grp_indirect_income = saveOrFetchGroups("indirect income", grp_income)

def addDefaultAccounts():

    grp_bank = saveOrFetchGroups("bank")
    acc_bank = saveOrFetchAccounts("bank",grp_bank,"auto_generated")

    grp_cash = saveOrFetchGroups("cash")
    acc_cash = saveOrFetchAccounts("cash",grp_cash,"auto_generated")

    grp_direct_income = saveOrFetchGroups("direct income")
    acc_order = saveOrFetchAccounts("order",grp_direct_income,"auto_generated")

def saveDebit(ref_no,transaction_type,obj_db_account,amount,discription):

    obj_debit = TblGeneralLedger()
    obj_debit.ref_no = ref_no
    obj_debit.transaction_type = transaction_type
    obj_debit.account = obj_db_account
    obj_debit.db_amt = float(amount)
    obj_debit.cr_amt = 0.00
    obj_debit.discription = discription
    obj_debit.save()
    print("debit recorded")
    return obj_debit

def saveCredit(ref_no,transaction_type,obj_cr_account,amount,discription):

    obj_credit = TblGeneralLedger()
    obj_credit.ref_no = ref_no
    obj_credit.transaction_type = transaction_type
    obj_credit.account = obj_cr_account
    obj_credit.db_amt = 0.00
    obj_credit.cr_amt = float(amount)
    obj_credit.discription = discription
    obj_credit.save()
    print("credit recorded")
    return obj_credit


def saveTransaction(ref_no,transaction_type,obj_db_account,obj_cr_account,amount,discription):

    dic = {}
    lst = []

    try:

        obj_debit = saveDebit(ref_no,transaction_type,obj_db_account,amount,discription)
        lst.append(obj_debit)
        obj_credit = saveCredit(ref_no,transaction_type,obj_cr_account,amount,discription)
        lst.append(obj_credit)
        print("transaction saved")


        dic["debit"] = obj_debit
        dic["credit"] = obj_credit

        return dic

    except Exception as e:
        print("Exception occured : " + str(e))
        for i in lst:
            i.delete()

        return False

def get_balance(obj_account):

    qs = TblGeneralLedger.objects.filter(account= obj_account)
    db = getFloatOfObject(qs.aggregate(Sum("db_amt"))["db_amt__sum"])
    cr = getFloatOfObject(qs.aggregate(Sum("cr_amt"))["cr_amt__sum"])
    balance = db - cr

    return balance

def refreshAccountsModels():

    addDefaultGroups()
    addDefaultAccounts()