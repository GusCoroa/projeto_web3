from django.contrib import admin
from .models import Evento
from .models import Post
from django.urls import reverse
from django.utils.html import format_html



# Personalizar cabeçalhos
admin.site.site_header = "Sistema de Administração FFC"
admin.site.site_title = "Administração"
admin.site.index_title = "Painel de Controle"



# class EventoAdmin(admin.ModelAdmin):
#     list_display = ("nome", "data", "local", "gerente", 'excluir_link')
#     list_display_links = ('nome',)




#     def acao_excluir(self, obj):
#         url = reverse(
#             f'admin:{obj.meta.app_label}{obj._meta.model_name}_delete',
#             args=[obj.pk]
#         )
#         return format_html(
#             '<a class="deletelink" href="{}">&times; Excluir</a>',
#             url
#         )
#     acao_excluir.short_description = ''
    
#     # def botao_excluir(self, obj):
#     #     url = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),
#     #         args=[obj.pk]
#     #     )
#     #     return format_html('<a class="button deletelink" href="{}">Excluir</a>', url)
#     # botao_excluir.short_description = ''
# class CustomUserAdmin(UserAdmin):
#     class Media:
#         css = {
#             "all": ("css/custom_admin.css",)
#         }







@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data', 'acao_excluir')
    list_display_links = ('nome',)  # deixa só o nome clicável
    # change_form_template = 'admin/evento/evento/change_form.html'
    search_fields = ("nome", "gerente__nome")

    def acao_excluir(self, obj):
        url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        return format_html('<a class="deletelink" href="{}">&times; Excluir</a>', url)
    acao_excluir.short_description = 'Ações'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'acao_excluir')
    list_display_links = ('titulo',)  # deixa só o nome clicável
    # change_form_template = 'admin/evento/evento/change_form.html'
    search_fields = ("titulo",)

    def acao_excluir(self, obj):
        url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        return format_html('<a class="deletelink" href="{}">&times; Excluir</a>', url)
    acao_excluir.short_description = 'Ações'