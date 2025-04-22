from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Voluntario

def voluntario(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        tel = request.POST['tel']
        cpf = request.POST['cpf']
        dataNascimento = request.POST['dataNascimento']
        sexo = request.POST['sexo']
        sexo = True if sexo.lower() == 'masculino' else False
        cadastro_voluntario = Voluntario.objects.create(nome = fullname, email = email, telefone = tel, cpf = cpf, dataNascimento = dataNascimento, sexo = sexo)

        return redirect(request, 'home')
    return render(request, 'formulario.html')