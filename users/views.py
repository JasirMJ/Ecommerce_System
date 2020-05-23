
from EcommerceSystem.global_variables import *
from EcommerceSystem.Imports import *
from users.serializers import *

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
    # def get_queryset(self):
    #     id = self.request.GET.get('id','')
    #
    #     if id :
    #         queryset = User.objects.filter(id=id)
    #     else:
    #         queryset = User.objects.all()
    #     return queryset

    def post(self,request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(password=make_password(self.request.data['password']))
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
            obj = serializer.save(user_id=self.request.POST['id'])
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

        if keyword =="add_role":
            if self.request.user.is_superuser:
                role_id = self.request.POST.get("role_id","")
                if not role_id or role_id == "":
                    return Response({
                        STATUS: False,
                        MESSAGE: "Required role_id"
                    })
                UserDetails.objects.get(user=id).role.add(UserRoles.objects.get(id=role_id))
                return Response({
                    STATUS:True,
                    MESSAGE:"New role added"
                })
            else:
                return Response({
                    STATUS: False,
                    MESSAGE: "Only admin can change it"
                })
        elif keyword =="remove_role":
            if self.request.user.is_superuser:

                role_id = self.request.POST.get("role_id", "")
                if not role_id or role_id == "":
                    return Response({
                        STATUS: False,
                        MESSAGE: "Required role_id"
                    })
                UserDetails.objects.get(user=id).role.remove(UserRoles.objects.get(id=role_id))
                return Response({
                    STATUS: True,
                    MESSAGE: "Role removed"
                })
            else:
                return Response({
                    STATUS: False,
                    MESSAGE: "Only admin can change it"
                })
        elif keyword =="add_page":
            UserDetails.objects.get(created_by=self.request.user.id)
            if self.request.user.is_superuser:
                page_id = self.request.POST.get("page_id", "")
                if not page_id or page_id == "":
                    return Response({
                        STATUS: False,
                        MESSAGE: "Required page_id"
                    })
                UserDetails.objects.get(user=id).pages.add(Pages.objects.get(id=page_id))
                return Response({
                    STATUS: True,
                    MESSAGE: "Page added"
                })
            else:
                return Response({
                    STATUS: False,
                    MESSAGE: "Only admin can change it"
                })
        elif keyword =="remove_page":
            if self.request.user.is_superuser:
                page_id = self.request.POST.get("page_id", "")
                if not page_id or page_id == "":
                    return Response({
                        STATUS: False,
                        MESSAGE: "Required page_id"
                    })
                UserDetails.objects.get(user=id).pages.remove(Pages.objects.get(id=page_id))
                return Response({
                    STATUS: True,
                    MESSAGE: "Page removed"
                })
            else:
                return Response({
                    STATUS: False,
                    MESSAGE: "Only admin can change it"
                })
        elif keyword =="generate_string":
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
        elif keyword=="add_assistant":

            serializer = UserDetailsSerializers(UserDetails.objects.filter(user=id).first(), data=self.request.data,
                                                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(referance=None,created_by=User.objects.get(id=self.request.user.id))

            return Response(
                {
                    STATUS: True,
                    MESSAGE: "assistant added",
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
    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         queryset = Address.objects.all()
    #     else:
    #         obj = UserDetails.objects.none()
    #     return queryset

    def post(self,request):
        id = ""

        user = self.request.POST.get("user")
        # print(UserDetails.objects.get(user=user))
        if not user or user == "":
            return Response({
                STATUS: False,
                MESSAGE: "Required user"
            })

        try:
            if not User.objects.filter(id=user).exists():
                return Response({
                    STATUS:False,
                    MESSAGE:"Unauthorised access"
                })

            serializer = AddressSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)

            obj = serializer.save()
            print("Data id or object : ",obj.id)
            id = obj.id

            UserDetails.objects.get(user=user).address.add(obj)

            # address.add(obj)

            return Response(
                {
                    STATUS: True,
                    MESSAGE:"Data created "+str(obj.id)
                }
            )
        except Exception as e:
            if id:
                Address.objects.get(id=id).delete()

            printLineNo()
            print("type :",type(e))

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

class PagesView(ListAPIView):
    serializer_class = PagesSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Pages.objects.all()
        return queryset

    def post(self,request):
        try:
            serializer = PagesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.is_valid(raise_exception=True)
            obj = serializer.save()
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
                    MESSAGE: e.detail,
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
        serializer = PagesSerializers(UserDetails.objects.filter(id=id).first(), data=request.data,partial=True)
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
                Pages.objects.all().delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all data",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                Pages.objects.filter(id__in=id).delete()
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

            serializer = UserRolesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.is_valid(raise_exception=True)
            obj = serializer.save()
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

        serializer = UserRolesSerializers(UserRoles.objects.filter(id=id).first(), data=request.data,partial=True)
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
