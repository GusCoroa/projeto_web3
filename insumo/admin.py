from django.contrib import admin
from .models import Insumo
from django.urls import reverse
from django.utils.html import format_html


# Personalizar cabeçalhos
admin.site.site_header = "Sistema de Administração FFC"
admin.site.site_title = "Administração"
admin.site.index_title = "Painel de Controle"


@admin.register(Insumo)

class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'quantidade','acao_excluir')
    list_display_links = ('nome',)
    search_fields = ("nome","descricao")


    def acao_excluir(self, obj):
        url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        return format_html('<a class="deletelink" href="{}">&times; Excluir</a>', url)
    acao_excluir.short_description = 'Ações'
# from django.urls import reverse
# from django.utils.html import format_html

# @admin.register(Evento)
# class EventoAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'descricao', 'data', 'acao_excluir')
#     list_display_links = ('nome',)  # deixa só o nome clicável
#     search_fields = ("nome", "gerente__nome")

#     def acao_excluir(self, obj):
#         url = reverse(
#             f'admin:{obj.meta.app_label}{obj._meta.model_name}_delete',
#             args=[obj.pk]
#         )
#         return format_html(
#             '<a class="deletelink" href="{}">&times; Excluir</a>',
#             url
#         )
#     acao_excluir.short_description = ''  # sem título de coluna