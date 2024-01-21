from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('criar_conta/', views.criar_conta_view, name='criar_conta'),
    path('confirmar-conta/', views.confirmar_conta, name='confirmar_conta'),
    path('iniciar-redefinir-senha/', views.iniciar_redefinir_senha, name='iniciar_redefinir_senha'),
    path('redefinir-senha/<str:token>/', views.redefinir_senha, name='redefinir_senha'),
    path('perfil/', views.profile_view, name='perfil'),  
]

