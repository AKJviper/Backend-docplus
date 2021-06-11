import os
import channels
from django.conf.urls import url
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from chat.consumers import ChatConsumer
from channels.layers import get_channel_layer
from .middlewares import JwtAuthMiddlewareStack

channel_layer = get_channel_layer()
application = ProtocolTypeRouter({
    # Just HTTP for now. (We can add other protocols later.)
    'websocket':JwtAuthMiddlewareStack(
    AuthMiddlewareStack(
    AllowedHostsOriginValidator(
            URLRouter(
                [
                    re_path(r"^chat/messages/(?P<username>[\w.@+-]+)/$", ChatConsumer.as_asgi()),
                ]
            )
        )))
    })