from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
