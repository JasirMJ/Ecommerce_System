from django.shortcuts import render
from EcommerceSystem.Imports import *
from .serializer import ItemCategorySerializer
from .serializer import BrandSerializer
from .serializer import ItemSerializer
from .serializer import ItemSerializerWithStock
from .models import TblItemCategory, TblBrand
from .models import TblItems
from Shops.models import ShopDetails
from .logics import add_Stock

# Create your views here.

class ClsCategory(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemCategorySerializer


    def post(self,request):

        try:


            name = request.POST["name"]
            parent = request.POST["parent"]
            shop_id = request.POST["shop_id"]
            obj_shop = ShopDetails.objects.get(id= shop_id)
            obj_parent = None
            parent_id = None
            if parent != "":
                obj_parent = TblItemCategory.objects.get(id= parent)
                parent_id = obj_parent.id
            print("Request Accepted")



            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_shop,request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            if TblItemCategory.objects.filter(shop= obj_shop).filter(name__iexact= name).count() >0:
                return JsonResponse(getValErrorDict("category already exist in this name"))
            if obj_parent != None:
                if obj_parent.parent != None:
                    return JsonResponse(getValErrorDict("cannot create a category under a sub category"))
            print("Request Validated")


            obj_category = TblItemCategory()
            obj_category.name = name
            obj_category.parent = parent_id
            obj_category.shop = obj_shop
            obj_category.save()
            print("category saved")


            return JsonResponse(getSuccessDict("category saved"))


        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))


    def get_queryset(self):

        try:

            id = self.request.GET.get("id", "")
            shop_id = self.request.GET.get("shop_id", "")
            page_wise = self.request.GET.get("page_wise","true")
            name_sorting = self.request.GET.get("name_sorting","")
            search_text = self.request.GET.get("search_text","")
            parent = self.request.GET.get("parent_id","")
            print("Request Accepted")


            if page_wise not in lst_string_bool_values_without_blank:
                return TblItemCategory.objects.none()
            print("Request validated")


            if get_bool_of_string(page_wise) == False:
                self.pagination_class = None

            qs = TblItemCategory.objects.all()

            if shop_id != "":
                qs = qs.filter(shop_id= shop_id)
            if id != "":
                qs = qs.filter(id= id)
            if parent != "":
                if parent == "null":
                    qs = qs.filter(parent= None)
                elif parent == "!null":
                    qs = qs.exclude(parent= None)
                else:
                    qs = qs.filter(parent= parent)
            if name_sorting == "a":
                qs = qs.order_by("name")
            elif name_sorting == "d":
                qs = qs.order_by("-name")

            qs = qs.filter(name__icontains= search_text)


            return qs


        except Exception as e:
            print("excetion occured : " + str(e))
            return TblItemCategory.objects.none()


    def put(self,request):

        try:

            id = request.POST["id"]
            obj_category = TblItemCategory.objects.get(id= id)
            obj_shop = obj_category.shop
            name = request.POST["name"]
            parent = request.POST["parent"]
            obj_parent = None
            parent_id = None
            if parent != "":
                obj_parent = TblItemCategory.objects.get(id=parent)
                parent_id = obj_parent.id
            print("Request Accepted")


            # Accessing the permissios of user on the shop
            dic_permissions = getRoleDetails(obj_shop,request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to edit item category"))
            if TblItemCategory.objects.filter(shop= obj_shop).filter(name__iexact= name).exclude(id= id).count() >0:
                return JsonResponse(getValErrorDict("category already exist in this name"))
            if obj_parent != None:
                if obj_parent.parent != None:
                    return JsonResponse(getValErrorDict("Cannot create a category under a sub category"))
            print("Request Validated")


            obj_category.name= name
            obj_category.parent = parent_id
            obj_category.save()
            print("category updated")


            return JsonResponse(getSuccessDict("category updated"))

        except Exception as e:
            return JsonResponse(getErrorDict("An error occured",str(e)))


    def delete(self,request):

        try:

            id = request.GET["id"]
            obj_category = TblItemCategory.objects.get(id= id)
            print("Request Accepted")

            # Accessing the permissios of the user on the shop
            dic_permissions = getRoleDetails(obj_category.shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to delete item category"))
            print("Request Validated")


            qs_sub_category = TblItemCategory.objects.filter(parent= obj_category.id)
            qs_sub_category.update(parent= None)
            print("Sub Categories parent changed to null")


            obj_category.delete()
            print("Category Deleted")

            return JsonResponse(getSuccessDict("category deleted"))


        except Exception as e:
            return JsonResponse(getErrorDict("An error occured", str(e)))


class ClsBrand(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BrandSerializer

    def post(self,request):
        try:

            shop_id = request.POST["shop_id"]
            obj_shop = ShopDetails.objects.get(id= shop_id)
            name = request.POST["name"]
            print("Request Accepted")


            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            if name == "":
                return JsonResponse(getValErrorDict("invalid name"))
            if TblBrand.objects.filter(shop= obj_shop).filter(name__iexact= name).count() >0:
                return JsonResponse(getValErrorDict("brand already exist in this name"))
            print("Request Validated")


            obj_brand = TblBrand()
            obj_brand.name = name
            obj_brand.shop = obj_shop
            obj_brand.save()

            return JsonResponse(getSuccessDict("brand Saved"))

        except Exception as e:
            return JsonResponse(getErrorDict("An error occured",str(e)))

    def get_queryset(self):


        id = self.request.GET.get("id", "")
        shop_id = self.request.GET.get("shop_id", "")
        page_wise = self.request.GET.get("page_wise","true")
        name_sorting = self.request.GET.get("name_sorting","")
        search_text = self.request.GET.get("search_text","")
        print("Request Accepted")


        if page_wise not in lst_string_bool_values_without_blank:
            return TblBrand.objects.none()
        print("Request validated")


        if get_bool_of_string(page_wise) == False:
            self.pagination_class = None

        qs = TblBrand.objects.all()

        if shop_id != "":
            qs = qs.filter(shop_id= shop_id)
        if id != "":
            qs = qs.filter(id= id)
        if name_sorting == "a":
            qs = qs.order_by("name")
        elif name_sorting == "d":
            qs = qs.order_by("-name")

        qs = qs.filter(name__icontains= search_text)

        return qs

    def put(self,request):

        try:

            id = request.POST["id"]
            obj_brand = TblBrand.objects.get(id= id)
            name = request.POST["name"]
            print("Request Accepted")

            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_brand.shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            if TblBrand.objects.filter(shop= obj_brand.shop).filter(name__iexact= name).exclude(id= id).count() >0:
                return JsonResponse(getValErrorDict("brand already exist in this name"))
            print("Request Validated")

            obj_brand.name= name
            obj_brand.save()

            return JsonResponse(getSuccessDict("brand updated"))


        except Exception as e:
            return JsonResponse(getErrorDict("An error occured",str(e)))

    def delete(self,request):

        try:

            id = request.GET["id"]
            obj_brand = TblBrand.objects.get(id= id)
            print("Request Accepted")

            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_brand.shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            print("Request Validated")


            obj_brand.delete()
            print("brand Deleted")

            return JsonResponse(getSuccessDict("brand deleted"))


        except Exception as e:
            return JsonResponse(getErrorDict("An error occured", str(e)))


class ClsItems(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    def post(self,request):

        try:

            shop_id = request.POST["shop_id"]
            obj_shop = ShopDetails.objects.get(id= shop_id)
            name = request.POST["name"]
            description = request.POST["description"]
            category = request.POST["category"]
            subcategory = request.POST["subcategory"]
            obj_category = None
            obj_sub_category = None
            if category != "":
                obj_category = TblItemCategory.objects.get(id= category)
            if subcategory != "":
                obj_sub_category = TblItemCategory.objects.get(id= subcategory)
            brand = request.POST["brand"]
            obj_brand = None
            if brand != "":
                obj_brand = TblBrand.objects.get(id= brand)
            rate = float(request.POST["rate"])
            print("Request Accepted")



            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_shop, request.user)

            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            if name == "":
                return JsonResponse(getValErrorDict("invalid name"))
            if obj_category != None:
                if obj_category.shop != obj_shop:
                    return JsonResponse(getValErrorDict("this category is not saved for this shop"))
            if obj_sub_category != None:
                if obj_sub_category.shop != obj_shop:
                    return JsonResponse(getValErrorDict("the subcategory is not saved for this shop"))
                if obj_category == None:
                    return JsonResponse(getValErrorDict("cannot add subcategory without category"))
                else:
                    if str(obj_sub_category.parent) != str(obj_category.id):
                        return JsonResponse(getValErrorDict("the category is not identified as the parent of subcategory"))
            if  obj_brand != None:
                if obj_brand.shop != obj_shop:
                    return JsonResponse(getValErrorDict("this brand is not saved for this shop"))
            if TblItems.objects.filter(shop= obj_shop).filter(name__iexact= name).count() > 0:
                return JsonResponse(getValErrorDict("item already exist. please change the name"))
            if rate == 0:
                return JsonResponse(getValErrorDict("rate cannot be zero"))
            print("Request validated")


            obj_serializer = ItemSerializer(data= request.data)

            if obj_serializer.is_valid() == True:
                obj_serializer.save(category= obj_category,
                                    brand= obj_brand,
                                    rate= rate,
                                    subcategory= obj_sub_category,
                                    shop = obj_shop)
                return JsonResponse(getSuccessDict("item saved"))

            else:
                return JsonResponse(getValErrorDict(obj_serializer.errors))

        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))

    def get_queryset(self):

        try:

            id = self.request.GET.get("id","")
            shop_id = self.request.GET.get("shop_id","")
            stock = self.request.GET.get("need_stock","false")
            print("Request Accepted")


            if get_bool_of_string(stock) == True:
                self.serializer_class = ItemSerializerWithStock
            qs = TblItems.objects.all()
            if shop_id != "":
                qs = qs.filter(shop_id= shop_id)
            if id != "":
                qs = qs.filter(id= id)


            return qs


        except Exception as e:
            return TblItems.objects.none()

    def put(self,request):

        try:

            id = request.POST["id"]
            obj_item = TblItems.objects.get(id= id)
            obj_shop = obj_item.shop
            name = request.POST["name"]
            description = request.POST["description"]
            category = request.POST["category"]
            subcategory = request.POST["subcategory"]
            obj_category = None
            obj_sub_category = None
            if category != "":
                obj_category = TblItemCategory.objects.get(id= category)
            if subcategory != "":
                obj_sub_category = TblItemCategory.objects.get(id= subcategory)
            brand = request.POST["brand"]
            obj_brand = None
            if brand != "":
                obj_brand = TblBrand.objects.get(id= brand)
            rate = float(request.POST["rate"])
            print("Request Accepted")


            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            if name == "":
                return JsonResponse(getValErrorDict("invalid name"))
            if obj_category != None:
                if obj_category.shop != obj_shop:
                    return JsonResponse(getValErrorDict("this category is not saved for this shop"))
            if obj_sub_category != None:
                if obj_sub_category.shop != obj_shop:
                    return JsonResponse(getValErrorDict("the subcategory is not saved for this shop"))
                if obj_category == None:
                    return JsonResponse(getValErrorDict("cannot add subcategory without category"))
                else:
                    if str(obj_sub_category.parent) != str(obj_category.id):
                        return JsonResponse(
                            getValErrorDict("the category is not identified as the parent of subcategory"))
            if obj_brand != None:
                if obj_brand.shop != obj_shop:
                    return JsonResponse(getValErrorDict("this brand is not saved for this shop"))
            if TblItems.objects.filter(shop=obj_shop).filter(name__iexact=name).exclude(id= id).count() > 0:
                return JsonResponse(getValErrorDict("item already exist. please change the name"))
            if rate == 0:
                return JsonResponse(getValErrorDict("rate cannot be zero"))
            print("Request validated")


            obj_serializer = ItemSerializer(obj_item,data= request.data,)

            if obj_serializer.is_valid() == True:
                obj_serializer.save(category=obj_category,
                                    brand=obj_brand,
                                    rate=rate,
                                    subcategory=obj_sub_category,
                                    shop=obj_shop)
                return JsonResponse(getSuccessDict("item updated"))
            else:
                return JsonResponse(getValErrorDict(obj_serializer.errors))

        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))

    def delete(self,request):

        try:


            id = request.GET["id"]
            obj_item = TblItems.objects.get(id= id)
            print("Request Accepted")

            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_item.shop, request.user)
            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage items"))
            print("Request Validated")

            obj_item.delete()

            return JsonResponse(getSuccessDict("item deleted"))


        except Exception as e:
            return JsonResponse(getErrorDict("an error occured",str(e)))


class ClsInventory(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:

            lst_keywords = ["add_stock","less_stock"]

            keyword = request.POST["keyword"]


            lst_items = json.loads(request.POST["items"])
            shop_id = request.POST["shop_id"]
            obj_shop = ShopDetails.objects.get(id= shop_id)
            print("Request Accepted")

            if keyword not in lst_keywords:
                return JsonResponse(getValErrorDict("invalid keyword"))

            # Accessing the permissions of the user on the shop
            dic_permissions = getRoleDetails(obj_shop, request.user)

            if dic_permissions[STOCK_MANAGEMENT] == False:
                return JsonResponse(getValErrorDict("you don't have the permission to manage stock"))
            if len(lst_items) == 0:
                return JsonResponse(getValErrorDict("list of items cannot be empty"))
            print("Request validated")


            lst_rejected = []

            for dic in lst_items:

                if "item" not in dic:
                    dic.update({"error" : "item is not provided"})
                    lst_rejected.append(dic)
                    continue
                if "qty" not in dic:
                    dic.update({"error": "qty is not provided"})
                    lst_rejected.append(dic)
                    continue


                item = dic["item"]
                obj_item = TblItems.objects.filter(id= item)
                if obj_item.count() == 0:
                    dic["error"] = "item_id is invalid"
                    lst_rejected.append(dic)
                    continue
                else:
                    obj_item = obj_item.first()


                qty = getFloatOfObject(dic["qty"])
                if qty == 0:
                    dic["error"] = "invalid qty"
                    lst_rejected.append(dic)
                    continue

                print(lst_rejected)

                if keyword == "add_stock":
                    add_Stock(datetime.now(),obj_shop, obj_item, "PS", "0", qty, 0)
                elif keyword == "less_stock":
                    add_Stock(datetime.now(),obj_shop, obj_item, "PS", "0", 0, qty)
                else:
                    pass

            if len(lst_rejected) == 0:
                return JsonResponse(getSuccessDict("success"))
            else:
                return JsonResponse(getSuccessDict("the following items stock doesn't changed",{"rejections" : lst_rejected}))


        except Exception as e:

            return JsonResponse(getErrorDict("an error occured",str(e)))