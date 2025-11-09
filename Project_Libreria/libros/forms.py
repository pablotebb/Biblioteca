from django import forms


class Formulario_libros(forms.Form):
    
    isbn = forms.CharField(label="Isbn", required=True)
    titulo = forms.CharField(label="Título", required=True)
    autor = forms.CharField(label="Autor", required=True)
    categoria = forms.CharField(label="Categoria")
    contenido = forms.CharField(label="Contenido", widget=forms.Textarea)
    imagen = forms.ImageField(label="Imagen")
   
    