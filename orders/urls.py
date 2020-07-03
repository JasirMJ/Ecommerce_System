from django.urls import include,path
from orders import views

urlpatterns = [

    path("status",views.ClsStatus.as_view(),name= "status"),

]
