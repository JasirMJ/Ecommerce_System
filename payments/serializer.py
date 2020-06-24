from EcommerceSystem.Imports import *
from .models import TblPayments
from users.serializers import UserSerializerSimple

class TblPaymentSerializer(DynamicFieldsModelSerializer):

    user = UserSerializerSimple(many= False,read_only= True)

    class Meta:

        model = TblPayments
        fields = [
                    "date",
                    "transaction_id",
                    "transaction_date",
                    "amount",
                    "status",
                    "user",
                 ]