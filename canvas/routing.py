from django.urls import re_path
from .consumers import CanvasConsumer

websocket_urlpatterns = [
    re_path(r'ws/canvases/(?P<canvas_id>\w+)/$', CanvasConsumer.as_asgi()),
]