# backend/config/middleware.py

class ApiKeyMiddleware:
    """
    Middleware PASSTHROUGH - L'autenticazione è gestita interamente da DRF.
    Questo middleware non fa nulla, serve solo per compatibilità.
    """

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Semplicemente passa tutto a DRF che gestisce l'autenticazione tramite TokenAuthentication
        return self.get_response(request)
