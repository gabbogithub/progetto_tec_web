from django.shortcuts import render
from xhtml2pdf import pisa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from gestione_medici.models import Esame
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from zoneinfo import ZoneInfo
from datetime import datetime
from utenti_custom.models import *

# Create your views here.
@login_required
def situazione_utente(request):
    user = get_object_or_404(UtenteCustom, pk=request.user.pk)
    esami = user.esami.all()
    paginatore = Paginator(esami, 1)
    numero_pagina = request.GET.get("page")
    pagina = paginatore.get_page(numero_pagina)
    ctx = {'page_obj': pagina}
    return render(request,"gestione_utenti/situazione.html",ctx)

@login_required
def stampa_esame(request, pk):
    e = get_object_or_404(Esame, pk=pk)
    if e.stato == 'prenotato' or e.stato == 'eseguito':

        if e.paziente.pk != request.user.pk:
            messages.error("Non sei stato tu a prenotare questa visita!")
            redirect('gestione_utenti:situazione')

        else:
            template_path = 'gestione_utenti/stampa_esame.html'
            context = {'esame': e}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="promemoria_{e.paziente.last_name}.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                messages.error("Errore durante la creazione del pdf")
                redirect('gestione_utenti:situazione')
            return response
        
    messages.error("La visita non e' stampabile")
    redirect('gestione_utenti:situazione')

def cancella_prenotazione(request, pk):
    e = get_object_or_404(Esame, pk=pk)

    if e.paziente.pk != request.user.pk:
        messages.error("Non sei stato tu a prenotare questa visita!")
        return redirect(request,'gestione_utenti:situazione')
    
    if e.data > datetime.now(tz=ZoneInfo("Europe/Rome")):
        e.stato = 'disponibile'
        e.paziente = None
    else:
        e.stato = 'cancellato'
        e.paziente = None
    e.save()
    messages.success(request, "Cancellazione effettuata con successo")
    return redirect('gestione_utenti:situazione')
    