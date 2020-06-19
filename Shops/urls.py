from django.urls import path, include

from Shops import views

urlpatterns = [

    path('', views.ShopsView.as_view(), name= "details"),

]


