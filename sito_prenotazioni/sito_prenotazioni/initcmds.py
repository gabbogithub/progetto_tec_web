from django.contrib.auth.models import Group, Permission
import random
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
import shutil
from gestione_assistenza.models import *
from gestione_medici.models import *
from utenti_custom.models import *

def crea_gruppi():
    """ Controlla che esistano i gruppi 'Medici' e 'Assistenza' e nel caso non 
    li trovi, li crea"""

    try:
        Group.objects.get(name='Medici')
    except Group.DoesNotExist:
        nuovo_gruppo = Group.objects.create(name='Medici')
        lista_permessi = ('view_esame', 'add_esame', 'change_esame', 'view_medico', 
                          'change_medico')
        permessi = Permission.objects.filter(codename__in=lista_permessi)
        nuovo_gruppo.permissions.set(permessi)
        nuovo_gruppo.save()
    
    try:
        Group.objects.get(name='Assistenza')
    except Group.DoesNotExist:
        nuovo_gruppo = Group.objects.create(name='Assistenza')
        lista_permessi = ('add_utentecustom', 'change_utentecustom', 'view_utentecustom', 
                          'add_esame', 'change_esame', 'view_esame', 'add_medico', 
                          'change_medico', 'view_medico', 'add_commento', 'change_commento',
                          'delete_commento', 'view_commento')
        permessi = Permission.objects.filter(codename__in=lista_permessi)
        nuovo_gruppo.permissions.set(permessi)
        nuovo_gruppo.save()

def crea_db():
    """ Crea una serie di utenti, medici, esami, chat e poi tre utenti per categoria 
    con caratteristiche predefinite"""

    path_nomi = 'sito_prenotazioni/file_init/nomi.txt'
    path_cognomi = 'sito_prenotazioni/file_init/cognomi.txt'
    n_utenti = 20
    n_medici = 15
    n_chat = 20
    n_esami = 10 # numero esami per ogni medico, non totali
    utenti = []

    with (
        open(path_nomi, 'r', encoding='utf-8') as nomi,  
        open(path_cognomi, 'r', encoding='utf-8') as cognomi
    ):
        nomi = nomi.read().splitlines()
        cognomi = cognomi.read().splitlines()

        # creazione utenti
        for _ in range(n_utenti):
            nome = random.choice(nomi)
            cognome = random.choice(cognomi)
            email = nome + cognome + "@gmail.com"
            password = nome + cognome
            utente = UtenteCustom.objects.create_user(email=email, password=password, 
                                                      first_name=nome, last_name=cognome)
            utenti.append(utente)
        
    utenti_medici = random.sample(utenti, n_medici) 
    medici = []

    # creazione medici
    for num, utente in enumerate(utenti_medici, start=1):
        medico = Medico.objects.create(utente=utente)
        medici.append(medico)
        # creazione esami associati ad ogni medico
        for i in range(n_esami):
            tipologia = random.choice(Esame.TIPOLOGIE_POSSIBILI)[0]
            data = (datetime.now(tz=ZoneInfo("Europe/Rome")) + 
                    timedelta(days=num*i) + 
                    timedelta(minutes=num*i))
            stato = 'disponibile'
            Esame.objects.create(tipologia=tipologia, medico=medico, data=data, 
                                 stato=stato)

    # creazione chat
    for _ in range(n_chat):
        stato = 'in_attesa'
        nome = random.choice(nomi)
        cognome = random.choice(cognomi)
        Chat.objects.create(stato=stato, identificativi_utente=nome+cognome)

    # creazione utente di prova dell'assistenza
    nome_assistenza = 'assistenza'
    cognome_assistenza = 'clienti'
    password_assistenza = 'assistenzaclienti'
    email_assistenza = 'assistenzaclienti@gmail.com'
    path_foto_assistenza = 'sito_prenotazioni/file_init/immagine_assistenza.jpg'
    assistenza = UtenteCustom.objects.create_user(email=email_assistenza, 
                                                  password=password_assistenza, 
                                                  first_name=nome_assistenza, 
                                                  last_name=cognome_assistenza,
                                                  is_staff=True)
    gruppo_assistenza = Group.objects.get(name='Assistenza')
    gruppo_assistenza.user_set.add(assistenza)
    with open(path_foto_assistenza, 'rb') as foto:
        data = foto.read()
        assistenza.foto_profilo.save('immagine_assistenza.jpg',  ContentFile(data), 
                                        save=True)
 
    # creazione dell'admin
    nome_admin = 'admin'
    cognome_admin = 'superutente'
    password_admin = 'admin'
    email_admin = 'admin@gmail.com'
    UtenteCustom.objects.create_superuser(email=email_admin, password=password_admin,
                                           first_name=nome_admin, last_name=cognome_admin)

    # creazione utente di prova
    nome_utente = 'mario'
    cognome_utente = 'rossi'
    password_utente = 'mariorossi'
    email_utente = 'mariorossi@gmail.com'
    path_foto_utente = 'sito_prenotazioni/file_init/immagine_utente.jpg'
    utente = UtenteCustom.objects.create_user(email=email_utente, password=password_utente, 
                                              first_name=nome_utente, last_name=cognome_utente)
    with open(path_foto_utente, 'rb') as foto:
        data = foto.read()
        utente.foto_profilo.save('immagine_utente.jpg',  ContentFile(data), 
                                        save=True)

    # creazioni esami per l'utente di prova
    for i in range(n_esami):
        tipologia = random.choice(Esame.TIPOLOGIE_POSSIBILI)[0]
        differenza_data = random.randint(-10, 10)
        data = (datetime.now(tz=ZoneInfo("Europe/Rome")) + 
                timedelta(weeks=differenza_data) +
                timedelta(minutes=differenza_data)
                )
        stato = 'prenotato'
        if differenza_data < 0:
            stato = random.choice(('eseguito', 'cancellato')) 
        medico = random.choice(medici)
        Esame.objects.create(tipologia=tipologia, medico=medico, data=data, 
                             stato=stato, paziente=utente)
        
    # creazione utente medico di prova
    nome_medico = 'luigi'
    cognome_medico = 'bianchi'
    password_medico = 'luigibianchi'
    email_medico = 'luigibianchi@gmail.com'
    path_foto_medico = 'sito_prenotazioni/file_init/immagine_medico.jpg'
    utente_medico = UtenteCustom.objects.create_user(email=email_medico, password=password_medico, 
                                              first_name=nome_medico, last_name=cognome_medico)
    
    with open(path_foto_medico, 'rb') as foto:
        data = foto.read()
        utente_medico.foto_profilo.save('immagine_medico.jpg',  ContentFile(data), 
                                        save=True)

    descrizione_medico = ("Sono un medico laureato nel 2010 all'universita' di " 
                          "Modena e Reggio Emilia. Il mio punto di forza è il " 
                          "rapporto con i pazienti che cerco di curare nei minimi " 
                          "dettagli.")
    
    medico = Medico.objects.create(utente=utente_medico, descrizione=descrizione_medico)
    
    # creazione esami disponibili per la ricerca del medico di prova
    for i in range(n_esami):
            tipologia = random.choice(Esame.TIPOLOGIE_POSSIBILI)[0]
            differenza_data = random.randint(1, 10)
            data = (datetime.now(tz=ZoneInfo("Europe/Rome")) + 
                    timedelta(weeks=differenza_data) + 
                    timedelta(minutes=differenza_data))
            stato = 'disponibile'
            Esame.objects.create(tipologia=tipologia, medico=medico, data=data, 
                                 stato=stato)
    
    # creazione esami prenotati, eseguiti e cancellati dal medico di prova
    for i in range(n_esami):
        tipologia = random.choice(Esame.TIPOLOGIE_POSSIBILI)[0]
        paziente = random.choice(utenti)
        stato = 'prenotato'
        differenza_data = random.randint(-10, 10)
        data = (datetime.now(tz=ZoneInfo("Europe/Rome")) + 
                timedelta(weeks=differenza_data) + 
                timedelta(minutes=differenza_data))
        if differenza_data < 0:
            stato = random.choice(('eseguito', 'cancellato'))
        Esame.objects.create(tipologia=tipologia, medico=medico, data=data, 
                                stato=stato, paziente=paziente)
        
    # creazione commenti relativi al medico di prova
    with open('sito_prenotazioni/file_init/commenti.txt', 'r') as commenti:
        for num, line in enumerate(commenti):
            Commento.objects.create(medico=medico, commentatore=utenti[num], 
                                    testo=line)

def elimina_db():
    """ Elimina tutte le istanze dei modelli che sono presenti nel database e 
    la cartella con le immagini """

    Chat.objects.all().delete()
    Commento.objects.all().delete()
    Esame.objects.all().delete()
    Medico.objects.all().delete()
    UtenteCustom.objects.all().delete()
    shutil.rmtree('media/immagini_utenti')

def setup_sistema():
    """ Funzione di setup che richiama la funzione per la creazione dei gruppi e 
    nel caso l'utente voglia creare un nuovo database, chiama le funzioni 
    necessarie a eliminare quello esistente e a crearne uno nuovo"""

    crea_gruppi()
    scelta = input("Vuoi eliminare il database esistente e crearne uno nuovo? ")
    if scelta in ('si', 'sì', 'Si', 'Sì', 'SI'):
        elimina_db()
        print("\nEliminazione database completata\n")
        crea_db()
        print("\nCreazione database completata\n")
    else:
        print("\nIl database esistente è stato mantenuto\n")