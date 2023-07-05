from django.shortcuts import render
from xhtml2pdf import pisa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from gestione_medici.models import Esame
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import ListView
from django.utils.dateparse import parse_datetime
from zoneinfo import ZoneInfo
from datetime import datetime
from utenti_custom.models import *
from .forms import SearchEsamiForm

@login_required
def situazione_utente(request):
    """ Implementa la view per la situazione dell'utente utilizzando anche un 
    paginatore per i risultati"""

    user = get_object_or_404(UtenteCustom, pk=request.user.pk)
    esami = user.esami.all().order_by('-data')
    paginatore = Paginator(esami, 5)
    numero_pagina = request.GET.get("page")
    pagina = paginatore.get_page(numero_pagina)
    ctx = {'page_obj': pagina, 'title': 'Situazione visite'}
    return render(request,'gestione_utenti/situazione.html', ctx)

@login_required
def stampa_esame(request, pk):
    """ Implementa la view per la stampa di un esame """

    e = get_object_or_404(Esame, pk=pk)
    if e.stato == 'prenotato' or e.stato == 'eseguito':
        if e.paziente.pk != request.user.pk:
            messages.error("Non sei stato tu a prenotare questa visita!")
            redirect('gestione_utenti:situazione')
        else:
            template_path = 'gestione_utenti/stampa_esame.html'
            context = {'esame': e}
            # crea una risposta http e specifica il contenuto come pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="promemoria_{e.paziente.last_name}.pdf"'
            # trova e rendera il template che rappresentera' l'esame
            template = get_template(template_path)
            html = template.render(context)

            # crea pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # se trova un errore, riporta alla pagina con la situazione e mostra 
            # un messaggio
            if pisa_status.err:
                messages.error("Errore durante la creazione del pdf")
                redirect('gestione_utenti:situazione')
            return response
        
    messages.error("La visita non e' stampabile")
    redirect('gestione_utenti:situazione')

@login_required
def cancella_prenotazione(request, pk):
    """ Implementa la view per l'eliminazione di un esame """

    e = get_object_or_404(Esame, pk=pk)

    if e.paziente.pk != request.user.pk:
        messages.error("Non sei stato tu a prenotare questa visita!")
        return redirect(request,'gestione_utenti:situazione')
    
    # bisogna estrarre la data perche' altrimenti anche se venisse cancellato
    # lo stesso giorno, ritornerebbe disponibile
    if datetime.date(e.data) > datetime.date(datetime.now(tz=ZoneInfo("Europe/Rome"))):
        e.stato = 'disponibile'
        e.paziente = None
    else:
        e.stato = 'cancellato'
        e.paziente = None

    e.save()
    messages.success(request, "Cancellazione effettuata con successo")
    return redirect('gestione_utenti:situazione')

def ricerca_esami(request):
    """ Implementa la view per la ricerca degli esami, mostrando il form di ricerca 
    all'utente e poi chiamando redirenzionando l'utente alla view che mostra i 
    risultati """
    
    if request.method == "POST":
        form = SearchEsamiForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data.get('search_nome')
            cognome = form.cleaned_data.get('search_cognome')
            data_inizio = form.cleaned_data.get('search_data_inizio')
            data_fine = form.cleaned_data.get('search_data_fine')
            tipologia = form.cleaned_data.get('search_tipologia')
            return redirect('gestione_utenti:ricerca_esami_risultati', nome, 
                            cognome, data_inizio, data_fine, tipologia)
    else:
        form = SearchEsamiForm()
    return render(request,template_name='gestione_utenti/ricerca_esami.html', 
                  context={'form':form, 'title':'Ricerca esami'})

@login_required
def prenota_esame(request, pk):
    """ Implementa la view per prenotare un esame da parte di un utente registrato """

    e = get_object_or_404(Esame, pk=pk)

    if e.medico.utente == request.user:
        messages.error(request, "Non puoi prenotare un esame creato da te stesso")
        return redirect('gestione_utenti:ricerca_esami')
    
    e.stato = 'prenotato'
    e.paziente = request.user
    e.save()
    messages.success(request, "Prenotazione effettuata con successo")
    return redirect('gestione_utenti:ricerca_esami')

class EsameRicercaView(ListView):
    """ Implementa la view che mostra i risultati della ricerca degli esami all'utente, 
    per farlo filtra tutti gli esami disponibili e a partire dalla data odierna, usando 
    i parametri che gli vengono passati """

    title = "Risultati ricerca"
    model = Esame
    template_name = 'gestione_utenti/lista_esami.html'
    paginate_by = 5

    def get_queryset(self):
        data_odierna = datetime.now(tz=ZoneInfo("Europe/Rome"))
        risultati = self.model.objects.filter(stato__exact='disponibile', 
                                              data__gte=data_odierna)
        nome = self.request.resolver_match.kwargs['nome']
        cognome = self.request.resolver_match.kwargs['cognome']
        data_inizio = self.request.resolver_match.kwargs['data_inizio']
        data_fine = self.request.resolver_match.kwargs['data_fine']
        tipologia = self.request.resolver_match.kwargs['tipologia']

        if nome:
            risultati = risultati.filter(medico__utente__first_name__icontains=nome)
        if cognome:
            risultati = risultati.filter(medico__utente__last_name__icontains=cognome)
        if data_inizio != 'None':
            data_oggetto = parse_datetime(data_inizio)
            risultati = risultati.filter(data__gte=data_oggetto)
        if data_fine != 'None':
            data_oggetto = parse_datetime(data_fine)
            risultati = risultati.filter(data__lte=data_oggetto)
        if tipologia:
            risultati = risultati.filter(tipologia__exact=tipologia)
        
        return risultati