from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from gestione_medici.models import Esame

class SearchEsamiForm(forms.Form):
    """ Definisce un form per la ricerca degli esami """
    
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_nome = forms.CharField(label="Inserisci il nome del medico", max_length=100,
                                   required=False)
    search_cognome = forms.CharField(label="Inserisci il cognome del medico",
                                     max_length=100, required=False)
    search_data_inizio = forms.DateTimeField(label="Da quando?", required=False,
                                             widget=DateTimePickerInput())
    search_data_fine = forms.DateTimeField(label="Fino a quando?", required=False, 
                                           widget=DateTimePickerInput(range_from='search_data_inizio'))
    # tipologie a cui viene aggiunta una label vuota nel caso l'utente non volesse
    # selezionarne nessuna
    search_tipologia = forms.ChoiceField(label="Che tipo di visita?", choices=[('','---------')] 
                                         + Esame.TIPOLOGIE_POSSIBILI, required=False)