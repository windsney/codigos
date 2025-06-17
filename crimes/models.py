from django.db import models

# crimes/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models

class Crime(models.Model):
    TIPO_CHOICES = [
        ('ROUBO', 'Roubo'),
        ('FURTO', 'Furto'),
        ('HOMICIDIO', 'Homicidio'),
        ('OUTRO', 'Outro'),
    ]
    
    tipo = models.CharField(max_length=25, choices=TIPO_CHOICES, verbose_name='Tipo de Crime')
    data = models.DateTimeField(auto_now_add=True, verbose_name='Data do Ocorrido')
    localizacao = gis_models.PointField(verbose_name='Localização (clique no mapa)')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    endereco = models.CharField(max_length=255, blank=True, verbose_name='Endereço Aproximado')
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    
    class Meta:
        verbose_name = 'Registro de Crime'
        verbose_name_plural = 'Registros de Crimes'
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.bairro} - {self.data.strftime('%d/%m/%Y')}"