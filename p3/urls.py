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
from tela.views import IndexView,painel,sub,noticias  # Importe sua CBV
from crimes.views import MapaCrimesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('painel/', painel.as_view(), name='painel'),
    path('sub/', sub.as_view(), name='sub'),
    path('', noticias, name='noticias'),
    path('mapa/', MapaCrimesView.as_view(), name='mapa-crimes-publico'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
