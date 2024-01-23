# meu_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm

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
        fields = ['username', 'email', 'bio', 'photo']

    