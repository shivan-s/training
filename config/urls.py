"""Root urls."""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path("", include("project.urls")),
    path("profile/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("grappelli/", include("grappelli.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
    path("__debug__", include("debug_toolbar.urls")),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
