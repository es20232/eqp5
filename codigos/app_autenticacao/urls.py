from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('criar_conta/', views.criar_conta_view, name='criar_conta'),
    path('confirmar-conta/', views.confirmar_conta, name='confirmar_conta'),
    path('iniciar-redefinir-senha/', views.iniciar_redefinir_senha, name='iniciar_redefinir_senha'),
    path('redefinir-senha/<str:token>/', views.redefinir_senha, name='redefinir_senha'),
    path('perfil/', views.profile_view, name='perfil'),  
    path('upload_perfil/', views.upload_perfil, name='upload_perfil'),
    path('editar_conta/', views.editar_conta, name='editar_conta'), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
