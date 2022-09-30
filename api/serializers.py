from cgitb import lookup
from rest_framework import serializers
from app.models import *


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = "__all__"


class BoletimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boletim
        fields = "__all__"


class NotasBoletimSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.CharField(source="disciplina", read_only=True)
    boletim_nome = serializers.CharField(source="boletim", read_only=True)

    def to_internal_value(self, data):
        temp_data = data.copy()
        temp_data["nota"] = locale_float(data["nota"])
        data = temp_data

        return super(NotasBoletimSerializer, self).to_internal_value(data)

    class Meta:
        model = NotaBoletim
        fields = "__all__"
