from django.urls import include, path
from rest_framework import routers

from api import views as v

app_name = "api"
router = routers.DefaultRouter()
router.register("alunos", v.AlunoViewSet, basename="aluno")
router.register("disciplinas", v.DisciplinaViewSet, basename="disciplina")
router.register("boletins", v.BoletimViewSet, basename="boletim")
router.register("notas_boletins", v.NotasBoletimViewSet, basename="nota_boletim")

urlpatterns = [
    path("", include(router.urls)),
]
