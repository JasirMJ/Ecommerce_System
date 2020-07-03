from EcommerceSystem.Imports import *
from .models import TblCart
from items.serializer import ItemSerializer

class CartSerializer(DynamicFieldsModelSerializer):

    item = ItemSerializer(many= False,read_only= True)

    class Meta:
        model = TblCart
        fields = ["id","date","item"]
