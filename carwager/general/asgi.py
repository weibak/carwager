import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Сначала настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'general.settings')
django.setup()  # Важно: вызываем setup ДО импорта приложений

# Теперь импортируем routing
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
