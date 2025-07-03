from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/', views.register_user,name="register"),
    path('view/', views.view_account,name="view_account"),
    path('edit/', views.edit_account,name="edit_account"),
    path('password/', views.change_password,name="change_password"),
    path('address/', views.manage_addresses,name="manage_addresses"),
    path('address/<int:address_id>/edit', views.edit_address,name="edit_address"),

]