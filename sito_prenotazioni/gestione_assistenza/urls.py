from django.urls import path
from .views import *

app_name = 'gestione_assistenza'

urlpatterns = [
    path('richiesta_assistenza', richiesta_assistenza, name='richiesta_assistenza'),
    path('chat_assistenza/<str:identificativi>/<int:pk>', chat_assistenza, name='chat_assistenza'),
    path('utenti_attesa/', UtentiAttesaView.as_view(), name='utenti_attesa')
]
