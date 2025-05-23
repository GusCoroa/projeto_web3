from django.db import models

# Create your models here.

class Insumo (models.Model):
    nome = models.CharField("Nome do Insumo", max_length = 50)
    descricao = models.CharField("Descrição", max_length = 100)
    quantidade = models.IntegerField("Quantidade")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    def __str__(self):
        return self.nome

   