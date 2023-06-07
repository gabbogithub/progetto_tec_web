from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.mail import send_mail
from .models import UtenteCustom

class CustomUserCreationForm(UserCreationForm):
    """Classe che implementa il form per la registrazione di un utente"""
    helper = FormHelper()
    helper.form_id = 'addutente_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Registrati'))

    def save(self, commit=True):
        user = super().save(commit)
        send_mail(
            "Conferma registrazione",
            "La registrazione è avvenuta con successo.",
            "sito_prenotazioni@gmail.com",
            [user.email],
            fail_silently=False,
        )
        return user

    class Meta:
        model = UtenteCustom
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'foto_profilo')

class CustomUserChangeForm(UserChangeForm):
    helper = FormHelper()
    helper.form_id = 'changeutente_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Modifica'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = self.fields.get("password")
        if self.password:
            self.password.help_text = (
            "Non posso mostrarti la tua password attuale perche' viene cifrata prima di "
            'essere salvata, ma la puoi cambiare cliccando su questo <a href="{}">link</a>.'
            ) 
            self.password.help_text = self.password.help_text.format(
                f"../../utente/modifica_password/"
            )

    class Meta:
        model = UtenteCustom
        fields = ('email', 'first_name', 'last_name', 'password', 'foto_profilo')

class CustomPasswordChangeForm(PasswordChangeForm):
    helper = FormHelper()
    helper.form_id = 'changepassword_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Modifica'))

    class Meta:
        model = UtenteCustom
        fields = '__all__'