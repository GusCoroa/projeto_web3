from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from evento.models import Evento
from insumo.models import Insumo
from voluntario.models import Voluntario

SEARCH_MODELS = {
    'evento':    (Evento,    'nome',       'Eventos'),
    'insumo':    (Insumo,    'nome',       'Insumos'),
    'voluntario':(Voluntario,'nome',       'Voluntários'),
}

def search_view(request):
    q   = request.GET.get('q','')
    cat = request.GET.get('category','all')

    # se categoria específica, manda pro changelist com ?q=
    if cat != 'all' and cat in SEARCH_MODELS:
        model, _, _ = SEARCH_MODELS[cat]
        url = reverse(f'admin:{model.meta.app_label}{model._meta.model_name}_changelist')
        return HttpResponseRedirect(f'{url}?q={q}')

    # senão mostra a página custom
    def make_entries(model, field):
        return [
            {
                'obj': obj,
                'url': reverse(
                    f'admin:{obj.meta.app_label}{obj._meta.model_name}_change',
                    args=[obj.pk]
                )
            }
            for obj in model.objects.filter({f'{field}__icontains': q})
        ]

    results = {
        label: make_entries(model, field)
        for key,(model, field, label) in SEARCH_MODELS.items()
    }

    categories = [('all','Todas')] + [(k,label) for k,(_,_,label) in SEARCH_MODELS.items()]
    ctx = {
        **admin.site.each_context(request),
        'results': results,
        'q': q,
        'categories': categories,
        'selected_cat': cat,
    }
    return TemplateResponse(request, 'admin/search_results.html', ctx)

orig = admin.site.get_urls
def get_urls():
    return [ path('search/', admin.site.admin_view(search_view), name='search') ] + orig()
admin.site.get_urls = get_urls