from django.urls import include, path
from rest_framework import routers

from api import views as v

app_name = "api"
router = routers.DefaultRouter()
router.register("aluno", v.AlunoViewSet)
router.register("disciplina", v.DisciplinaViewSet)
router.register("boletim", v.BoletimViewSet)
router.register("notas_boletim", v.NotasBoletimViewSet, basename="notas_boletim")

urlpatterns = [
    path("", include(router.urls)),
]
