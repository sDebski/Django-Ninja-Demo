from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from backend.api import api

urlpatterns = [
    path("api/", api.urls),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
