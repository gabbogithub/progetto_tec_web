from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import IdentificativiForm
from django.contrib import messages
from django.views.generic import ListView
from braces.views import GroupRequiredMixin
from .models import Chat


def richiesta_assistenza(request):
    if request.user.is_authenticated:
        new_chat = Chat.objects.create(identificativi_utente=request.user.__str__())
        return redirect('gestione_assistenza:chat_assistenza', new_chat.identificativi_utente, new_chat.pk)
    
    if request.method == 'POST':
        form = IdentificativiForm(request.POST)
        if form.is_valid():
            identificativi = form.cleaned_data.get('identificativi')
            new_chat = Chat.objects.create(identificativi_utente=identificativi)
            return redirect('gestione_assistenza:chat_assistenza', identificativi, new_chat.pk)
    else:
        form = IdentificativiForm()

    return render(request, template_name='gestione_assistenza/inserimento_identificativi.html', context={'form':form})

def chat_assistenza(request, identificativi, pk):
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
                  context={'identificativi':identificativi, 'pk':pk})

class UtentiAttesaView(GroupRequiredMixin, ListView):
    group_required = ['Assistenza']
    title = "Pagina con gli utenti in attesa di assistenza"
    model = Chat
    template_name = "gestione_assistenza/utenti_attesa.html"
    paginate_by = 5

    def get_queryset(self):
        return Chat.objects.filter(stato='in_attesa')
