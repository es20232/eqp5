#fast>models.py
from django.db import models
from django import forms

class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imgs/", null=True, blank=True) 
    descricao = models.TextField(blank=True)

class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = [
            'imagem',
            'descricao'
        ]



#paia