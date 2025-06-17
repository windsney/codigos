from django.db import models
from django.core.validators import FileExtensionValidator

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    destaque = models.BooleanField(default=False)
    
    # CAMPO FOTO DEVE TER blank=True E null=True
    foto = models.ImageField(
        upload_to='noticias/fotos/',
        null=True,
        blank=True,  # Isso torna o campo opcional nos formulários
        verbose_name='Foto (opcional)'
    )
    
    video = models.FileField(
        upload_to='noticias/videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])]
    )

    def __str__(self):
        return self.titulo