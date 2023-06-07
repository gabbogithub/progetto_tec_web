from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *

def logout_riuscito(request):
    return render(request, template_name="registration/logout.html")


class UserCreateView(SuccessMessageMixin, CreateView):
    """Classe che implementa la view per la registrazione di un utente"""
    form_class = CustomUserCreationForm
    template_name = 'registration/registrazione.html'
    success_url = reverse_lazy('home')
    success_message = "Ti sei registrato correttamente"

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    success_message = "Hai eseguito correttamente l'accesso"

class CustomModificaView(SuccessMessageMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/modifica_informazioni.html'
    success_url = reverse_lazy('utenti_custom:modifica_informazioni')
    success_message = "Le modfiche sono state effettuate"

    def get_object(self):
        return self.request.user
    
class CustomModificaPassword(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/modifica_password.html'
    success_url = reverse_lazy('utenti_custom:modifica_password')
    success_message = "Le password è stata cambiata con successo"





