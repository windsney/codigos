from django.shortcuts import render
from .models import Noticia

def noticias_tv(request):
    noticias = Noticia.objects.filter(destaque=True).order_by('-data_publicacao')
    return render(request, 'noticias_tv.html', {'noticias': noticias})

# Create your views here.
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "tela/index.html"


class painel(TemplateView):
    template_name = "tela/painel.html"


def noticias(request):
    noticias = Noticia.objects.filter(destaque=True).order_by('-data_publicacao')
    return render(request, 'tela/noticias.html', {'noticias': noticias})
    

class sub(TemplateView):
    template_name = "tela/sub.html"