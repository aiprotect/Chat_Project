from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # مسیر با uuid و در نظر گرفتن پیشوند زبان (اگر لازم باشه)
    re_path(r'ws/chat/(?P<room_id>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]
