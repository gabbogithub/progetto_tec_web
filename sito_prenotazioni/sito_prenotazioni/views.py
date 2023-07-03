from django.shortcuts import render

def sito_home(request):
    """ Implementa la view della home limitandosi a restituire il render della 
    pagina """
    
    return render(request, template_name="home.html")