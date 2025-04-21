from django.utils import translation

class ForcarIdiomaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate('pt-br')
        response = self.get_response(request)
        translation.deactivate()
        return response
