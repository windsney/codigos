"""
URL configuration for p3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from tela.views import IndexView,painel,sub,noticias,teste  # Importe sua CBV
from crimes.views import MapaCrimesView
from pessoal.views import dashboard,ProntoEmpregoListView,PesquisarMilitaresListView, BuscarValoresFiltroView,BaseMilitarListView,exportar_pdf
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('painel/', painel.as_view(), name='painel'),
    path('sub/', sub.as_view(), name='sub'),
    path('teste/', teste.as_view(), name='teste'),
    path('', noticias, name='noticias'),
    path('pessoal/', dashboard, name='dashboard'),
    path('militares/', BaseMilitarListView.as_view(), name='lista_militares'),
    
    path('mapa/', MapaCrimesView.as_view(), name='mapa-crimes-publico'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pronto-emprego/', ProntoEmpregoListView.as_view(), name='pronto_emprego_lista'),
    path('pesquisar/', PesquisarMilitaresListView.as_view(), name='nome_da_url_pesquisa'),
    path('buscar-valores-filtro/', BuscarValoresFiltroView.as_view(), name='buscar_valores_filtro'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
