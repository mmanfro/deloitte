from django.contrib.auth.models import User
from django.urls import include, path, reverse
from django.utils.timezone import datetime
import pytz
from app.models import *
from api.serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.utils.translation import gettext_lazy as _


def dummyAluno():
    return Aluno.objects.get_or_create(
        nome="Aluno Teste",
        email="teste@teste.com",
        data_nascimento=datetime(1994, 10, 4).date(),
    )[0]


def dummyDisciplina():
    return Disciplina.objects.get_or_create(
        nome="Disciplina Teste",
        carga_horaria=40,
    )[0]


def dummyBoletim():
    return Boletim.objects.get_or_create(
        aluno=dummyAluno(),
        data_entrega=datetime(2022, 10, 4, tzinfo=pytz.timezone("America/Sao_Paulo")),
    )[0]


class AlunoTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("v1:aluno-list")
        self.user = User.objects.create(username="test")
        self.user.set_password("test")
        self.user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=self.user)[0].key}"
        )

    def test_create_aluno_without_auth(self):

        """
        Nenhum aluno deve ser criado sem autenticação.
        """
        self.client.credentials(HTTP_AUTHORIZATION="")

        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Aluno.objects.count(), 0)

    def test_create_aluno(self):
        """
        Aluno deve ser criado.
        """

        data = {
            "nome": "Aluno Teste",
            "email": "teste@teste.com",
            "data_nascimento": "1994-10-04",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aluno.objects.count(), 1)

    def test_create_aluno_data_nascimento_futura(self):
        """
        Aluno não deve ser criado com data de nascimento futura.
        → ValidationError
        """

        data = {
            "nome": "Aluno Teste",
            "email": "teste@teste.com",
            "data_nascimento": "2094-10-04",
        }

        with self.assertRaises(ValidationError):
            self.client.post(self.url, data, format="json")

        self.assertEqual(Aluno.objects.count(), 0)


class NotaBoletimTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("v1:nota_boletim-list")
        self.user = User.objects.create(username="test")
        self.user.set_password("test")
        self.user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=self.user)[0].key}"
        )

    def test_create_nota_boletim_without_auth(self):

        """
        Nenhum nota deve ser criada sem autenticação.
        """
        self.client.credentials(HTTP_AUTHORIZATION="")

        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(NotaBoletim.objects.count(), 0)

    def test_create_nota_boletim(self):
        """
        Nota deve ser criada.
        """

        data = {
            "boletim": dummyBoletim().pk,
            "disciplina": dummyDisciplina().pk,
            "nota": 7.5,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NotaBoletim.objects.count(), 1)

    def test_create_nota_boletim_converter_nota(self):
        """
        Notas com vírgula ou maiores que 10 devem ser convertidas.
        """

        data = {
            "boletim": dummyBoletim().pk,
            "disciplina": dummyDisciplina().pk,
            "nota": "7,5",
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(float(response.json()["nota"]), 7.5)

        data = {
            "boletim": dummyBoletim().pk,
            "disciplina": dummyDisciplina().pk,
            "nota": 75,
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.json()["nota"]), 7.5)

        self.assertEqual(NotaBoletim.objects.count(), 2)
