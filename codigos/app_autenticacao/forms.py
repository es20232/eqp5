
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Photo, Post, Comentario 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm

class UsuarioCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um endereço de e-mail válido.')
    
    class Meta:
        model = Usuario
        fields = ('name', 'email', 'password1', 'password2', 'username' )

class UsuarioLoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']

class EditForm(UserChangeForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = Usuario
        fields = ['photo' ]

class Form_editar_informacoes(UserChangeForm):
    bio = forms.CharField(max_length=500, required=False)
    password = forms.CharField(label='Nova Senha', widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput, required=False)
    name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)
    class Meta:
        model = Usuario
        fields = ('name','email', 'username', 'bio')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        fields = ('name','email', 'username', 'bio')
        if password==password_confirm:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance
    
class PhotoForm(forms.ModelForm):
    publica = forms.BooleanField(label='publicar', required=False)  
    class Meta:
        model = Photo
        fields = ['image', 'publica']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['descricao']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']