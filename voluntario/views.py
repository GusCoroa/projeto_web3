from django.shortcuts import render, redirect
from .forms import VoluntarioFormulario
from .models import  Voluntario
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def voluntario(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        tel = request.POST['tel']
        cpf = request.POST['cpf']
        dataNascimento = request.POST['dataNascimento']
        sexo = request.POST['sexo']
        # sexo = True if sexo.lower() == 'masculino' else False
        
        if Voluntario.objects.filter(cpf=cpf).exists():
            return render(request, 'formulario.html', {'mensagem': 'CPF já cadastrado.'})
        if Voluntario.objects.filter(telefone=tel).exists():
            return render(request, 'formulario.html', {'mensagem': 'Telefone já cadastrado.'})
        if Voluntario.objects.filter(email=email).exists():
            return render(request, 'formulario.html', {'mensagem': 'E-mail já cadastrado.'})

        try:
            cadastro_voluntario  = Voluntario.objects.create(
                nome = fullname,
                email = email,
                telefone = tel,
                cpf = cpf,
                dataNascimento = dataNascimento,
                sexo = sexo
            )
            return render(request, 'formulario.html',  {'mensagem': "Cadastro realizado com sucesso!"})
        except IntegrityError:
            return render(request,  'formulario.html', {'mensagem': 'Erro  no cadastro. Tente novamente.'})
        # cadastro_voluntario = Voluntario.objects.create(nome = fullname, email = email, telefone = tel, cpf = cpf, dataNascimento = dataNascimento, sexo = sexo)

    return render(request, 'formulario.html')