from django.urls import path
from .views import *

app_name = "gestione_medici"

urlpatterns = [
    path('crea_esame/', CreateEsameView.as_view(), name='crea_esame'),
    path('esami_caricati/', esami_caricati, name='esami_caricati'),
    path('modifica_esame/<pk>/', ModificaEsameView.as_view(), name='modifica_esame'),
    path('modifica_informazioni/<pk>/', ModificaInformazioniView.as_view(), name='modifica_informazioni'),
    path('informazioni_medico/<pk>/', InformazioniMedicoView.as_view(), name='informazioni_medico'),
    path('recensioni_medico/<pk>/', CommentiMedicoView.as_view(), name='commenti_totali'),
    path('scrivi_recensione/<pk>/', CreaCommentoView.as_view(), name='crea_commento'),
]
