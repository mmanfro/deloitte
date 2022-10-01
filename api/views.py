from app.models import *
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

import api.v1.serializers as v1
import api.v1.serializers as last
from api.utils import get_version


class AlunoViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento de Alunos.

    ---
    ## Filtros:
    - **email**: email do aluno  ` ?email=<email> `
    """

    serializer_class = v1.AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if get_version(self.request.version) == "v1":
            return v1.AlunoSerializer
        return last.AlunoSerializer

    def get_queryset(self):
        queryset = self.queryset
        if "email" in self.request.GET:
            queryset = queryset.filter(email=self.request.GET["email"])
        return queryset


class DisciplinaViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento de Disciplinas.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Disciplina.objects.all()
    lookup_field = "nome"

    def get_serializer_class(self):
        if self.request.version == "v1":
            return v1.DisciplinaSerializer
        return last.DisciplinaSerializer


class BoletimViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento de Boletins.

    ---
    ## Filtros:
    - **aluno**: id do aluno  ` ?aluno=<id> `
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Boletim.objects.all()

    def get_serializer_class(self):
        if self.request.version == "v1":
            return v1.BoletimSerializer
        return last.BoletimSerializer

    def get_queryset(self):
        queryset = self.queryset
        if "aluno" in self.request.GET:
            queryset = queryset.filter(aluno=self.request.GET["aluno"])
        return queryset


class NotasBoletimViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento das notas dos boletins.

    As notas com vírgula ou maiores que 10 são convertidas. Exemplo:

    - 7,5 → 7.5
    - 75 → 7.5

    ---
    ## Filtros:
    ` ?aluno=<id>&disciplina=<id>&boletim=<id>&nota=<valor_inicial>e<valor_final> `

    - **aluno**: id do aluno  ` ?aluno=<id> `
    - **disciplina**: id da disciplina  ` ?disciplina=<id> `
    - **boletim**: id do boletim  ` ?boletim=<id> `
    - **nota**: distância de valores, separados pela letra _e_  ` ?nota=<valor_inicial>e<valor_final> `
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = NotasBoletim.objects.all()

    def get_serializer_class(self):
        if self.request.version == "v1":
            return v1.NotasBoletimSerializer
        return last.NotasBoletimSerializer

    def get_queryset(self):
        queryset = self.queryset
        if "aluno" in self.request.GET:
            queryset = queryset.filter(boletim__aluno=self.request.GET["aluno"])
        if "disciplina" in self.request.GET:
            queryset = queryset.filter(disciplina=self.request.GET["disciplina"])
        if "boletim" in self.request.GET:
            queryset = queryset.filter(boletim=self.request.GET["boletim"])
        if "nota" in self.request.GET:
            valor_inicial, valor_final = self.request.GET["nota"].split("e")
            queryset = queryset.filter(nota__gte=valor_inicial, nota__lte=valor_final)
        return queryset
