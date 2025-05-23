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
    q   = request.GET.get('q','').strip()
    cat = request.GET.get('category','all')
    if cat != 'all' and cat in SEARCH_MODELS:
        model, _, _ = SEARCH_MODELS[cat]
        url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
        return HttpResponseRedirect(f'{url}?q={q}')
    def make_entries(model, field):
        return [
            {
                'obj': obj,
                'url': reverse(
                    f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
                    args=[obj.pk]
                )
            }
            for obj in model.objects.filter(**{f'{field}__icontains': q})
        ]
    results = {
        label: make_entries(model, field)
        for key,(model, field, label) in SEARCH_MODELS.items()
    }
    categories = [('all','Todas')] + [(k,label) for k,(_,_,label) in SEARCH_MODELS.items()]
    context = {
        **admin.site.each_context(request),
        'results': results,
        'q': q,
        'categories': categories,
        'selected_cat': cat,
    }
    return TemplateResponse(request, 'admin/search_results.html', context)

orig_get_urls = admin.site.get_urls
def get_urls():
    return [
        path('search/', admin.site.admin_view(search_view), name='search'),
    ] + orig_get_urls()
admin.site.get_urls = get_urls
