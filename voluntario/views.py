from django.shortcuts import render, redirect
from .forms import VoluntarioFormulario
from .models import  Voluntario
from django.db import IntegrityError
import logging
from django.shortcuts import render

def pagina_voluntario(request):
    return render(request, 'voluntario.html')

def eventos(request):
    return render(request, 'eventos.html')

def politica(request):
    return render(request, 'politica.html')

logger = logging.getLogger(__name__)

def voluntario(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        tel = request.POST['tel']
        cpf = request.POST['cpf']
        dataNascimento = request.POST['dataNascimento']
        sexo = request.POST['sexo']
        
        if Voluntario.objects.filter(cpf=cpf).exists():
            return render(request, 'voluntario.html', {'mensagem': 'CPF já cadastrado.'})
        if Voluntario.objects.filter(telefone=tel).exists():
            return render(request, 'voluntario.html', {'mensagem': 'Telefone já cadastrado.'})
        if Voluntario.objects.filter(email=email).exists():
            return render(request, 'voluntario.html', {'mensagem': 'E-mail já cadastrado.'})

        try:
            cadastro_voluntario  = Voluntario.objects.create(
                nome = fullname,
                email = email,
                telefone = tel,
                cpf = cpf,
                dataNascimento = dataNascimento,
                sexo = sexo
            )
            cadastro_voluntario.save()
            return render(request, 'voluntario.html',  {'mensagem': "Cadastro realizado com sucesso!"})
        except IntegrityError:
            return render(request,  'voluntario.html', {'mensagem': 'Erro  no cadastro. Tente novamente.'})

    return render(request, 'voluntario.html')