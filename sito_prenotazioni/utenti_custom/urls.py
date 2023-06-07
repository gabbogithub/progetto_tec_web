from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'utenti_custom'

urlpatterns = [
    path('registrazione/', UserCreateView.as_view(), name='registrazione'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout_riuscito/', logout_riuscito, name='logout_riuscito'),
    path('modifica_informazioni/', CustomModificaView.as_view(), name='modifica_informazioni'),
    path('modifica_password/', CustomModificaPassword.as_view(), name='modifica_password'),
]