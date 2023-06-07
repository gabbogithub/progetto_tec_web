from django.shortcuts import render

def sito_home(request):
    return render(request, template_name="home.html")