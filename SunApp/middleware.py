# middleware.py

from .utils import obtenir_marque_dispositif

class MarqueDispositifMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Vérifier si l'utilisateur est connecté
        if request.user.is_authenticated:
            # Obtenir la marque du dispositif et la stocker dans la session
            marque_dispositif = obtenir_marque_dispositif(request)
            request.session['marque_dispositif'] = marque_dispositif

        return response
