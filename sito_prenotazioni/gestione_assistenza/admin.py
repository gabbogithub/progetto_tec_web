from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """ Modifica della pagina admin standard per mostrare i vari campi di ogni 
    chat escluso l'id e per aggiungere filtri e ricerca """

    list_display = ('stato', 'membro_assistenza', 'identificativi_utente', 'data')
    list_filter = ('stato', 'data')
    search_fields = ('data', 'membro_assistenza__first_name', 'membro_assistenza__last_name',
                     'identificativi_utente')
