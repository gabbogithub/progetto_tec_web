from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import *

class CreateMedicoForm(UserCreationForm):
    '''Classe che definisce il form per la registrazione dei medici'''

    def save(self, commit=True):
        '''Override del metodo save per aggiungere i permessi associati ad un utente medico oltre ad aggiungerlo al database'''

        user = super().save(commit)
        g = Group.objects.get(name="Medici")
        g.user_set.add(user)
        return user 

class FiltraEsameForm(forms.Form):
    helper = FormHelper()
    helper.form_id = 'cerca_esame_crispy_form'
    helper.form_method = 'GET'
    helper.add_input(Submit("submit","Filtra Esami"))
    categorie = [('', '--------'), ('stato', 'Stato'), ('data', 'Data')]
    search_categoria = forms.ChoiceField(label="Come vuoi filtrare?", choices=categorie, 
                                         required=False)
    search_stato = forms.ChoiceField(label='Quale stato?', choices=Esame.STATI_POSSIBILI, required=False)
    search_data_inizio = forms.DateTimeField(label="Da quando?", required=False, widget=DateTimePickerInput())
    search_data_fine = forms.DateTimeField(label="Fino a quando?", required=False, 
                                           widget=DateTimePickerInput(range_from='search_data_inizio'))

class CreateEsameForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_esame_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Esame"))

    class Meta:
        model = Esame
        fields = ['tipologia', 'data']
        widgets = {
            'data': DateTimePickerInput(),
        }
    
class ModificaEsameForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "modifica_esame_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Modifica Esame"))

    class Meta:
        model = Esame
        fields = ['tipologia', 'stato', 'data',]
        widgets = {
            'data': DateTimePickerInput(),
        }

class CreaCommentoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "crea_commento_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Pubblica commento"))

    class Meta:
        model = Commento
        fields = ['testo']
