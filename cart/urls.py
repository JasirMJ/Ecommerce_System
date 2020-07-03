from django.urls import path,include
from cart import views

urlpatterns = [

    path("",views.ClsCart.as_view(),name= "details"),

]