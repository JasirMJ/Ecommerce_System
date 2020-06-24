from EcommerceSystem.Imports import *
from .models import TblItemCategory, TblItems
from .models import TblBrand
from .logics import get_stock

class ParentSerializer(serializers.ModelSerializer):

    class Meta:

        model = TblItemCategory
        fields = ["id","name",]


class ItemCategorySerializer(DynamicFieldsModelSerializer):

    parent = serializers.SerializerMethodField()

    class Meta:

        model = TblItemCategory
        fields = ["id","name","parent"]

    def get_parent(self,obj):

        print(obj)

        if obj.parent == None:
            return None

        obj_parent = TblItemCategory.objects.get(id= obj.parent)

        sr = ParentSerializer(obj_parent,many= False)

        return sr.data


class BrandSerializer(DynamicFieldsModelSerializer):

    class Meta:

        model = TblBrand
        fields = ["id","name"]


class ItemSerializer(DynamicFieldsModelSerializer):

    category = ItemCategorySerializer(many= False, read_only= True,exclude= ["parent"])
    subcategory = ItemCategorySerializer(many= False, read_only= True,exclude= ["parent"])
    brand = BrandSerializer(many= False, read_only= True)


    class Meta:

        model = TblItems
        fields = ["id","name","description","category","subcategory","brand","rate"]


class ItemSerializerWithStock(DynamicFieldsModelSerializer):

    category = ItemCategorySerializer(many= False, read_only= True,exclude= ["parent"])
    subcategory = ItemCategorySerializer(many= False, read_only= True,exclude= ["parent"])
    brand = BrandSerializer(many= False, read_only= True)
    stock = serializers.SerializerMethodField()

    class Meta:

        model = TblItems
        fields = ["id","name","description","category","subcategory","brand","rate","stock"]


    def get_stock(self,obj):

        return get_stock(obj)