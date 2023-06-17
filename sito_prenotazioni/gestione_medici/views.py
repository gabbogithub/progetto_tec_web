from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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
    return user.groups.filter(name='Medici').exists()

@user_passes_test(ha_gruppo_medico)
def esami_caricati(request):
    user = get_object_or_404(UtenteCustom, pk=request.user.pk)
    medico = user.medico
    esami = medico.esami_caricati.all()
    paginatore = Paginator(esami, 1)
    numero_pagina = request.GET.get("page")
    pagina = paginatore.get_page(numero_pagina)
    ctx = {'page_obj': pagina}
    return render(request,"gestione_medici/esami_caricati.html",ctx)

class CreateEsameView(SuccessMessageMixin, GroupRequiredMixin, CreateView):
    group_required = ['Medici']
    title = "Aggiungi un esame tra quelli caricati"
    form_class = CreateEsameForm
    template_name = 'gestione_medici/crea_esame.html'
    success_url = reverse_lazy('gestione_medici:crea_esame')
    success_message = "L'esame e' stato creato con successo"

    def form_valid(self, form):
        form.instance.medico = self.request.user.medico
        form.instance.stato = 'disponibile'
        return super().form_valid(form)

class ModificaEsameView(SuccessMessageMixin, GroupRequiredMixin, UpdateView):
    group_required = ['Medici']
    title = "Modifica l'esame"
    model = Esame
    form_class = ModificaEsameForm
    template_name = "gestione_medici/modifica_esame.html"
    success_url = reverse_lazy('gestione_medici:esami_caricati')
    success_message = "L'esame e' stato modificato con successo"

class ModificaInformazioniView(SuccessMessageMixin, GroupRequiredMixin, UpdateView):
    group_required = ['Medici']
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
        commenti_totali = context['medico'].commenti.all()
        context['commenti'] = commenti_totali[:3]
        return context

class CommentiMedicoView(ListView):
    title = "Pagina con i commenti sul medico"
    model = Commento
    template_name = "gestione_medici/commenti_totali.html"
    paginate_by = 2

    def get_queryset(self):
        medico = Medico.objects.get(pk=self.kwargs['pk'])
        self.context = {'medico': medico}
        return medico.commenti.all()
    
    def get_context_data(self, **kwargs):
        self.context = self.context | super().get_context_data(**kwargs) #unione due dizionari
        return self.context
    
class CreaCommentoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    title = "Crea un commento"
    model = Commento
    form_class = CreaCommentoForm
    template_name = 'gestione_medici/crea_commento.html'
    success_message = "Il commento e' stato creato con successo"

    def form_valid(self, form):
        form.instance.commentatore = self.request.user
        form.instance.medico = Medico.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "Hai gia' commentato questo medico")

        return HttpResponseRedirect(reverse_lazy('gestione_medici:informazioni_medico', kwargs={'pk': self.kwargs['pk']}))
    
    def get_success_url(self):
        return reverse_lazy('gestione_medici:informazioni_medico', kwargs={'pk': self.kwargs['pk']})