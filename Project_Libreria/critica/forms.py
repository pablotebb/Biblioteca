from django import forms


class Formulario_critica(forms.Form):
    
    titulo = forms.CharField(label="Título", required=True)
    contenido = forms.CharField(label="Contenido", widget=forms.Textarea)
    
    


    