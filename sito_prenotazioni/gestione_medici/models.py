from django.db import models
from django.conf import settings
from dirtyfields import DirtyFieldsMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from utenti_custom.models import UtenteCustom

class Medico(models.Model):
    """ Definisce il modello del medico """
    
    utente = models.OneToOneField(UtenteCustom, on_delete=models.CASCADE, 
                                  related_name='medico')
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Medici'

    def save(self, *args, **kwargs):
        """ Override del metodo save per aggiungere automaticamente l'utente 
        associato al medico, al gruppo 'Medici' """

        if self._state.adding:
            gruppo = Group.objects.get(name="Medici")
            gruppo.user_set.add(self.utente)

        return super().save(*args, **kwargs)
    
    def __str__(self):
        """ Rappresentazione come stringa del medico che segue la rappresentazione
          nel modello dell'utente """
        
        return self.utente.__str__()
    
class Esame(DirtyFieldsMixin, models.Model):
    """ Definisce il modello per gli esami medici"""

    TIPOLOGIE_POSSIBILI = [
        ('ematochimica', 'Ematochimica'),
        ('urine', 'Urine'),
        ('oculistica', 'Oculistica'),
        ('radiografia', 'Radiografia'),
        ('ginecologia', 'Ginecologia'),
        ('ecografia', 'Ecografia'),
        ('risonanza_magnetica', 'Risonanza magnetica'),
        ('cardiologia', 'Cardiologia'),
        ('allergologia', 'Allergologia'),
        ('gastroenterologia', 'Gastroenterologia'),
        ('urologia', 'Urologia'),
        ('psichiatria', 'Psichiatria'),
        ('pediatria', 'Pediatria'),
        ('otorinolaringologia', 'Otorinolaringologia'),
        ('neurologia', 'Neurologia'),
        ('dermatologia', 'Dermatologia'),
        ('endocrinologia', 'Endocrinologia'),
        ('angiologia', 'Angiologia')
    ]

    STATI_POSSIBILI = [
        ('disponibile', 'Disponibile'),
        ('prenotato', 'Prenotato'),
        ('eseguito', 'Eseguito'),
        ('cancellato', 'Cancellato')
    ]

    tipologia = models.CharField(max_length=30, choices=TIPOLOGIE_POSSIBILI)
    medico = models.ForeignKey(Medico, related_name='esami_caricati', on_delete=models.PROTECT)
    data = models.DateTimeField()
    stato = models.CharField(max_length=20, choices=STATI_POSSIBILI, default='disponibile')
    paziente = models.ForeignKey(UtenteCustom, related_name='esami', null=True, blank=True, 
                               on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        """ Override del metodo save per fare in modo che venga mandata una mail 
        al paziente associato all'esame dopo la prenotazione, se il medico cambia 
        delle informazioni dell'esame o se il medico lo cancella """

        manda_mail = False
        dirty_fields = self.get_dirty_fields(check_relationship=True)

        if self.is_dirty() and not self._state.adding:
            campi_controllo = set(['tipologia', 'data', 'stato'])
            if not set(dirty_fields.keys()).isdisjoint(campi_controllo):
                manda_mail = True

        try:
            if manda_mail:
                if (self.paziente is not None and self.stato == 'prenotato' and
                dirty_fields.get('stato') == 'disponibile'):
                    testo_mail = (f"Gentile utente, l'esame che si svolgera' in"
                                  f" data {self.data.strftime('%d-%m-%Y')} alle" 
                                  f" ore {self.data.strftime('%H:%M:%S')} e' stato prenotato")
                    send_mail(
                    "Notifica prenotazione esame",
                    testo_mail,
                    settings.EMAIL_HOST_USER,
                    [self.paziente.email],
                    fail_silently=False,
                    )

                elif self.paziente is not None:
                    testo_mail = (f"Gentile utente, l'esame prenotato per la data"
                                  f" {self.data.strftime('%d-%m-%Y')} alle ore" 
                                  f" {self.data.strftime('%H:%M:%S')} e' stato modificato")
                    send_mail(
                    "Notifica modifica esame",
                    testo_mail,
                    settings.EMAIL_HOST_USER,
                    [self.paziente.email],
                    fail_silently=False,
                    )

                elif dirty_fields['paziente'] is not None:
                    paziente = UtenteCustom.objects.get(pk=dirty_fields['paziente'])
                    testo_mail = (f"Gentile utente, la cancellazione della prenotazione"
                                  f" per l'esame che si svolgera' in data" 
                                  f" {self.data.strftime('%d-%m-%Y')} alle ore" 
                                  f" {self.data.strftime('%H:%M:%S')} e' stata effettuata")
                    send_mail(
                    "Notifica cancellazione esame",
                    testo_mail,
                    settings.EMAIL_HOST_USER,
                    [paziente.email],
                    fail_silently=False,
                    )
            super().save(*args, **kwargs)
        except Exception as ex:
            print(f"Errore causato da {ex}, un'eccezione del tipo {type(ex)}")
    
    def __str__(self):
        """ Metodo per stampare tutti i campi dell'esame come una frase coerente """
        
        tipologia = self.get_tipologia_display()
        verbo_corretto = "verra'"
        paziente = "nessuno" if self.paziente is None else self.paziente
        frase_finale = f"ed e' stato prenotato da {paziente}"
        
        if self.stato == 'eseguito':
            verbo_corretto = "e' stato"
        elif self.stato == 'cancellato':
            verbo_corretto = 'che doveva essere'
            frase_finale = "e' stato cancellato"
        
        return (f"L'esame della tipologia {tipologia} {verbo_corretto} eseguito"
                f" dal medico {self.medico} in data {self.data.strftime('%d-%m-%Y')}" 
                f" alle ore {self.data.strftime('%H:%M:%S')} {frase_finale}")
    
    def get_nome_medico(self):
        """ Restituisce il nome dell'utente associato al medico """

        return self.medico.utente.first_name
    
    def get_cognome_medico(self):
        """ Restituisce il cognome dell'utente associato al medico """

        return self.medico.utente.last_name
    
    class Meta:
        verbose_name_plural = 'Esami'
        ordering = ['data']

class Commento(models.Model):
    """ Definisce il modello per i commenti ai medici """

    medico = models.ForeignKey(Medico, related_name='commenti', on_delete=models.CASCADE)
    commentatore = models.ForeignKey(UtenteCustom, related_name='commenti', on_delete=models.CASCADE)
    testo = models.TextField(max_length=150)
    data = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Commenti'
        ordering = ['-data']
        constraints = [
            models.UniqueConstraint(
                fields=['medico', 'commentatore'], name='combinazione_medico_commentatore'
            )
        ]
