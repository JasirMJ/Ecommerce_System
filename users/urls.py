from django.urls import path, include

from users import views

urlpatterns = [
    # path('', views.index, name="index"),

    # path('', views.AdvancedUserView.as_view(), name="users"),
    path('', views.UsersView.as_view(), name="users"),#for username ,password ,email
    path('details/', views.UserDetailsView.as_view(), name="details"),#for mobile number
    path('address/', views.AddressView.as_view(), name="address"),
    path('pages/', views.PagesView.as_view(), name="pages"),
    path('roles/', views.UsersRoleView.as_view(), name="role"),
    path('login/', views.LoginView.as_view(), name="role"),
]


