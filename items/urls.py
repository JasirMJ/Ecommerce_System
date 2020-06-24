from django.urls import path, include

from items import views

urlpatterns = [

    path('category/', views.ClsCategory.as_view(), name= "category"),
    path('brand/', views.ClsBrand.as_view(), name= "brand"),
    path('details/', views.ClsItems.as_view(), name= "details"),
    path('stock/', views.ClsInventory.as_view(), name= "stock"),

]


