from django import forms
from .models import Producto, Categoria
from PIL import *


class FormProducto(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),
        required=True, help_text='La categoría debe estar registrada', empty_label="Seleccione una opción", widget=forms.Select(attrs={'class': 'form-control selectpicker', 'type':"text"}))
    titulo = forms.CharField(
        label='Producto', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese un nombre para el Artículo'}), max_length=250, required=True)
    descripcion = forms.CharField(
        label='Descripción', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese una breve descripción'}), max_length=2000, required=True)
    imagen = forms.ImageField(
        required=True)
    precio = forms.DecimalField(
        label='Precio', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'$'}), max_digits=10, decimal_places=2, required=True)
   
    class Meta:
        model = Producto
        fields = ('categoria','titulo', 'descripcion', 'imagen', 'precio')

#Formulario Categoria
class FormCategoria(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Descripcion'}), max_length=64, required=True, help_text='Requerido. Al menos 4 caracteres.')
    #Metadata
    class Meta:
        model = Categoria
        fields = ("descripcion",)