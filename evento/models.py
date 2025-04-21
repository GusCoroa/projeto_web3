from django.db import models
from insumo.models import Insumo
from voluntario.models import Voluntario

# Create your models here.

class Evento (models.Model):
    nome = models.CharField("Nome do Evento", max_length = 50)
    descricao = models.CharField("Descrição",max_length = 100)
    data = models.DateField("Data do Evento")
    local = models.CharField("Local",max_length = 50)

    gerente = models.ForeignKey(
        Voluntario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Gerente do Evento",
        related_name="eventos_gerenciados"
    )

    insumo = models.ManyToManyField(Insumo, blank = True)
    voluntario = models.ManyToManyField(Voluntario, blank = True)
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.nome
