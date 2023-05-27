from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class CreateUtenteMedico(UserCreationForm):
    '''Classe che definisce il form per la registrazione dei medici'''

    def save(self, commit=True):
        '''Override del metodo save per aggiungere i permessi associati ad un utente medico oltre ad aggiungerlo al database'''

        user = super().save(commit)
        g = Group.objects.get(name="Medici")
        g.user_set.add(user)
        return user 
    
class CreateEsameForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addesame_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Esame"))

    class Meta:
        model = Esame
        fields = ["tipologia", "medico", "data", "stato"]

