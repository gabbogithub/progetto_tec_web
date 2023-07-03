from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from .initcmds import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$|^\/$|^home\/$", sito_home, name="home"),
    path('utente/', include('utenti_custom.urls')),
    path('medici/', include('gestione_medici.urls')),
    path('gestione_utenti/', include('gestione_utenti.urls')),
    path('assistenza/', include('gestione_assistenza.urls'))
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

crea_gruppi()