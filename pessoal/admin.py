from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Militar  # Importe seu modelo



# Opção 2: Registro customizado (recomendado)
@admin.register(Militar)
class MilitarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'posto_grad', 'qra', 'unidade')  # Campos exibidos na lista
    search_fields = ('nome', 'qra', 'cpf')  # Campos pesquisáveis
    list_filter = ('posto_grad', 'unidade')  # Filtros laterais