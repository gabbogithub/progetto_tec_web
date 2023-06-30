from django.shortcuts import render, redirect
from .forms import IdentificativiForm
from django.contrib import messages
from django.views.generic import ListView
from braces.views import GroupRequiredMixin
from .models import Chat


def richiesta_assistenza(request):
    """ Implementa la pagina di richiesta di assistenza che nel caso l'utente 
    sia autenticato, redirige direttamente alla chat con l'assistenza, altrimenti 
    visualizza un form da riempire con nome e cognome """

    if request.user.is_authenticated:
        new_chat = Chat.objects.create(identificativi_utente=request.user.__str__())
        return redirect('gestione_assistenza:chat_assistenza', new_chat.identificativi_utente, 
                        new_chat.pk)
    
    if request.method == 'POST':
        form = IdentificativiForm(request.POST)
        if form.is_valid():
            identificativi = form.cleaned_data.get('identificativi')
            new_chat = Chat.objects.create(identificativi_utente=identificativi)
            return redirect('gestione_assistenza:chat_assistenza', identificativi, 
                            new_chat.pk)
    else:
        form = IdentificativiForm()

    return render(request, template_name='gestione_assistenza/inserimento_identificativi.html', 
                  context={'form':form, 'title':'Richiesta assistenza'})

def chat_assistenza(request, identificativi, pk):
    """ Implementa la view per la chat di assistenza controllando che l'utente possa accedere alla chat richiesta e 
    poi impostando lo stato della chat corretto """

    chat = Chat.objects.get(pk=pk)

    if chat.stato == 'in_corso' or chat.stato == 'terminato' or (chat.stato == 'in_attesa' and not request.user.is_staff):
        messages.error(request, 'Non puoi entrare in questa chat')
        return redirect('home')

    if request.user.is_staff:
        chat.membro_assistenza = request.user
        chat.stato = 'in_corso'
        chat.save()
    else:
        chat.stato = 'in_attesa'
        chat.save()

    return render(request, template_name='gestione_assistenza/pagina_chat.html', 
                  context={'identificativi':identificativi, 'pk':pk, 'title':'Chat assistenza'})

class UtentiAttesaView(GroupRequiredMixin, ListView):
    """ Implementa la view per l'assistenza clienti con gli utenti in attesa e 
    aggiunge una paginazione"""

    group_required = ['Assistenza']
    title = "Pagina con gli utenti in attesa di assistenza"
    model = Chat
    template_name = "gestione_assistenza/utenti_attesa.html"
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(stato='in_attesa')
