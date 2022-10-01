from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.authtoken import views as rf_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("app.urls", namespace="app")),
    path("api/", include("api.urls", namespace="api")),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", rf_views.obtain_auth_token, name="api_token_auth"),
]

urlpatterns += [
    path("favicon.ico", RedirectView.as_view(url=static("images/favicon.ico"))),
]
