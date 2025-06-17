from django.shortcuts import render

# Create your views here.
# crimes/views.py
from django.shortcuts import render
from django.views import View
from .models import Crime
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen, MiniMap
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time


class MapaCrimesView(View):
    def get(self, request):
        # Coordenadas de Rondonópolis-MT
        CENTRO_LAT = -16.4703
        CENTRO_LON = -54.6360
        
        # Limites aproximados da cidade
        bounds = [[-16.55, -54.70], [-16.40, -54.55]]
        
        # Criar mapa
        m = folium.Map(
            location=[CENTRO_LAT, CENTRO_LON],
            zoom_start=14,
            tiles='cartodbpositron',
            min_zoom=12,
            max_bounds=True,
            control_scale=True
        )
        
        # Limitar visualização à área de Rondonópolis
        m.fit_bounds(bounds)
        
        # Filtros
        tipo_crime = request.GET.get('tipo')
        bairro = request.GET.get('bairro')
        
        # Obter crimes filtrados
        crimes = Crime.objects.all()
        if tipo_crime:
            crimes = crimes.filter(tipo=tipo_crime)
        if bairro:
            crimes = crimes.filter(bairro__icontains=bairro)
        
        # Preparar dados para o mapa
        heat_data = []
        marker_data = []
        
        for crime in crimes:
            if crime.localizacao:
                coord = [crime.localizacao.y, crime.localizacao.x]
                popup = f"""
                    <b>{crime.get_tipo_display()}</b><br>
                    <b>Data:</b> {crime.data.strftime('%d/%m/%Y %H:%M')}<br>
                    <b>Bairro:</b> {crime.bairro}<br>
                    <b>Endereço:</b> {crime.endereco}<br>
                    <b>Descrição:</b> {crime.descricao[:100]}...
                """
                heat_data.append(coord)
                marker_data.append({
                    'coord': coord,
                    'popup': popup,
                    'icon': 'red' if crime.tipo == 'ROUBO' else 'blue'
                })
        
        # Adicionar mapa de calor
        HeatMap(heat_data, radius=15, blur=10, 
               gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'orange', 1.0: 'red'}).add_to(m)
        
        # Adicionar marcadores agrupados
        marker_cluster = MarkerCluster(name="Ocorrências").add_to(m)
        for data in marker_data:
            folium.Marker(
                location=data['coord'],
                popup=data['popup'],
                icon=folium.Icon(color=data['icon'], icon='info-sign')
            ).add_to(marker_cluster)
        
        # Adicionar controles extras
        Fullscreen().add_to(m)
        MiniMap().add_to(m)
        folium.LayerControl().add_to(m)
        
        # Estatísticas para exibir no template
        total_crimes = crimes.count()
        roubos = crimes.filter(tipo='ROUBO').count()
        furtos = crimes.filter(tipo='FURTO').count()
        homicidios = crimes.filter(tipo='HOMICIDIO').count()
        
        # Bairros para filtro
        bairros = Crime.objects.values_list('bairro', flat=True).distinct()
        
        context = {
            'mapa': m._repr_html_(),
            'titulo': 'Mapa de Ocorrências Criminais - Rondonópolis-MT',
            'total_crimes': total_crimes,
            'roubos': roubos,
            'furtos': furtos,
            'homicidios': homicidios,
            'bairros': bairros,
            'tipo_filtro': tipo_crime,
            'bairro_filtro': bairro,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY if hasattr(settings, 'GOOGLE_MAPS_API_KEY') else None
        }
        
        return render(request, 'crimes/mapa_publico.html', context)
    

