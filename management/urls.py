from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_vision, name='manager_home'),
    path('list_product',views.ManagerProductView.as_view(), name='manage_products'),
    path('product/',views.manage_product, name='manage_product'),
]