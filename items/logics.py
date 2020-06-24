from EcommerceSystem.Imports import *
from .models import TblInventory



def add_Stock(date,obj_shop, obj_item, v_type, ref_no, in_qty = 0, out_qty = 0):

    obj_inventory = TblInventory()

    obj_inventory.date = date
    obj_inventory.shop = obj_shop
    obj_inventory.item = obj_item
    obj_inventory.v_type = v_type
    obj_inventory.ref_no = ref_no
    obj_inventory.in_qty = in_qty
    obj_inventory.out_qty = out_qty
    obj_inventory.save()

    return obj_inventory


def get_stock(obj_item):

    qs = TblInventory.objects.filter(item= obj_item)

    sum_in = getFloatOfObject(qs.aggregate(Sum("in_qty"))["in_qty__sum"])
    sum_out = getFloatOfObject(qs.aggregate(Sum("out_qty"))["out_qty__sum"])

    stock = sum_in - sum_out

    return stock
