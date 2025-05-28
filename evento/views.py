from django.shortcuts import render
from .models import Post
from .models import Evento

# Create your views here.


def lista_posts(request):
    posts = Post.objects.order_by('-criado_em')
    return render(request, 'postagens.html', {'posts': posts})

def lista_eventos(request):
    posts = Evento.objects.order_by('data')
    return render(request, 'eventos.html', {'posts': posts})
