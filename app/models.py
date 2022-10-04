from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class Aluno(models.Model):
    email = models.EmailField(
        _("e-mail"),
        help_text=_("E-mail deve ser único"),
        blank=False,
        null=False,
        unique=True,
        max_length=50,
        db_index=True,
    )

    nome = models.CharField(
        _("nome"),
        blank=False,
        null=False,
        unique=True,
        max_length=100,
        db_index=True,
    )

    data_nascimento = models.DateField(
        _("data de nascimento"),
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(
        _("nome"),
        blank=False,
        null=False,
        unique=True,
        max_length=100,
        db_index=True,
    )

    carga_horaria = models.IntegerField(
        _("carga horária"), validators=[MinValueValidator(0), MinValueValidator(9999)]
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Boletim(models.Model):
    aluno = models.ForeignKey(Aluno, null=False, blank=False, on_delete=models.CASCADE)

    data_entrega = models.DateTimeField(_("data de entrega"), null=False, blank=False)

    class Meta:
        verbose_name_plural = "Boletins"
        unique_together = ("aluno", "data_entrega")
        ordering = ["-data_entrega"]

    def __str__(self) -> str:
        return f"{self.aluno} | {self.data_entrega}"


class NotasBoletim(models.Model):
    disciplina = models.ForeignKey(
        Disciplina, null=False, blank=False, on_delete=models.CASCADE
    )

    boletim = models.ForeignKey(
        Boletim, null=False, blank=False, on_delete=models.CASCADE
    )

    nota = models.DecimalField(
        _("nota"),
        null=False,
        blank=False,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name_plural = "Notas dos Boletins"
        ordering = ["-boletim"]

    def __str__(self) -> str:
        return f"{self.disciplina} - {self.nota}"


def check_dates(sender, instance, *args, **kwargs):
    if type(instance) == Aluno:
        if instance.data_nascimento > datetime.date(datetime.now()):
            raise ValidationError(_("Data de nascimento no futuro."))


def normalize_nota(sender, instance, *args, **kwargs):
    if type(instance) == NotasBoletim:
        if instance.nota > 10:
            instance.nota = instance.nota / 10


pre_save.connect(check_dates, sender=Aluno)
pre_save.connect(normalize_nota, sender=NotasBoletim)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
