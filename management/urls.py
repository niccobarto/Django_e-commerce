from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_vision, name='manager_home'),
    path('list_product',views.ManagerProductView.as_view(), name='manage_products'),
    path('product/<int:product_id>/',views.manage_product, name='product_edit'),
    path('list_categories/',views.m_categories_list, name='manage_categories'),
]