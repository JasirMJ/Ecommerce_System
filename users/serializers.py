from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from .models import *

from EcommerceSystem.Imports import *

User._meta.get_field('email')._unique = True

class UserSerializerSimple(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('groups','user_permissions')



class UserRolesSerializers(serializers.ModelSerializer):

    user = UserSerializers()

    class Meta:
        model = UserRoles
        fields = '__all__'

class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'



class UserDetailsSerializers(serializers.ModelSerializer):

    user = UserSerializers(read_only= True,many= False)

    class Meta:
        model = UserDetails
        fields = '__all__'

# class AdvancedUserSerializers(serializers.ModelSerializer):
#     # password = serializers.CharField(write_only=True)
#     class Meta:
#         model = UserDetails
#         fields = '__all__'