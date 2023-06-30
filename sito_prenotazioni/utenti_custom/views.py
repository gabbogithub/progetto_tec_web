from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *

def logout_riuscito(request):
    """ Ritorna il render della pagina di logout """

    return render(request, template_name='registration/logout.html')


class UserCreateView(SuccessMessageMixin, CreateView):
    """ Implementa la view per la registrazione di un utente"""

    title = "Registrazione utente"
    form_class = CustomUserCreationForm
    template_name = 'registration/registrazione.html'
    success_url = reverse_lazy('home')
    success_message = "Ti sei registrato correttamente"

class CustomLoginView(SuccessMessageMixin, LoginView):
    """ Implementa la view per il login dell'utente """

    title = "Login"
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    success_message = "Hai eseguito correttamente l'accesso"

class CustomModificaView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """ Implementa la view per la modifica delle informazioni dell'utente """

    title = "Modifica informazioni"
    form_class = CustomUserChangeForm
    template_name = 'registration/modifica_informazioni.html'
    success_url = reverse_lazy('utenti_custom:modifica_informazioni')
    success_message = "Le modifiche sono state effettuate"

    def get_object(self):
        return self.request.user
    
class CustomModificaPassword(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Implementa la view per la modifica della password dell'utente """

    title = "Modifica password"
    form_class = CustomPasswordChangeForm
    template_name = 'registration/modifica_password.html'
    success_url = reverse_lazy('utenti_custom:modifica_password')
    success_message = "Le password e' stata cambiata con successo"





