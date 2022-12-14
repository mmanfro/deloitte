# Generated by Django 4.1.1 on 2022-10-01 14:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Aluno",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        help_text="e-mail deve ser único",
                        max_length=50,
                        unique=True,
                        verbose_name="e-mail",
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        db_index=True, max_length=100, unique=True, verbose_name="nome"
                    ),
                ),
                (
                    "data_nascimento",
                    models.DateField(verbose_name="data de nascimento"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Boletim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data_entrega", models.DateTimeField(verbose_name="data de entrega")),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.aluno"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Boletins",
                "unique_together": {("aluno", "data_entrega")},
            },
        ),
        migrations.CreateModel(
            name="Disciplina",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        db_index=True, max_length=100, unique=True, verbose_name="nome"
                    ),
                ),
                (
                    "carga_horaria",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MinValueValidator(9999),
                        ],
                        verbose_name="carga horária",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotasBoletim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nota",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="nota",
                    ),
                ),
                (
                    "boletim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.boletim"
                    ),
                ),
                (
                    "disciplina",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="app.disciplina",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Notas dos Boletins",
            },
        ),
    ]
