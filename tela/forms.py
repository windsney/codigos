from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        foto = cleaned_data.get('foto')
        video = cleaned_data.get('video')
        
        if not foto and not video:
            raise forms.ValidationError("Você deve adicionar pelo menos uma foto ou um vídeo")
        
        return cleaned_data