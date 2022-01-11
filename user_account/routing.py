from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # /test_ws_preguntas/
    re_path(r'test_ws_preguntas/$', consumers.ChatConsumer.as_asgi()),

]