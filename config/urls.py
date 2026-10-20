from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from gallery.views import artwork_media

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "media/artworks/<path:path>",
        artwork_media,
        name="artwork_media",
    ),
    path("", include("gallery.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
