from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views as rf_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls", namespace="v1")),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", rf_views.obtain_auth_token),
]
