import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "general.settings")

import django  # noqa

django.setup()

from channels.auth import AuthMiddlewareStack  # noqa
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
from django.core.asgi import get_asgi_application  # noqa

import auction.routing  # noqa
import chat.routing  # noqa


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
            + auction.routing.websocket_urlpatterns
        )
    ),
})
