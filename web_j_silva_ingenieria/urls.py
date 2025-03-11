# proyecto/urls.py (archivo principal)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contacto.urls')),  # Incluyendo todas las rutas de contacto
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   