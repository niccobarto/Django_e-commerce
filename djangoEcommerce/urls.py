from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('store.urls')),
    path("accounts/", include('accounts.urls')),
    path('cart/',include('cart.urls')),
    path('order/', include('order.urls')),
    path('management/', include('management.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve file media durante lo sviluppo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)