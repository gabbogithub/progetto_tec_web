from django.test import TestCase
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from django.core import mail
from django.conf import settings
from .models import Esame, Medico
from utenti_custom.models import UtenteCustom

def creazione_utenti_esame():
    """ Crea un utente, un medico con relativo utente e un esame """

    utente_medico = UtenteCustom.objects.create_user(email='prova1@gmail.com', password='prova1', 
                                                        first_name='medico', last_name='di prova')
    medico = Medico.objects.create(utente=utente_medico)
    utente_normale = UtenteCustom.objects.create_user(email='prova2@gmail.com', password='prova2', 
                                                        first_name='utente2', last_name='di prova 2')
    data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
    esame = Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, 
                                    stato='disponibile')
    return (utente_normale, esame)

class EsameMetodiTest(TestCase):
    """ Definisce i test per l'invio di mail agli utenti in relazione all'esame 
    prenotato """
    
    def test_invio_mail_prenotazione(self):
        """ Testa che venga mandata una mail di conferma quando un utente prenota 
        un esame """

        utente_normale, esame = creazione_utenti_esame()
        esame.stato = 'prenotato'
        esame.paziente = utente_normale
        esame.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Notifica prenotazione esame")
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, [utente_normale.email])
        testo_mail = (f"Gentile utente, l'esame che si svolgera' in data {esame.data.strftime('%d-%m-%Y')}" 
                      f" alle ore {esame.data.strftime('%H:%M:%S')} e' stato prenotato")
        self.assertEqual(mail.outbox[0].body, testo_mail)

    def test_invio_mail_modifica(self):
        """ Testa che venga mandata una mail di notifica quando l'esame prenotato 
        da un utente subisce una modifica """

        utente_normale, esame = creazione_utenti_esame()
        esame.stato = 'prenotato'
        esame.paziente = utente_normale
        esame.save()
        vecchia_data = esame.data
        esame.data =  datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=1)
        esame.save()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, "Notifica modifica esame")
        self.assertEqual(mail.outbox[1].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[1].to, [utente_normale.email])
        testo_mail = (f"Gentile utente, l'esame prenotato per la data {vecchia_data.strftime('%d-%m-%Y')}" 
                                  f" alle ore {vecchia_data.strftime('%H:%M:%S')} e' stato modificato")
        self.assertEqual(mail.outbox[1].body, testo_mail)

    def test_invio_mail_cancellazione(self):
        """ Testa che venga mandata una mail di notifica quando l'esame prenotato 
        da un utente viene cancellato """

        utente_normale, esame = creazione_utenti_esame()
        esame.stato = 'prenotato'
        esame.paziente = utente_normale
        esame.save()
        esame.paziente = None
        esame.stato = 'cancellato'
        esame.save()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, "Notifica cancellazione esame")
        self.assertEqual(mail.outbox[1].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[1].to, [utente_normale.email])
        testo_mail = (f"Gentile utente, la cancellazione della prenotazione per l'esame che si svolgera' in data" 
                      f" {esame.data.strftime('%d-%m-%Y')} alle ore {esame.data.strftime('%H:%M:%S')} e' stata effettuata")
        self.assertEqual(mail.outbox[1].body, testo_mail)