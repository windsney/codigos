from django.contrib import admin

# Register your models here.
# crimes/admin.py
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Crime
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render
import folium
from folium.plugins import HeatMap

class CrimeAdmin(LeafletGeoAdmin):
    list_display = ('tipo', 'data_formatada', 'bairro', 'endereco_curto', 'mapa_link')
    list_filter = ('tipo', 'bairro', 'data')
    search_fields = ('descricao', 'endereco', 'bairro')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'descricao')
        }),
        ('Localização', {
            'fields': ('endereco', 'bairro', 'localizacao')
        }),
    )
    
    def data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y %H:%M')
    data_formatada.short_description = 'Data'
    
    def endereco_curto(self, obj):
        return obj.endereco[:30] + '...' if len(obj.endereco) > 30 else obj.endereco
    endereco_curto.short_description = 'Endereço'
    
    def mapa_link(self, obj):
        url = reverse('mapa-crimes-publico')
        return format_html('<a href="{}" target="_blank">Ver no Mapa</a>', url)
    mapa_link.short_description = 'Mapa'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mapa/', self.admin_site.admin_view(self.mapa_admin_view)),
        ]
        return custom_urls + urls
    
    def mapa_admin_view(self, request):
        # Mesma view do mapa público, mas apenas para admin
        from .views import MapaCrimesView
        return MapaCrimesView.as_view()(request)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['titulo_pagina'] = "Gerenciamento de Ocorrências Criminais"
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Crime, CrimeAdmin)