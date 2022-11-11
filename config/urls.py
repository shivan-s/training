from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
    path("admin/", admin.site.urls),
    path("__debug__", include("debug_toolbar.urls")),
    path("", include("project.urls")),
    path("profile/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
