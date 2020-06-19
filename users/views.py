from EcommerceSystem.Imports import *
from users.serializers import *
from Shops.models import ShopDetails


def index(request):
    return HttpResponse('Welcome to Ecommerce , site is under developement')

class UsersView(ListAPIView):

    serializer_class = UserSerializers
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response({
            STATUS:True,
            MESSAGE:"GET method not allowed"
        })

    def post(self,request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(password=make_password(self.request.data['password']),is_active= True)
        print("user id or object : ",obj.id)

        return Response(
            {
                STATUS: True,
                MESSAGE:"User created "+str(obj.id)
            }
        )

    def put(self,request):
        print(self.request.user.id)
        #
        if self.request.user.is_superuser:
            print("superuser")
            id = self.request.POST.get("id",'')
            if not id or id =="":
                return Response({
                    STATUS:False,
                    MESSAGE:"Required id"
                })
            # return Response({True})
        else:
            print("normaluser")
            if not self.request.user.id:
                return Response({
                    STATUS:False,
                    MESSAGE:"Unauthorised"
                })
            # else:
            #     return Response({True})


        serializer = UserSerializers(User.objects.filter(id=id).first(), data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        if self.request.POST.get('password'):
            serializer.save(password=make_password(self.request.data['password']))
        else:
            serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )

    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                User.objects.all().exclude(is_staff=True).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all users",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                User.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "users deleted having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )


class UserDetailsView(ListAPIView):
    serializer_class = UserDetailsSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        id = self.request.GET.get('id','-1')
        keyword = self.request.GET.get('keyword','')

        print("Super User ? : ",self.request.user.is_superuser)
        print("id ",id)
        if keyword =="referance":
            queryset = UserDetails.objects.filter(referance=id)
            return queryset

        if self.request.user.is_superuser:
            print("Admin ")

            if keyword=="my":
                #fetch admin profile
                queryset = UserDetails.objects.filter(user__username=self.request.user)
            elif keyword == "userid":
                #fetch user profile with id
                queryset = UserDetails.objects.filter(user__id=id)
            else:
                #fetch all profile
                print("Admin viewed all user ")
                queryset = UserDetails.objects.all()
            return queryset
        elif str(self.request.user) == "AnonymousUser":
            #hangle unknown user
            print("Unknown User")
            return UserDetails.objects.none()
        else:
            #fetch user profile
            print("User ",self.request.user)
            return UserDetails.objects.filter(user=self.request.user)

    def post(self,request):
        try:

            serializer = UserDetailsSerializers(data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            # serializer.is_valid(raise_exception=True)
            obj = serializer.save(user=self.request.user)
            print("Data id or object : ",obj.id)

            return Response(
                {
                    STATUS: True,
                    MESSAGE:"Data created "+str(obj.id)
                }
            )
        except Exception as e:
            printLineNo()
            return JsonResponse(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

    def put(self,request):
        id = self.request.POST.get("id")
        keyword = self.request.POST.get("keyword","")
        # print(self.request.user.id)
        # return Response({True})

        if not id or id =="":
            return Response({
                STATUS:False,
                MESSAGE:"Required object id as id"
            })


        if keyword =="generate_string":
            value = get_random_alphaNumeric_string()
            serializer = UserDetailsSerializers(UserDetails.objects.filter(user=id).first(),data=self.request.data ,
                                                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(referance=value)

            return Response(
                {
                    STATUS: True,
                    MESSAGE: "Data updated",
                    # "Data": request.data
                }
            )
        else:
            serializer = UserDetailsSerializers(UserDetails.objects.filter(user=id).first(), data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    STATUS: True,
                    MESSAGE: "Data updated",
                    # "Data": request.data
                }
            )

    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                UserDetails.objects.all().delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all data",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                UserDetails.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted data having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )


class AddressView(ListAPIView):
    serializer_class = AddressSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            STATUS:True,
            MESSAGE:"GET not allowed"
        })


    def post(self,request):

        try:

            serializer = AddressSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)

            obj = serializer.save(user= request.user)
            print("Data id or object : ",obj.id)
            id = obj.id

            return Response(
                {
                    STATUS: True,
                    MESSAGE:"Data created "+str(obj.id)
                }
            )
        except Exception as e:

            printLineNo()

            return JsonResponse(
                {
                    STATUS: False,
                    # MESSAGE: e.get_full_details(),
                    MESSAGE: e.detail, # serializer error will be formated
                    # MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

    def put(self,request):
        id = self.request.POST.get("id")
        if not id or id =="":
            return Response({
                STATUS:False,
                MESSAGE:"Required object id as id"
            })

        serializer = AddressSerializers(Address.objects.filter(id=id).first(), data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )

    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                Address.objects.all().delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all data",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                Address.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted data having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )


class UsersRoleView(ListAPIView):
    serializer_class = UserRolesSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = UserRoles.objects.all()
        return queryset

    def post(self,request):
        try:

            shop_id = request.POST["shop_id"]
            obj_shop = ShopDetails.objects.get(id= shop_id)

            if request.user != obj_shop.super_manager:
                return JsonResponse(getValErrorDict("you are not the owner of this shop",))

            user_id = request.POST["user_id"]
            obj_user = User.objects.filter(id= user_id)

            serializer = UserRolesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save(user= obj_user,shop= obj_shop)
            print("user id or object : ",obj.id)

            return Response(
                {
                    STATUS: True,
                    MESSAGE:"Role created "+str(obj.id)
                }
            )
        except Exception as e:
            printLineNo()
            return JsonResponse(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

    def put(self,request):
        id = self.request.POST.get("id")
        if not id or id =="":
            return Response({
                STATUS:False,
                MESSAGE:"Required product id as id"
            })

        shop_id = request.POST["shop_id"]
        obj_shop = ShopDetails.objects.get(id=shop_id)

        if request.user != obj_shop.super_manager:
            return JsonResponse(getValErrorDict("you are not the owner of this shop", ))

        user_id = request.POST["user_id"]
        obj_user = User.objects.filter(id=user_id)



        serializer = UserRolesSerializers(UserRoles.objects.filter(id=id).first(), data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(shop = obj_shop,user= obj_user)

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )

    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                UserRoles.objects.all().delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all data",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                UserRoles.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "users deleted having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': "Token "+token.key,
            'user_id': user.pk,
            'username': user.username
        })



# class AdvancedUserView(ListAPIView):
#     serializer_class = AdvancedUserSerializers
#
#     def get_queryset(self):
#         queryset = UserDetails.objects.all()
#         return queryset
#
#     def post(self, request):
#
#         user_serializer = UserSerializers(data=request.data)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save(password=make_password(self.request.data['password']))
#
#         advanced_user_serializer = AdvancedUserSerializers(data=request.data)
#         advanced_user_serializer.is_valid(raise_exception=True)
#         advanced_user_serializer.save()
#
#         return Response(
#             {
#                 STATUS: True,
#                 MESSAGE: "User created"
#             }
#         )
#
#     def put(self, request):
#         id = self.request.POST.get("id")
#         if not id or id == "":
#             return Response({
#                 STATUS: False,
#                 MESSAGE: "Required product id as id"
#             })
#
#         serializer = AdvancedUserSerializers(User.objects.filter(id=id).first(), data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#
#         if self.request.POST.get('password'):
#             serializer.save(password=make_password(self.request.data['password']))
#         else:
#             serializer.save()
#
#         return Response(
#             {
#                 STATUS: True,
#                 MESSAGE: "Data updated",
#                 # "Data": request.data
#             }
#         )
#
#     def delete(self, request):
#         try:
#             id = self.request.POST.get('id', "")
#             if id == "" or not id:
#                 User.objects.all().exclude(is_staff=True).delete()
#                 return Response(
#                     {
#                         STATUS: True,
#                         MESSAGE: "Deleted all users",
#                     }
#                 )
#             else:
#                 id = json.loads(id)
#                 print(id)
#                 User.objects.filter(id__in=id).delete()
#                 return Response(
#                     {
#                         STATUS: True,
#                         MESSAGE: "users deleted having id " + str(id),
#                     }
#                 )
#         except Exception as e:
#             printLineNo()
#             return Response(
#                 {
#                     STATUS: False,
#                     MESSAGE: str(e),
#                     "line_no": printLineNo()
#                 }
#             )
