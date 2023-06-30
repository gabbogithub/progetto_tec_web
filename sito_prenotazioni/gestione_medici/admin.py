from django.contrib import admin
from .models import Medico, Esame, Commento

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    """ Modifica della pagina admin standard per mostrare i vari campi di ogni 
    medico escluso l'id e la descrizione e per aggiungere filtri e ricerca """

    lista_display = ('utente',)
    search_fields = ('utente__first_name', 'utente__last_name')

@admin.register(Esame)
class EsameAdmin(admin.ModelAdmin):
    """ Modifica della pagina admin standard per mostrare i vari campi di ogni 
    esame escluso l'id e per aggiungere filtri e ricerca """

    list_display = ('tipologia', 'medico', 'data', 'stato', 'paziente')
    list_filter = ('stato', 'data', 'tipologia')
    search_fields = ('data', 'medico__utente__first_name', 'medico__utente__last_name',
                     'paziente__first_name', 'paziente__last_name')

@admin.register(Commento)
class CommentoAdmin(admin.ModelAdmin):
    """ Modifica della pagina admin standard per mostrare i vari campi di ogni 
    commento escluso l'id e il testo e per aggiungere filtri e ricerca """

    list_display = ('medico', 'commentatore', 'data')
    list_filter = ('data',)
    search_fields = ('data', 'medico__utente__first_name', 'medico__utente__last_name',
                     'commentatore__first_name', 'commentatore__last_name')
