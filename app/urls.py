from django.urls import include, path

from app import views as v

app_name = "app"
urlpatterns = [
    path("", v.index),
    path(
        "generate-data-via-REST",
        v.generate_data_via_REST,
        name="generate_data_via_REST",
    ),
]
