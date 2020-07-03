from django.shortcuts import render
from EcommerceSystem.Imports import *
from .models import TblStatus
from .serializer import StatusSerializer

# Create your views here.

class ClsStatus(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StatusSerializer


    def get_queryset(self):

        self.pagination_class = None
        qs = TblStatus.objects.all()
        return qs




