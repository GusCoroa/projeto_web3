from django.contrib import admin
from .models import Insumo


# Personalizar cabeçalhos
admin.site.site_header = "Sistema de Administração FFC"
admin.site.site_title = "Administração"
admin.site.index_title = "Painel de Controle"


admin.site.register(Insumo)
