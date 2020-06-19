from EcommerceSystem.Imports import *
from .models import *
from users.serializers import UserSerializerSimple

class AddressSerializer(DynamicFieldsModelSerializer):

    class Meta:

        model = ShopAddress
        exclude = ["shop"]

class ShopSerializer(DynamicFieldsModelSerializer):

    address = serializers.SerializerMethodField()
    super_manager = UserSerializerSimple(read_only= True, many= False,)

    class Meta:

        model = ShopDetails
        fields = ["id","shop_name","address","super_manager","is_approved","is_active"]

    def get_address(self,obj):

        qs_address = ShopAddress.objects.filter(shop = obj)

        if qs_address.count() == 0:
            return None

        sr = AddressSerializer(qs_address.first(),many= False)

        return sr.data
