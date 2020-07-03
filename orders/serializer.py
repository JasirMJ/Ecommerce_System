from EcommerceSystem.Imports import *
from .models import TblStatus

class StatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = TblStatus
        fields = ["id","name",]