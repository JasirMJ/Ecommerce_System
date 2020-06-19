from .models import User
from .models import UserRoles
from Shops.models import ShopDetails
from EcommerceSystem.global_variables import *

def getRoleDetails(obj_shop,obj_user):

    dic = {}

    if obj_shop.super_manager == obj_user:

        # shop owner have all the permissions
        dic[DELIVERY] = True
        dic[ORDER_MANAGEMENT] = True
        dic[STOCK_MANAGEMENT] = True

        return dic


    # fetching roles of non shop manager user
    qs_roll = UserRoles.objects.filter(shop = obj_shop).filter(user= obj_user)


    # checking whether the user have delivery management permissions
    if qs_roll.filter(roll= DELIVERY).count() > 0:
        dic[DELIVERY] = True
    else:
        dic[DELIVERY] = False


    # checking whether the user have order management permissions
    if qs_roll.filter(roll= ORDER_MANAGEMENT).count() > 0:
        dic[ORDER_MANAGEMENT] = True
    else:
        dic[ORDER_MANAGEMENT] = False


    # checking whether the user have stock management permissions
    if qs_roll.filter(roll= STOCK_MANAGEMENT).count() > 0:
        dic[STOCK_MANAGEMENT] = True
    else:
        dic[STOCK_MANAGEMENT] = False


    # returning the generated dictionary
    return dic