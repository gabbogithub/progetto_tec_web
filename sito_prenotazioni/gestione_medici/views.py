from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

def ricerca_esami(request):
    if request.method == "POST":
        form = SearchEsamiForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data.get('search_nome')
            cognome = form.cleaned_data.get('search_cognome')
            data_inizio = form.cleaned_data.get('search_data_inizio')
            data_fine = form.cleaned_data.get('search_data_fine')
            categoria = form.cleaned_data.get('search_categoria')
            return redirect('gestione_medici:ricerca_esami_risultati', nome, cognome, data_inizio, data_fine, categoria)
    else:
        form = SearchEsamiForm()
    return render(request,template_name="gestione_medici/ricerca_esami.html", context={"form":form})

@login_required
def esami_caricati(request):
    user = get_object_or_404(UtenteCustom, pk=request.user.pk)
    medico = user.medico
    esami = medico.esami_caricati.all()
    paginatore = Paginator(esami, 1)
    numero_pagina = request.GET.get("page")
    pagina = paginatore.get_page(numero_pagina)
    ctx = {'page_obj': pagina}
    return render(request,"gestione_medici/esami_caricati.html",ctx)

class CreateEsameView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    #group_required = ["Medici"]
    title = "Aggiungi un esame tra quelli caricati"
    form_class = CreateEsameForm
    template_name = 'gestione_medici/crea_esame.html'
    success_url = reverse_lazy('gestione_medici:crea_esame')
    success_message = "L'esame e' stato creato con successo"

    def form_valid(self, form):
        form.instance.medico = self.request.user.medico
        form.instance.stato = 'disponibile'
        return super().form_valid(form)

class ModificaEsameView(SuccessMessageMixin, UpdateView):
    title = "Modifica l'esame"
    model = Esame
    form_class = ModificaEsameForm
    template_name = "gestione_medici/modifica_esame.html"
    success_url = reverse_lazy('gestione_medici:esami_caricati')
    success_message = "L'esame e' stato modificato con successo"

class ModificaInformazioniView(SuccessMessageMixin, UpdateView):
    title = "Modifica informazioni sul tuo profilo medico"
    model = Medico
    fields = ['descrizione']
    template_name = "gestione_medici/modifica_informazioni.html"
    success_message = "Le informazioni del tuo profilo medico sono state modificate con successo"

    def get_success_url(self):
        return reverse_lazy('gestione_medici:modifica_informazioni', kwargs={'pk': self.kwargs['pk']})
    
class InformazioniMedicoView(DetailView):
    title = "Pagina di informazioni sul medico"
    model = Medico
    template_name = "gestione_medici/presentazione.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commenti'] = context['medico'].commenti.all()
        return context


class EsameRicercaView(ListView):
    titolo = "La tua ricerca ha dato come risultato"
    model = Esame
    template_name = 'gestione_medici/lista_esami.html'
    paginate_by = 2

    def get_queryset(self):
        risultati = self.model.objects.filter(stato__exact='disponibile')
        nome = self.request.resolver_match.kwargs['nome']
        cognome = self.request.resolver_match.kwargs['cognome']
        data_inizio = self.request.resolver_match.kwargs['data_inizio']
        data_fine = self.request.resolver_match.kwargs['data_fine']
        tipologia = self.request.resolver_match.kwargs['tipologia']
        print(type(nome), cognome, type(data_inizio), type(data_fine), tipologia)

        if nome:
            print("Arrivato a")
            risultati = risultati.filter(medico__utente__first_name__icontains=nome)
        if cognome:
            print("Arrivato b")
            risultati = risultati.filter(medico__utente__last_name__icontains=cognome)
        if data_inizio != "None":
            print("Arrivato c")
            data_oggetto = parse_datetime(data_inizio)
            risultati = risultati.filter(data__gte=data_oggetto)
        if data_fine != "None":
            print("Arrivato d")
            data_oggetto = parse_datetime(data_fine)
            risultati = risultati.filter(data__lte=data_oggetto)
        if tipologia:
            print("Arrivato e ")
            risultati = risultati.filter(tipologia__exact=tipologia)
        
        return risultati
        
'''
class EsameRicercaView(ListView):
    titolo = "La tua ricerca ha dato come risultato"
    model = Esame
    template_name = 'gestione_medici/lista_esami.html'
    paginate_by = 2

    def get_queryset(self):
        risultati = self.model.objects.filter(stato__exact='disponibile')
        nome = self.request.resolver_match.kwargs['nome']
        cognome = self.request.resolver_match.kwargs['cognome']
        data_inizio = self.request.resolver_match.kwargs['data_inizio']
        data_fine = self.request.resolver_match.kwargs['data_fine']
        tipologia = self.request.resolver_match.kwargs['tipologia']
        print(type(nome), cognome, type(data_inizio), type(data_fine), tipologia)

        if nome:
            print("Arrivato a")
            risultati = risultati.filter(medico__utente__first_name__icontains=nome)
        if cognome:
            print("Arrivato b")
            risultati = risultati.filter(medico__utente__last_name__icontains=cognome)
        if data_inizio :
            print("Arrivato c")
            risultati = risultati.filter(data__gte=data_inizio)
        if data_fine :
            print("Arrivato d")
            risultati = risultati.filter(data__lte=data_fine)
        if tipologia:
            print("Arrivato e ")
            risultati = risultati.filter(tipologia__exact=tipologia)
        
        return risultati'''