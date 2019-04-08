from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import (
                    AllowedHostsOriginValidator,
                    OriginValidator
                )
from delivery.consumers import TaskConsumer, CurTaskConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^raise_task/$", TaskConsumer),
                    url(r"^get_cur_task/$", CurTaskConsumer),
                ]
            )
        )
    )
})
