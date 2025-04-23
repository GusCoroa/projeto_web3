from django.db import models

# Create your models here.

class Voluntario (models.Model):

    GENERO_OPCOES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('outro', 'Outro'),
    ]

    cpf = models.CharField("CPF", max_length = 50, unique = True)
    nome = models.CharField("Nome", max_length = 50)
    sexo = models.CharField("Sexo", max_length=10, choices=GENERO_OPCOES)
    email = models.EmailField("E-mail")
    dataNascimento = models.DateField("Data de Nascimento")
    funcao = models.CharField("Função", max_length = 50)
    telefone = models.CharField("Telefone", max_length = 15)
    
    
    class Meta:
        verbose_name = "Voluntário"
        verbose_name_plural = "Voluntários"

    def __str__(self):
        return self.nome