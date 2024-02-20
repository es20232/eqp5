from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User

class Usuario(AbstractUser):
    nome = models.CharField(max_length=30, default='Nome')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    profile_picture = models.ImageField(upload_to="profile_imgs/", null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='user_gallery/', null=True, blank=True)
    publica = models.BooleanField(default=False) 

    def __str__(self):
        return f"Photo {self.id} - {self.user.username}"
    
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField()
    #photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)  # Alteração aqui
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post {self.id} - {self.user.username}"

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário por {self.autor.username} em {self.data_publicacao}"



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)