LIBRERIE NECESSARIE:

Per poter utilizzare il progetto sono necessari una serie di pacchetti che indichero' di
seguito ma nella cartella e' presente anche un pipfile che puo' agevolare l'operazione.
Le versioni di molti pacchetti sono parecchio recenti perche' hanno subito aggiornamenti
mentre sviluppavo il progetto o poco prima della consegna del progetto ma non vi 
preoccupate perche' ho testato che tutto funzionasse anche con le librerie piu' recenti.

-python: io ho usato la versione 3.11.3 ma dovrebbe funzionare anche con versioni meno
recenti anche se ho utilizzato in un file una sintassi disponibile solo da python 3.10;
-django: versione 4.2.3 ma anche questo dovrebbe funzionare con versioni meno recenti;
-pillow: 10.0.0;
-crispy-bootstrap5: versione 0.7;
-django-bootstrap-datepicker-plus = 5.0.4;
-xhtml2pdf = 0.2.11;
-django-dirtyfields = 1.9.2;
-django-channels = 4.0.0;
-daphne = 4.0.0;
-django-braces = 1.15.0;

COME AVVIARE IL SITO:
Per avviare il progetto bisogna posizionarsi nella cartella sito_prenotazioni, dare il
comando "python manage.py runserver" e seguire il link locale. Ogni volta che avviate
il sito vi verra' chiesto se volete creare un nuovo database. L'operazione non è 
necessaria in quanto vi fornisco insieme ai file del sito un database già riempito ma 
nel caso voleste ricrearlo con nuovi dati vi bastera' immettere 'si' da riga di comando.
Vi avverto che la procedura non è velocissima e potrebbe durare un paio minuto. 
Consiglio inoltre di tenere d'occhio la console mentre testate il sito per notare quando
vengono inviate le mail per esempio quando si prenota un esame. Infine ricordo che se si
vuole testare la chat in tempo reale è necessario aprire due schede separate e in almeno
una bisogna accedere con un account dell'assistenza clienti.

DATI DI PROVA:
Il sito è stato riempito con dati di prova per testare le varie funzionalità.
Sfortunamente per come ho implementato la chat (dove quando si esce, la chat viene 
chiusa), non sono presenti chat di prova già pronte per essere testate ma dovrete farlo 
voi con due utenti diversi. Ho lo stesso inserito delle chat di prove fittizie per farvi 
vedere che aspetto avrebbe il sito se ci fossero un po' di utenti in attesa. Le chat 
sono in ordine cronologico quindi se ne create una, dovete andare all'ultima pagina per 
vederla. Di seguito trovate email e password per accedere al sito come ognuno delle 
categorie di utenti possibili:

-utente normale: mariorossi@gmail.com | mariorossi
-utente medico: luigibianchi@gmail.com | luigibianchi
-utente assistenza: assistenzaclienti@gmail.com | assistenzaclienti
-admin: admin@gmail.com | admin

I commenti e la presentazione sono stati inseriti solo per il medico 'luigi bianchi' 
quindi se volete vedere una pagina di presentazione realistica, dovete cercare un esame 
di luigi bianchi e poi cliccare sull'hyperlink verso la sua pagina di presentazione.
Gli utenti di prova che vi ho riportato prima sono quelli più completi ma tutti gli
utenti che ho generato seguono lo schema 'nomecognome@gmail.com nomecognome' quindi se
lo desiderate potete accedere anche come gli altri utenti che vedete nel sito.