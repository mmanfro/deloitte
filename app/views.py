import json
import logging
import urllib
from pathlib import Path

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request=request, template_name="app/index.html")


def generate_data_via_REST(request):
    if not User.objects.filter(username="admin"):
        superuser = User.objects.create_superuser(
            username="admin", email=None, password="admin"
        )
        superuser.save()

    # Pega o token de autenticação
    auth = {
        "username": "admin",
        "password": "admin",
    }
    data = urllib.parse.urlencode(auth).encode()
    url = request.build_absolute_uri(reverse("api_token_auth"))
    req = urllib.request.Request(url=url, data=data)
    resp = urllib.request.urlopen(req)
    token = json.load(resp)["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}",
    }

    alunos = json.loads(
        Path(finders.find("app/jsons/alunos.json")).read_text(encoding="utf-8")
    )
    for aluno in alunos:
        data = json.dumps(aluno).encode()
        url = request.build_absolute_uri(reverse("api:aluno-list"))
        req = urllib.request.Request(url=url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                pass
        except Exception as e:
            logging.error(e)
            continue

    disciplinas = json.loads(
        Path(finders.find("app/jsons/disciplinas.json")).read_text(encoding="utf-8")
    )
    for disciplina in disciplinas:
        data = json.dumps(disciplina).encode()
        url = request.build_absolute_uri(reverse("api:disciplina-list"))
        req = urllib.request.Request(url=url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                pass
        except Exception as e:
            logging.error(e)
            continue

    boletins = json.loads(
        Path(finders.find("app/jsons/boletins.json")).read_text(encoding="utf-8")
    )
    for boletim in boletins:
        data = json.dumps(boletim).encode()
        url = request.build_absolute_uri(reverse("api:boletim-list"))
        req = urllib.request.Request(url=url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                pass
        except Exception as e:
            logging.error(e)
            continue

    notas_boletim = json.loads(
        Path(finders.find("app/jsons/notasBoletim.json")).read_text(encoding="utf-8")
    )
    for nota_boletim in notas_boletim:
        data = json.dumps(nota_boletim).encode()
        url = request.build_absolute_uri(reverse("api:notas_boletim-list"))
        req = urllib.request.Request(url=url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                pass
        except Exception as e:
            logging.error(e)
            continue

    return HttpResponse(content=_("Dados gerados!"))
