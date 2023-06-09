from django.urls import path, re_path, register_converter
from .views import *
from .path_converters import *

app_name = "gestione_medici"

register_converter(NameConverter, "name")
register_converter(DateConverter, "date")

urlpatterns = [
    path('ricerca_esami/', ricerca_esami, name='ricerca_esami'),
    path("ricerca_esami/<name:nome>/<name:cognome>/<name:data_inizio>/<name:data_fine>/<name:tipologia>/", 
         EsameRicercaView.as_view(), name='ricerca_esami_risultati'),
    path('crea_esame/', CreateEsameView.as_view(), name='crea_esame'),
    path('esami_caricati/', esami_caricati, name='esami_caricati'),
    path('modifica_esame/<pk>/', ModificaEsameView.as_view(), name='modifica_esame'),
    path('modifica_informazioni/<pk>/', ModificaInformazioniView.as_view(), name='modifica_informazioni'),
    path('informazioni_medico/<pk>/', InformazioniMedicoView.as_view(), name='informazioni_medico'),
]
