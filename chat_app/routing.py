from django.urls import re_path

from .consumers import ChatConsumer

"""
WebSocket URL routing for the chat application.

This module defines WebSocket endpoints and maps them to their corresponding
consumers. Each URL pattern includes dynamic segments to identify the
users participating in the chat.

Attributes:
    websocket_urlpatterns (list): List of WebSocket URL patterns handled by Channels.
"""

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_id>\d+)/$", ChatConsumer.as_asgi()),
]
