from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class Usuario(AbstractUser):
    
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)