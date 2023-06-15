from django.db import models
from utenti_custom.models import UtenteCustom

class Chat(models.Model):
    STATI_POSSIBILI = [
        ('creato', 'Creato'),
        ('in_attesa', 'In attesa'),
        ('in_corso', 'In corso'),
        ('terminato', 'Terminato')
    ]

    stato = stato = models.CharField(max_length=10, choices=STATI_POSSIBILI, default='creato')
    membro_assistenza = models.ForeignKey(UtenteCustom, related_name='chat', null=True, blank=True, 
                                                 on_delete=models.CASCADE)
    identificativi_utente = models.CharField(max_length=30)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Chat'
        ordering = ['data']
