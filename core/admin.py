from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from evento.models import Evento
from insumo.models import Insumo
from voluntario.models import Voluntario
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import A4

class ExportPdfMixin:
    change_form_template = 'admin/export_pdf_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:object_id>/export_pdf/',
                self.admin_site.admin_view(self.export_pdf_view),
                name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_export_pdf'
            ),
        ]
        return custom + urls

    def export_pdf_view(self, request, object_id):
        obj = get_object_or_404(self.model, pk=object_id)
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        logo_path = settings.BASE_DIR / 'static' / 'Imagens' / 'logoheader.png'
        p.drawImage(str(logo_path), 50, 740, width=100, height=100, mask='auto')
        p.setFont("Helvetica-Bold", 20)
        p.drawString(200, 800, f"Federação Fluminense de Capoeira")
        p.drawCentredString(300, 750, f"Relatório de {self.model._meta.verbose_name.title()}")
        
        width, height = A4
        margin       = 50
        pad_x        = 250    # espaço entre label e valor
        line_height  = 24     # espaçamento vertical entre linhas
        y = height - 200
        y = 700
        all_fields = list(self.model._meta.fields) + list(self.model._meta.many_to_many)
        p.setFont("Helvetica", 12)
        for field in all_fields:
            label = field.verbose_name.title()
            if field.many_to_many:
                itens = getattr(obj, field.name).all()
                value = ' | '.join(str(i) for i in itens) or '–'
            else:
                value = getattr(obj, field.name) or '–'
                
            # Label em negrito e um pouco maior
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y, f"{label}:")

            # Valor em fonte normal, desenhado um pouco mais pra direita
            p.setFont("Helvetica", 12)
            p.drawString(margin + pad_x, y, str(value))
            
            y -= 18
            if y < margin:
                p.showPage()
                y = height - margin

        # for field in self.model._meta.fields:
        #     label = field.verbose_name.title()
        #     value = getattr(obj, field.name)
        #     p.setFont("Helvetica", 12,)
        #     p.drawString(50, y, f"{label}: {value}")
        #     y -= 20
        #     if y < 50:
        #         p.showPage()
        #         y = 800
        p.showPage()
        p.save()
        buffer.seek(0)
        resp = HttpResponse(buffer, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="Relatorio_{obj.nome}.pdf"'
        return resp



# def export_pdf_view(self, request, object_id):
#     obj = get_object_or_404(self.model, pk=object_id)
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#     logo_path = settings.BASE_DIR / 'static' / 'images' / 'logo.png'
#     p.drawImage(str(logo_path), 50, 740, width=100, height=100)
#     p.setFont("Helvetica-Bold", 20)
#     p.drawCentredString(300, 760, f"Relatório de {self.model._meta.verbose_name.title()}")
#     y = 700
#     for field in self.model._meta.fields:
#         label = field.verbose_name.title()
#         value = getattr(obj, field.name)
#         p.setFont("Helvetica", 12)
#         p.drawString(50, y, f"{label}: {value}")
#         y -= 20
#         if y < 50:
#             p.showPage()
#             y = 800
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     resp = HttpResponse(buffer, content_type='application/pdf')
#     resp['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}_{object_id}.pdf"'
#     return resp

    
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
