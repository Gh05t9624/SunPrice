# SunPrice/asgi.py

import os  # Assurez-vous que cette ligne est présente
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter  # type: ignore
from channels.auth import AuthMiddlewareStack  # type: ignore
from SunApp.routing import websocket_urlpatterns

# Définir les paramètres Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Affichez la variable d'environnement pour le débogage
print(os.environ.get('DJANGO_SETTINGS_MODULE'))

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
