from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.serializers import *
from app.models import *


class AlunoViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento de Alunos.

    ---
    ## Filtros:
    - **email**: email do aluno  ` ?email=<email> `
    """

    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Aluno.objects.all()

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
    serializer_class = DisciplinaSerializer
    lookup_field = "nome"


class BoletimViewSet(viewsets.ModelViewSet):
    """
    Ponto de API para gerenciamento de Boletins.

    ---
    ## Filtros:
    - **aluno**: id do aluno  ` ?aluno=<id> `
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Boletim.objects.all()
    serializer_class = BoletimSerializer

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
    serializer_class = NotasBoletimSerializer

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
