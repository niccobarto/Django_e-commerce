from django.urls import path
from .views import HomeView, product_detail

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
