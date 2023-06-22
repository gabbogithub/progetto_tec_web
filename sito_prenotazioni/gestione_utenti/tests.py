from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from utenti_custom.models import UtenteCustom
from gestione_medici.models import Medico, Esame

def crea_utenti_medico():
    utente_prova1 = UtenteCustom.objects.create_user(email='prova@gmail.com', password='prova', first_name='utente', 
                                                     last_name='di prova 1')
    utente_prova2 = UtenteCustom.objects.create_user(email='prova2@gmail.com', password='prova2', first_name='utente', 
                                                     last_name='di prova 2')
    utente_medico = UtenteCustom.objects.create_user(email='prova3@gmail.com', password='prova3', first_name='utente', 
                                                     last_name='medico')
    medico = Medico.objects.create(utente=utente_medico)
    return (utente_prova1, utente_prova2, medico)

class SituazioneUtenteViewTest(TestCase):

    def test_situazione_utente_non_loggato(self):
        """Test che controlla se il sito redirezioni verso la pagina di login nel caso l'utente non abbia fatto l'accesso con il
            suo account e cerchi di accedere alla situazione dei suoi esami"""
        client = Client()
        response = client.get(reverse('gestione_utenti:situazione'))
        self.assertRedirects(response, reverse('utenti_custom:login') + '?auth=notok&next=/gestione_utenti/situazione/')

    def test_situazione_utente_con_esami_altrui(self):
        """Test che verifica che quando sono presenti anche esami di altri utenti nel database, la pagina personale mostri
        solo i propri esami"""
        utente_prova1, utente_prova2, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_corretto = Esame.objects.create(tipologia='urine', medico=medico, data=data, stato='prenotato', 
                                              paziente=utente_prova1)
        Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, stato='prenotato', paziente=utente_prova2)
        
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:situazione'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])



class RicercaEsamiViewTest(TestCase):  

    def test_ricerca_esami_con_esami_non_disponibili(self):
        """Test che verifica che gli esami mostrati durante una ricerca siano solo quelli disponibili e non anche quelli
        prenotati, eseguiti o cancellati"""
        utente_prova1, utente_prova2, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, stato='prenotato', paziente=utente_prova2)
        Esame.objects.create(tipologia='oculistica', medico=medico, data=data, stato='cancellato')
        Esame.objects.create(tipologia='ecografia', medico=medico, data=data, stato='eseguito', paziente=utente_prova2)
        esame_corretto = Esame.objects.create(tipologia='urologia', medico=medico, data=data, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.post(reverse('gestione_utenti:ricerca_esami'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])
        
    
    def test_ricerca_esami_prenotazione_utente_non_loggato(self):
        """Test che verifica che gli esami possano essere prenotati solo dagli utenti registrati"""
        pass

    def test_ricerca_esami_redirezione_pagina_medico(self):
        """Test che verifica che il nome del medico degli esami trovati sia cliccabile e porti alla pagina con la sua 
        presentazione"""
        pass

    def test_ricerca_esami_numero_di_esami_pagina(self):
        """Test che verifica che il venga mostrato il numero corretto di esami in una pagina"""

    def test_ricerca_esami_nome(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando il nome del medico"""
        pass
    
    def test_ricerca_esami_cognome(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando il cognome del medico"""
        pass

    def test_ricerca_esami_data_inizio(self):
        """Test che verifica la funzionalita' di ricerca degli esami a partire da una certa data"""
        pass

    def test_ricerca_esami_data_fine(self):
        """Test che verifica la funzionalita' di ricerca degli esami non oltre una certa data"""
        pass

    def test_ricerca_esami_tra_due_date(self):
        """Test che verifica la funzionalita' di ricerca degli esami tra due date"""
        pass

    def test_ricerca_esami_tipologia(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando la tipologia dell'esame"""
        pass

    def test_ricerca_esami_tutti(self):
        """Test che verifica che quando non sono specificati parametri, vengano restituiti tutti gli esami"""
        pass