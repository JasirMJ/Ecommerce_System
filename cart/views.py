from django.shortcuts import render
from EcommerceSystem.Imports import *
from .models import TblCart
from items.models import TblItems
from .serializer import CartSerializer
# Create your views here.

class ClsCart(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def post(self,request):

        try:

            obj_user = self.request.user
            date = datetime.now()
            lst_items = json.loads(request.POST["items"])
            qs_items = TblItems.objects.filter(id__in= lst_items)
            print("Request Accepted")



            if qs_items.count() == 0:
                return JsonResponse(getValErrorDict("valid items not detected"))
            print("request validated")



            for obj_item in qs_items:
                obj_cart = TblCart()
                obj_cart.user = obj_user
                obj_cart.date = date
                obj_cart.item = obj_item
                obj_cart.save()
            print("items added to cart")


            return JsonResponse(getSuccessDict("items added to cart"))

        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))


    def get_queryset(self):

        try:

            qs = TblCart.objects.filter(user= self.request.user)
            qs = qs.order_by("-id")

            return qs

        except Exception as e:
            print("exception occured : " + str(e))
            return TblCart.objects.none()


    def delete(self,request):

        try:

            lst_id = json.loads(request.GET["id_list"])

            qs = TblCart.ojects.filter(id__in= lst_id)
            qs = qs.filter(user = self.request.user)
            count = qs.count()

            qs.delete()

            return JsonResponse(getSuccessDict(str(count) + " items removed"))

        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))