from django.shortcuts import render
from .models import Post

# Create your views here.


def lista_posts(request):
    posts = Post.objects.order_by('-criado_em')
    return render(request, 'postagens.html', {'posts': posts})
