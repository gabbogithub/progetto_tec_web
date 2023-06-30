from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class IdentificativiForm(forms.Form):
    """ Form per l'invio degli identificativi per connettersi ad una chat """
    
    helper = FormHelper()
    helper.form_id = 'identificativi_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Collegati'))
    identificativi = forms.CharField(label="Nome e cognome",max_length=30, 
                                     min_length=1, required=True)