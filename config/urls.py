"""Root urls."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("project.urls")),
    path("profile/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("grappelli/", include("grappelli.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
    path("__debug__", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
