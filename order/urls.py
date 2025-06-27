from django.urls import path
from . import views

urlpatterns = [
    path('shipment_address/', views.shipment_address,name="shipment_address"),
    path('checkout/', views.view_checkout,name="view_checkout"),
    path('confirm_order/', views.confirm_order,name="confirm_order"),
    path('history/',views.orders_history,name="orders_history"),
]