from django.contrib import admin
from django import forms
from .models import Noticia
from django.utils.html import format_html

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna os campos não obrigatórios na interface
        self.fields['foto'].required = False
        self.fields['video'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        foto = cleaned_data.get('foto')
        video = cleaned_data.get('video')
        
        if not foto and not video:
            raise forms.ValidationError(
                "Você deve adicionar pelo menos uma foto ou um vídeo",
                code='missing_media'
            )
        return cleaned_data

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    form = NoticiaForm
    list_display = ('titulo', 'data_publicacao', 'destaque', 'media_status')
    
    def media_status(self, obj):
        if obj.video:
            return format_html('<span style="color:green">✓ Vídeo</span>')
        elif obj.foto:
            return format_html('<span style="color:blue">✓ Foto</span>')
        return format_html('<span style="color:red">✗ Sem mídia</span>')
    media_status.short_description = 'Status Mídia'