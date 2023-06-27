from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import locale
from utenti_custom.models import UtenteCustom
from gestione_medici.models import Medico, Esame
from .views import EsameRicercaView

def crea_utenti_medico():
    """ Funzione che crea due utenti di prova e un medico (usando un terzo utente
      di prova)"""
    utente_prova1 = UtenteCustom.objects.create_user(email='prova1@gmail.com', password='prova1', 
                                                     first_name='utente1', last_name='di prova 1')
    utente_prova2 = UtenteCustom.objects.create_user(email='prova2@gmail.com', password='prova2', 
                                                     first_name='utente2', last_name='di prova 2')
    utente_medico = UtenteCustom.objects.create_user(email='prova3@gmail.com', password='prova3', 
                                                     first_name='utente3', last_name='medico')
    medico = Medico.objects.create(utente=utente_medico)
    return (utente_prova1, utente_prova2, medico)

class SituazioneUtenteViewTest(TestCase):

    def test_situazione_utente_non_loggato(self):
        """Test che controlla se il sito redirezioni verso la pagina di login nel
          caso l'utente non abbia fatto l'accesso con ilsuo account e cerchi di 
          accedere alla situazione dei suoi esami"""
        
        client = Client()
        response = client.get(reverse('gestione_utenti:situazione'))
        self.assertRedirects(response, reverse('utenti_custom:login') + 
                             '?auth=notok&next=/gestione_utenti/situazione/')

    def test_situazione_utente_con_esami_altrui(self):
        """Test che verifica che quando sono presenti anche esami di altri utenti 
        nel database, la pagina personale mostri solo i propri esami"""

        utente_prova1, utente_prova2, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_corretto = Esame.objects.create(tipologia='urine', medico=medico, data=data, 
                                              stato='prenotato', paziente=utente_prova1)
        Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, 
                             stato='prenotato', paziente=utente_prova2)
        
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:situazione'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])



class RicercaEsamiViewTest(TestCase):  

    def test_ricerca_esami_tutti(self):
        """Test che verifica che quando non sono specificati parametri, vengano 
        restituiti tutti gli esami"""
        utente_prova1, utente_prova2, medico_1 = crea_utenti_medico()
        data_1 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_1 = Esame.objects.create(tipologia='ematochimica', medico=medico_1, 
                                              data=data_1, stato='disponibile')
        data_2 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=1)
        medico_2 = Medico.objects.create(utente=utente_prova2)
        esame_2 = Esame.objects.create(tipologia='radiologia', medico=medico_2,
                              data=data_2, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_1, esame_2])

    def test_ricerca_esami_nome(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando il 
        nome del medico"""
        utente_prova1, utente_prova2, medico_corretto = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_corretto = Esame.objects.create(tipologia='ematochimica', medico=medico_corretto, 
                                              data=data, stato='disponibile')
        medico_sbagliato = Medico.objects.create(utente=utente_prova2)
        Esame.objects.create(tipologia='ematochimica', medico=medico_sbagliato,
                              data=data, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        nome_medico = medico_corretto.utente.first_name
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':nome_medico, 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])
    
    def test_ricerca_esami_cognome(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando il 
        cognome del medico"""
        utente_prova1, utente_prova2, medico_corretto = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_corretto = Esame.objects.create(tipologia='ematochimica', medico=medico_corretto, 
                                              data=data, stato='disponibile')
        medico_sbagliato = Medico.objects.create(utente=utente_prova2)
        Esame.objects.create(tipologia='ematochimica', medico=medico_sbagliato,
                              data=data, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        cognome_medico = medico_corretto.utente.last_name
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':cognome_medico, 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])

    def test_ricerca_esami_data_inizio(self):
        """Test che verifica la funzionalita' di ricerca degli esami a partire 
        da una certa data"""
        utente_prova1, _, medico = crea_utenti_medico()
        data_1 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        data_2 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=2)
        data_3 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=4)
        data_4 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=5)
        Esame.objects.create(tipologia='ematochimica', medico=medico, 
                             data=data_1, stato='disponibile')
        Esame.objects.create(tipologia='ematochimica', medico=medico,
                              data=data_2, stato='disponibile')
        esame_corretto_1 = Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_3, stato='disponibile')
        esame_corretto_2 = Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_4, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':'', 
                                              'data_inizio':data_3, 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto_1, 
                                                                esame_corretto_2])

    def test_ricerca_esami_data_fine(self):
        """Test che verifica la funzionalita' di ricerca degli esami non oltre 
        una certa data"""
        utente_prova1, _, medico = crea_utenti_medico()
        data_1 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        data_2 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=2)
        data_3 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=4)
        data_4 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=5)
        esame_corretto_1 = Esame.objects.create(tipologia='ematochimica', medico=medico, 
                             data=data_1, stato='disponibile')
        esame_corretto_2 = Esame.objects.create(tipologia='ematochimica', medico=medico,
                              data=data_2, stato='disponibile')
        Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_3, stato='disponibile')
        Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_4, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':data_2}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto_1, 
                                                                esame_corretto_2])

    def test_ricerca_esami_tra_due_date(self):
        """Test che verifica la funzionalita' di ricerca degli esami tra due date"""
        utente_prova1, _, medico = crea_utenti_medico()
        data_1 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        data_2 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=2)
        data_3 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=4)
        data_4 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=5)
        data_5 = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(weeks=3)
        Esame.objects.create(tipologia='ematochimica', medico=medico, 
                             data=data_1, stato='disponibile')
        Esame.objects.create(tipologia='ematochimica', medico=medico,
                              data=data_2, stato='disponibile')
        esame_corretto = Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_3, stato='disponibile')
        Esame.objects.create(tipologia='ematochimica', medico=medico,
                                              data=data_4, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':'', 
                                              'data_inizio':data_5, 'data_fine':data_3}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])

    def test_ricerca_esami_tipologia(self):
        """Test che verifica la funzionalita' di ricerca degli esami usando la 
        tipologia dell'esame"""
        utente_prova1, _, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame_corretto = Esame.objects.create(tipologia='ematochimica', medico=medico, 
                             data=data, stato='disponibile')
        Esame.objects.create(tipologia='radiografia', medico=medico,
                              data=data, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'ematochimica', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])

    def test_ricerca_esami_con_esami_non_disponibili(self):
        """Test che verifica che gli esami mostrati durante una ricerca siano 
        solo quelli disponibili e non anche quelli prenotati, eseguiti o cancellati"""

        utente_prova1, utente_prova2, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, 
                             stato='prenotato', paziente=utente_prova2)
        Esame.objects.create(tipologia='oculistica', medico=medico, data=data, 
                             stato='cancellato')
        Esame.objects.create(tipologia='ecografia', medico=medico, data=data, 
                             stato='eseguito', paziente=utente_prova2)
        esame_corretto = Esame.objects.create(tipologia='urologia', medico=medico, 
                                              data=data, stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.post(reverse('gestione_utenti:ricerca_esami'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame_corretto])

    def test_ricerca_esami_numero_di_esami_pagina(self):
        """Test che verifica che venga mostrato il numero corretto di esami in 
        una pagina"""

        utente_prova1, _, medico = crea_utenti_medico()
        num_pagine = EsameRicercaView.paginate_by
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esami = [Esame.objects.create(tipologia='ematochimica', medico=medico, 
                                      data=data, stato='disponibile') for i in range(num_pagine + 2)]
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'ematochimica', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}) + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], esami[:num_pagine])
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'ematochimica', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], esami[num_pagine:])

    def test_ricerca_esami_non_presenti(self):
        utente_prova1, _, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, 
                             stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'sbagliato', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [])
        self.assertContains(response, "Non sono stati trovati esami")

    def test_contenuto_esame_corretto(self):
        utente_prova1, _, medico = crea_utenti_medico()
        data = datetime.now(tz=ZoneInfo("Europe/Rome")) + timedelta(days=1)
        esame = Esame.objects.create(tipologia='ematochimica', medico=medico, data=data, 
                             stato='disponibile')
        client = Client()
        client.force_login(user=utente_prova1)
        response = client.get(reverse('gestione_utenti:ricerca_esami_risultati', 
                                      kwargs={'tipologia':'', 'nome':'', 'cognome':'', 
                                              'data_inizio':'None', 'data_fine':'None'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_obj'], [esame])
        self.assertContains(response, esame.tipologia)
        self.assertContains(response, esame.medico.__str__())
        self.assertContains(response, esame.stato)
        locale.setlocale(locale.LC_TIME, 'it_IT') 
        giorno = esame.data.strftime('%A').capitalize()
        mese = esame.data.strftime('%B').capitalize()
        data = f"{giorno} {esame.data.strftime('%d')} {mese} {esame.data.strftime('%Y %H:%M')}"
        self.assertContains(response, data)
        self.assertContains(response, 'Prenotalo')