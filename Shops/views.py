from django.shortcuts import render
from EcommerceSystem.Imports import *
from .models import *
from .serializer import ShopSerializer
# Create your views here.


class ShopsView(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer

    def post(self,request):

        is_shop_saved = False
        is_address_saved = False

        try:

            shop_name = request.POST["shop_name"]
            super_manager = self.request.user
            is_approved = False
            is_active = True
            place = request.POST["place"]
            city = request.POST["city"]
            pin = request.POST["pin"]
            district = request.POST["district"]
            state = request.POST["state"]
            latitude = request.POST["latitude"]
            longitude = request.POST["longitude"]
            print("Request Accepted")


            if shop_name == "":
                return JsonResponse(getValErrorDict("invalid shop_name"))
            if place == "":
                return JsonResponse(getValErrorDict("invalid place"))
            if city == "":
                return JsonResponse(getValErrorDict("invalid city"))
            if pin == "":
                return JsonResponse(getValErrorDict("invalid pin"))
            if district == "":
                return JsonResponse(getValErrorDict("invalid district"))
            if state == "":
                return JsonResponse(getValErrorDict("invalid state"))
            print("request validated")


            obj_shop = ShopDetails()
            obj_shop.shop_name = shop_name
            obj_shop.super_manager = super_manager
            obj_shop.is_active = is_active
            obj_shop.is_approved = is_approved
            obj_shop.save()
            is_shop_saved = True
            print("shop saved")


            obj_address = ShopAddress()
            obj_address.shop = obj_shop
            obj_address.place = place
            obj_address.city = city
            obj_address.pin = pin
            obj_address.district = district
            obj_address.state = state
            obj_address.latitude = latitude
            obj_address.longitude = longitude
            obj_address.save()
            is_address_saved = True
            print("address saved")


            return JsonResponse(getSuccessDict("shop details saved"))


        except Exception as e:
            if is_address_saved == True:
                obj_address.delete()
            if is_shop_saved == True:
                obj_shop.delete()
            return JsonResponse(getErrorDict("an error occured",str(e)))

    def get_queryset(self):

        try:

            qs = ShopDetails.objects.all()


            keyword = self.request.GET.get("keyword", "")
            is_active = self.request.GET.get("is_active","")
            is_approved = self.request.GET.get("is_approved","")
            print("request accepted")


            if is_active not in lst_string_bool_values_with_blank:
                return ShopDetails.objects.none()
            if is_approved not in lst_string_bool_values_with_blank:
                return ShopDetails.objects.none()
            print("request validated")


            is_active = get_bool_of_string(is_active)
            is_approved = get_bool_of_string(is_approved)


            if keyword == "my_shops":
                qs = qs.filter(super_manager= self.request.user)
            if is_active != "":
                qs = qs.filter(is_active = is_active)
            if is_approved != "":
                qs = qs.filter(is_approved= is_approved)


            return qs

        except Exception as e:
            print("Exception occured : " + str(e))
            return ShopDetails.objects.none()

    def patch(self,request):

        try:


            keyword = request.POST["keyword"]

            if keyword == "change_activation":

                shop_id = request.POST["shop_id"]
                obj_shop = ShopDetails.objects.get(id= shop_id)
                is_active = request.POST["is_active"]
                is_active = request.POST["is_active"]
                print("Request Accepted")


                if obj_shop.super_manager != request.user:
                    return JsonResponse(getValErrorDict("you are not identified as the manager of this shop"))
                if is_active not in lst_string_bool_values_without_blank:
                    return JsonResponse(getValErrorDict("invalid value for is_active"))
                print("request validated")


                obj_shop.is_active = get_bool_of_string(is_active)
                obj_shop.save()

                return JsonResponse(getSuccessDict("activation changed"))


            if keyword == "change_approval":

                shop_id = request.POST["shop_id"]
                obj_shop = ShopDetails.objects.get(id=shop_id)
                is_approved = request.POST["is_approved"]
                print("Request Accepted")

                if self.request.user.is_superuser != 1:
                    return JsonResponse(getValErrorDict("you are not identified as the admin"))
                if is_approved not in lst_string_bool_values_without_blank:
                    return JsonResponse(getValErrorDict("invalid value for is_approved"))
                print("request validated")

                obj_shop.is_approved = get_bool_of_string(is_approved)
                obj_shop.save()

                return JsonResponse(getSuccessDict("approval changed"))


            else:
                return JsonResponse(getValErrorDict("invalid keyword"))

        except Exception as e:
            print("Exception occured")
            return JsonResponse(getErrorDict("an error occured",str(e)))

    def put(self,request):

        is_shop_saved = False
        is_address_saved = False

        try:


            id = request.POST["id"]
            obj_shop = ShopDetails.objects.get(id= id)
            obj_address = ShopAddress.objects.filter(shop= obj_shop)
            if obj_address.count() > 0:
                obj_address = obj_address.first()
            else:
                obj_address = ShopAddress()
            obj_temp_shop = obj_shop
            obj_temp_address = obj_address
            shop_name = request.POST["shop_name"]
            place = request.POST["place"]
            city = request.POST["city"]
            pin = request.POST["pin"]
            district = request.POST["district"]
            state = request.POST["state"]
            latitude = request.POST["latitude"]
            longitude = request.POST["longitude"]
            print("Request Accepted")


            if obj_shop.super_manager != request.user:
                return JsonResponse(getValErrorDict("you are not identified as the admin of the shop"))
            if shop_name == "":
                return JsonResponse(getValErrorDict("invalid shop_name"))
            if place == "":
                return JsonResponse(getValErrorDict("invalid place"))
            if city == "":
                return JsonResponse(getValErrorDict("invalid city"))
            if pin == "":
                return JsonResponse(getValErrorDict("invalid pin"))
            if district == "":
                return JsonResponse(getValErrorDict("invalid district"))
            if state == "":
                return JsonResponse(getValErrorDict("invalid state"))
            print("request validated")


            obj_shop.shop_name = shop_name
            obj_shop.save()
            is_shop_saved = True
            print("shop updated")


            obj_address.shop = obj_shop
            obj_address.place = place
            obj_address.city = city
            obj_address.pin = pin
            obj_address.district = district
            obj_address.state = state
            obj_address.latitude = latitude
            obj_address.longitude = longitude
            obj_address.save()
            is_address_saved = True
            print("address updated")

            return JsonResponse(getSuccessDict("shop details updated"))


        except Exception as e:
            if is_address_saved == True:
                obj_temp_address.save()
            if is_shop_saved == True:
                obj_temp_shop.save()
            return JsonResponse(getErrorDict("an error occured", str(e)))