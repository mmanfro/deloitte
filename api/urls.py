from django.urls import include, path
from rest_framework import routers

from api import views as v

app_name = "api"
router = routers.DefaultRouter()
router.register("aluno", v.AlunoViewSet, basename="aluno")
router.register("disciplina", v.DisciplinaViewSet, basename="disciplina")
router.register("boletim", v.BoletimViewSet, basename="boletim")
router.register("notas_boletim", v.NotasBoletimViewSet, basename="notas_boletim")

urlpatterns = [
    path("", include(router.urls)),
]
