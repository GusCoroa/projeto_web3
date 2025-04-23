from django import forms 
from .models import Voluntario
from django.core.exceptions import ValidationError

class VoluntarioFormulario(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = ['nome', 'email', 'telefone', 'cpf', 'dataNascimento', 'sexo']

    def checkCpf(self):
        cpf = self.cleaned_data['cpf']
        if Voluntario.objects.filter(cpf=cpf).exists():
            raiseValidationError("CPF já cadastrado.")
        return cpf