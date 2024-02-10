# app_autenticacao > models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Galeria(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='galeria_fotos')
    foto = models.ImageField(upload_to='galeria_fotos/')

    def __str__(self):
        return f"Galeria de {self.user.username}"

class Usuario(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_imgs/", null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    galeria = models.ForeignKey(Galeria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
