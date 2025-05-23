from django.contrib import admin
from django.urls import path, reverse
from evento.models import Evento
from insumo.models import Insumo
from voluntario.models import Voluntario
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import A4
import textwrap
from reportlab.lib.utils    import ImageReader
from django.utils.text import slugify



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
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # — Logo e título —
        logo = ImageReader(settings.BASE_DIR / 'static' / 'Imagens' / 'logoheader.png')
        p.drawImage(logo, 15, height-100, width=100, height=100, mask='auto')
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width/2, height-50, "Federação Fluminense de Capoeira")
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width/2, height-80, f"Relatório de {self.model._meta.verbose_name.title()}")

        # — Configurações de layout —
        margin      = 30
        line_height = 18
        col1_x = margin
        col2_x = margin + 150
        y      = height - 180

        p.setFont("Helvetica", 12)
        # quantos chars cabem na descrição
        max_width      = 600
        avg_char_width = p.stringWidth("M", "Helvetica", 12)
        max_chars      = int(max_width / avg_char_width)

        all_fields = list(self.model._meta.fields) + list(self.model._meta.many_to_many)
        for field in all_fields:
            label = field.verbose_name.title()

            # 1) desenha a label
            p.setFont("Helvetica-Bold", 12)
            p.drawString(col1_x, y, f"{label}:")
            
            # 2) monta lista de linhas pra esse campo
            if field.many_to_many:
                lines = [f"• {str(i)}" for i in getattr(obj, field.name).all()] or ["–"]
            elif field.name == "descricao":
                raw   = getattr(obj, field.name) or ""
                lines = textwrap.wrap(raw, max_chars) or ["–"]
            else:
                raw   = getattr(obj, field.name)
                lines = [str(raw)] if raw is not None else ["–"]

            # 3) desenha cada linha começando em col2_x
            p.setFont("Helvetica", 12)
            for line in lines:
                y -= line_height
                if y < margin:
                    p.showPage()
                    y = height - margin
                    p.setFont("Helvetica", 12)
                p.drawString(col2_x, y+20, line)

            # 4) adiciona um espaçamento extra antes do próximo campo
            y -= line_height / 2
            if y < margin:
                p.showPage()
                y = height - margin

            # 5) nova página se necessário
            if y < margin:
                p.showPage(); y = height - margin

        # for field in all_fields:
        #     label = field.verbose_name.title()
        #     # extrai valor (tratando M2M)
        #     if field.many_to_many:
        #         itens = getattr(obj, field.name).all()
        #         value = ', '.join(str(i) for i in itens) or '–'
        #     else:
        #         raw = getattr(obj, field.name)
        #         value = str(raw) if raw is not None else '–'

        #     # desenha label em negrito
        #     p.setFont("Helvetica-Bold", 12)
        #     p.drawString(margin, y, f"{label}:")
        #     y -= line_height

        #     # desenha valor
        #     p.setFont("Helvetica", 12)
        #     if field.name == "descricao":
        #         # quebra em várias linhas
        #         for line in textwrap.wrap(value, max_chars):
        #             p.drawString(margin + 10, y, line)
        #             y -= line_height
        #             if y < margin:
        #                 p.showPage()
        #                 y = height - margin
        #     else:
        #         p.drawString(margin + pad_x, y, value)
        #         y -= line_height

        #     # nova página se necessário
        #     if y < margin:
        #         p.showPage()
        #         y = height - margin

        # finaliza e retorna
        p.showPage()
        p.save()
        buffer.seek(0)
        filename = f"{slugify(obj.nome)}.pdf"
        resp = HttpResponse(buffer, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="{filename}"'
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
