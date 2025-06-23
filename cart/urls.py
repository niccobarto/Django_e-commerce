from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_cart,name='view_cart'),
    path('add/<int:product_id>',views.add_cart,name='add_cart'),
    path('remove_all/<int:product_id>',views.remove_all_cart,name='remove_all_cart'),
    path('decrease_quantity/<int:product_id>',views.decrease_quantity,name='decrease_quantity'),
    path('address/', views.shipment_address,name="shipment_address"),
    path('checkout/', views.view_checkout,name="view_checkout"),
    path('confirm_order/', views.confirm_order,name="confirm_order"),
]