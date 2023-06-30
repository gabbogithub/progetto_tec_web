from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """ Definisce un modello manager per un modello utente senza campo
      username"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Crea e salva un utente con l'email e password data """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Crea e salva un utente normale con la data email e password """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Crea e salva un superutente con la data email e password """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class UtenteCustom(AbstractUser):
    """" Definisce un utente personalizzato senza il campo username e con un campo
      per l'immagine profilo """

    username = None
    email = models.EmailField(_('email address'), unique=True)
    foto_profilo = models.ImageField(upload_to ='immagini_utenti/%Y/%m/%d/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = UserManager()

    def __str__(self):
        """ Ritorna stringa con nome e cognome per rappresentare l'utente """
        return f"{self.first_name} {self.last_name}"