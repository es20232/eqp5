
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Galeria
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

class UsuarioCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um endereço de e-mail válido.')
    
    class Meta:
        model = Usuario
        fields = ('name', 'email', 'password1', 'password2', 'username')

class UsuarioLoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']

class EditForm(UserChangeForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    class Meta:
        model = Usuario
        fields = ['photo', 'name', 'username', 'bio', 'email']
        labels = {'name': 'Nome', 'username': 'Nome de Usuário', 'bio': 'Biografia','email': 'Email',  
        }

class GaleriaForm(forms.ModelForm):
    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    class Meta:
        model = Galeria
        fields = ['foto']
