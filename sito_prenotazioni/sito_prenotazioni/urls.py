"""
URL configuration for sito_prenotazioni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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