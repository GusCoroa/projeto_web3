"""
URL configuration for bd_web3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from voluntario import views

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    # rotas pra redefinição de senha admin
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Menu
    path('', TemplateView.as_view(template_name='inicio.html'), name='home'), 
    # formulario
    path('voluntario/', views.voluntario, name='voluntario'),
    # Eventos
    path('eventos/', views.eventos, name='eventos'),
    # Postagens
    path('postagens/', views.postagens, name='postagens'),
    # Politica
    path('politica/', views.politica, name='politica'),
    # # Pagina de postagens
    # path('posts/', include('evento.urls')),   
]

# desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
# Para imagens
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
