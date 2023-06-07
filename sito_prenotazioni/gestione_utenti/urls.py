from django.urls import path
from .views import *

app_name = 'gestione_utenti'

urlpatterns = [
    path("situazione/", situazione_utente, name="situazione"),
    path("stampa_esame/<pk>/", stampa_esame, name="stampa_esame"),
    path("cancella_prenotazione/<pk>/", cancella_prenotazione, name="cancella_prenotazione")
]