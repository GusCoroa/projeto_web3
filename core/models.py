from django.db import models

from django.urls import reverse

class ExportPdfMixin:
    change_form_template = 'admin/export_pdf_change_form.html'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            # monta a URL correta
            name = f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_export_pdf'
            extra_context['export_pdf_url'] = reverse(name, args=[object_id])
        return super().changeform_view(request, object_id, form_url, extra_context)
