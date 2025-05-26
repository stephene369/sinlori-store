import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Masquer les headers qui révèlent Django
        if 'Server' in response:
            del response['Server']
        
        response['Server'] = 'WebServer'
        
        return response

    def process_exception(self, request, exception):
        # Logger l'erreur sans la révéler à l'utilisateur
        logger.error(f"Erreur sur {request.path}: {str(exception)}")
        return None