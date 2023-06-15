from django.urls import path
from .consumers import ChatAssistenza

ws_urlpatterns = [
path("ws/chatws/<int:room>/", ChatAssistenza.as_asgi())
]