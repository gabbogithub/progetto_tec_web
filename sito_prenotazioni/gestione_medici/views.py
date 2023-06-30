from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from .forms import *

def ha_gruppo_medico(user):
    """ Verifica che l'utente passato come argomento faccia parte del gruppo 
    'Medici' """

    return user.groups.filter(name='Medici').exists()

def filtra_esami(form, esami):
    """ Data un form e gli esami totali, ritorna gli esami filtrati in base ai 
    valori dei campi del form """

    categoria = form.cleaned_data.get('search_categoria')
    
    if categoria == 'stato':
        stato = form.cleaned_data.get('search_stato')
        esami = esami.filter(stato__exact=stato)

    elif categoria == 'data':
        inizio = form.cleaned_data.get('search_data_inizio')
        fine = form.cleaned_data.get('search_data_fine')
        if inizio:
            esami = esami.filter(data__gte=inizio)
        if fine:
            esami = esami.filter(data__lte=fine)
    
    return esami

@user_passes_test(ha_gruppo_medico)
def esami_caricati(request):
    """ Implementa la view per la visualizzazione degli esami caricati da un 
    medico, gestendo anche un paginatore e un sistema di filtraggio degli esami """

    user = get_object_or_404(UtenteCustom, pk=request.user.pk)
    parametri_ricerca = ['search_categoria', 'search_stato', 'search_data_inizio', 
                         'search_data_fine']
    parametri_separati = {f"&{key}={value}" for key, value in request.GET.items() 
                          if key in parametri_ricerca}
    parametri_uniti = ''.join(parametri_separati)
    medico = user.medico
    esami = medico.esami_caricati.all().order_by('-data')
    risultati = FiltraEsameForm(request.GET)
    if risultati.is_valid():
        esami = filtra_esami(risultati, esami)
    paginatore = Paginator(esami, 5)
    numero_pagina = request.GET.get("page")
    pagina = paginatore.get_page(numero_pagina)
    form = FiltraEsameForm()
    ctx = {'page_obj':pagina, 'form':form, 'stringa_ricerca': parametri_uniti, 
           'title': 'Esami caricati'}
    return render(request,"gestione_medici/esami_caricati.html",ctx)

class CreaEsameView(SuccessMessageMixin, GroupRequiredMixin, CreateView):
    """ Implementa la view per la creazione di un nuovo esame da parte di un 
    medico """

    group_required = ['Medici']
    title = "Crea esame"
    form_class = CreaEsameForm
    template_name = 'gestione_medici/crea_esame.html'
    success_url = reverse_lazy('gestione_medici:crea_esame')
    success_message = "L'esame e' stato creato con successo"

    def form_valid(self, form):
        """ Override del metodo per aggiungere automaticamente il medico e lo 
        stato giusti """

        form.instance.medico = self.request.user.medico
        form.instance.stato = 'disponibile'
        return super().form_valid(form)

class ModificaEsameView(SuccessMessageMixin, GroupRequiredMixin, UpdateView):
    """ Implementa la view per la modifica di un esame da parte del medico che 
    l'ha caricato """    

    group_required = ['Medici']
    title = "Modifica esame"
    model = Esame
    form_class = ModificaEsameForm
    template_name = "gestione_medici/modifica_esame.html"
    success_url = reverse_lazy('gestione_medici:esami_caricati')
    success_message = "L'esame e' stato modificato con successo"

class ModificaInformazioniView(SuccessMessageMixin, GroupRequiredMixin, UpdateView):
    """ Implementa la view per la modifica delle informazioni di un medico """ 

    group_required = ['Medici']
    title = "Modifica profilo medico"
    model = Medico
    fields = ['descrizione']
    template_name = "gestione_medici/modifica_informazioni.html"
    success_message = "Le informazioni del tuo profilo medico sono state modificate con successo"

    def get_success_url(self):
        """ Ritorna lo url della pagina di modifica delle informazioni passandogli 
        la chiave del medico come argomento """

        return reverse_lazy('gestione_medici:modifica_informazioni', kwargs={'pk': self.kwargs['pk']})
    
class InformazioniMedicoView(DetailView):
    """ Implementa la view con le informazioni di un medico, i tre commenti piu' 
    recenti e da' la possibilita' di lasciarne uno """ 

    title = "Informazioni sul medico"
    model = Medico
    template_name = "gestione_medici/presentazione.html"

    def get_context_data(self, **kwargs):
        """ Override del metodo per recuperare oltre alle normali variabili di 
        contesto, anche i tre commenti piu' recenti """

        context = super().get_context_data(**kwargs)
        commenti_totali = context['medico'].commenti.all()
        context['commenti'] = commenti_totali[:3]
        return context

class CommentiMedicoView(ListView):
    """ Implementa la view per vedere tutti i commenti riguardo un certo medico 
    con paginazione"""

    title = "Commenti sul medico"
    model = Commento
    template_name = "gestione_medici/commenti_totali.html"
    paginate_by = 5

    def get_queryset(self):
        """ Filtra i commenti totali per ottenere solo quelli che riguardano il 
        medico indicato chiave nell'url """

        return self.model.objects.filter(medico=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        """ Aggiunta del medico indicato dalla chiave nell'url alle variabili 
        di contesto"""

        self.context = super().get_context_data(**kwargs)
        self.context['medico'] = Medico.objects.get(pk=self.kwargs['pk'])
        return self.context
    
class CreaCommentoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """ Implementa la view per creare un commento riguardo un certo medico """

    title = "Crea un commento"
    model = Commento
    form_class = CreaCommentoForm
    template_name = 'gestione_medici/crea_commento.html'
    success_message = "Il commento e' stato creato con successo"

    def form_valid(self, form):
        """ Aggiunta automatica dei parametri commentatore e medico sulla base 
        di chi richiede la pagina e degli argomenti passati all'url """

        form.instance.commentatore = self.request.user
        form.instance.medico = Medico.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        """ Override del metodo 'post' per aggiungere un messaggio di errore e 
        una redirezione alla pagina di informazioni del medico, nel caso l'utente 
        che prova ad inserire il commento ne avesse gia' fatto uno """

        try:
            super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "Hai gia' commentato questo medico")

        return HttpResponseRedirect(reverse_lazy('gestione_medici:informazioni_medico', kwargs={'pk': self.kwargs['pk']}))
    
    def get_success_url(self):
        """ Url della pagina di informazioni del medico a cui viene passato la 
        chiave del medico presente nell'url """

        return reverse_lazy('gestione_medici:informazioni_medico', kwargs={'pk': self.kwargs['pk']})