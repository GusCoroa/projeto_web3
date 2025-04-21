from django.contrib import admin
from .models import Evento
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Personalizar cabeçalhos
admin.site.site_header = "Sistema de Administração FFC"
admin.site.site_title = "Administração"
admin.site.index_title = "Painel de Controle"

admin.site.register(Evento)

class EventoAdmin(admin.ModelAdmin):
    list_display = ("nome", "data", "local", "gerente")  # mostra o gerente na listagem
    search_fields = ("nome", "gerente__nome")  # permite buscar pelo nome do gerente



class CustomUserAdmin(UserAdmin):
    class Media:
        css = {
            "all": ("css/custom_admin.css",)
        }

# Substitui o User padrão pelo seu
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)