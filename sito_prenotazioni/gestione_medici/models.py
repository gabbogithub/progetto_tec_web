from django.db import models
from django.conf import settings
from datetime import datetime

class Esame(models.Model):
    '''Classe che rappresenta il modello per gli esami medici'''

    TIPOLOGIE_POSSIBILI = [
        ("ematochimica", "Ematochimica"),
        ("urine", "Urine"),
        ("oculistica", "Oculistica"),
        ("radiografia", "Radiografia"),
        ("ginecologia", "Ginecologia"),
        ("ecografia", "Ecografia"),
        ("risonanza_magnetica", "Risonanza magnetica"),
        ("cardiologia", "Cardiologia"),
        ("allergologia", "Allergologia"),
        ("gastroenterologia", "gastroenterologia"),
        ("urologia", "Urologia"),
        ("psichiatria", "Psichiatria"),
        ("pediatria", "Pediatria"),
        ("otorinolaringologia", "Otorinolaringologia"),
        ("neurologia", "Neurologia"),
        ("dermatologia", "Dermatologia"),
        ("endocrinologia", "Endocrinologia"),
        ("angiologia", "Angiologia")
    ]

    STATI_POSSIBILI = [
        ("disponibile", "Disponibile"),
        ("prenotato", "Prenotato"),
        ("eseguito", "Eseguito"),
        ("cancellato", "Cancellato")
    ]

    tipologia = models.CharField(max_length=30, choices=TIPOLOGIE_POSSIBILI)
    medico = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="esami_caricati", on_delete=models.PROTECT)
    data = models.DateTimeField(format="%Y-%m-%d %H:%M")
    stato = models.CharField(max_length=20, choices=STATI_POSSIBILI, default="disponibile")
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="esami_prenotati", null=True, blank=True, 
                               on_delete=models.SET_NULL)
    
    def __str__(self):
        '''Metodo per stampare tutti i campi dell'esame come una frase coerente'''

        verbo = "verra'" if datetime.today() < self.data else "e' stato"
        return (f"L'esame della tipologia {self.tipologia} {verbo} eseguito dal medico {self.medico.first_name}"
                f" {self.medico.last_name} in data {self.data} ed e' stato prenotato da {self.utente}")

    class Meta:
        '''Classe che ha lo scopo di specificare il nome plurale per il modello "Esame"'''

        verbose_name_plural = "Esami"
