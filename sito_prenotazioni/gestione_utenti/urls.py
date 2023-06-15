from django.urls import path, register_converter
from .path_converters import EmptyStringConverter
from .views import *

app_name = 'gestione_utenti'

register_converter(EmptyStringConverter, 'empty_str')

urlpatterns = [
    path("situazione/", situazione_utente, name="situazione"),
    path("stampa_esame/<int:pk>/", stampa_esame, name="stampa_esame"),
    path("cancella_prenotazione/<int:pk>/", cancella_prenotazione, name="cancella_prenotazione"),
    path('ricerca_esami/', ricerca_esami, name='ricerca_esami'),
    path("ricerca_esami/<empty_str:nome>/<empty_str:cognome>/<empty_str:data_inizio>/<empty_str:data_fine>/<empty_str:tipologia>/", 
         EsameRicercaView.as_view(), name='ricerca_esami_risultati'),
    path('prenota_esame/<int:pk>/', prenota_esame, name='prenota_esame')
]