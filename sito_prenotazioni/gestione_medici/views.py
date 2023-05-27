from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CreateEsameForm

class CreateEsameView(CreateView):
    #group_required = ["Medici"]
    title = "Aggiungi un esame tra quelli caricati"
    form_class = CreateEsameForm
    template_name = "medici/crea_esame.html"
    success_url = reverse_lazy("gestione_medici:esami_caricati")
