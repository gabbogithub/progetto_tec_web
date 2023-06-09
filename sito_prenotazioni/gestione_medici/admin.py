from django.contrib import admin
from .models import Medico, Esame, Commento

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    lista_display = ('utente',)
    search_fields = ('utente__first_name__startswith',)

@admin.register(Esame)
class EsameAdmin(admin.ModelAdmin):
    list_display = ('tipologia', 'medico', 'data', 'stato', 'paziente')
    list_filter = ('stato', 'tipologia', 'data')
    search_fields = ('data', 'medico__utente__first_name', 'medico__utente__last_name',
                     'paziente__first_name', 'paziente__last_name')

admin.site.register(Commento)
