from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    '''Classe che implementa un backend personalizzato per fare il login con l'email dell'utente'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''Metodo che controlla se l'email data in input corrisponde ad un utente e nel caso
        venga trovata una voce che corrisponde, viene controllata anche la password. Nel caso 
        l'autenticazione fallisca viene ritornato "None"'''
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None