from .global_variables import *
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.logics import getRoleDetails

import json


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework import serializers
from django.db.models import Sum
from datetime import datetime

#=======================================================================

STR_ANONYMOUS_USER = "AnonymousUser"
STR_USER = "user"
STR_USER_DET = "user_det"
STR_IS_REGISTERED = "is_rgd"
STR_IS_SUPER_USER = "is_superuser"

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        request = kwargs.get('context', {}).get('request')
        ex_list = json.loads(request.GET.get("ex_list","[]") if request else "[]")

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif exclude is not None:
            # drop fields that are specified in the 'exclude' argument
            for field_name in set(exclude):
                self.fields.pop(field_name)
        for field_name in set(ex_list):
            self.fields.pop(field_name)


def isAnonymousUser(obj_suer):
    if str(obj_suer) == STR_ANONYMOUS_USER:
        return True
    else:
        return False






