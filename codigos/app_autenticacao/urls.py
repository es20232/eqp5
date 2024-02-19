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
    path('perfil/<str:username>/', views.profile_view, name='perfil'),  
    path('upload_perfil/', views.upload_perfil, name='upload_perfil'),
    path('editar_info/', views.editar_info, name='editar_info'),
    path('postar_foto/<int:photo_id>/', views.postar_foto, name='postar_foto'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('excluir_foto/<int:photo_id>/', views.excluir_foto, name='excluir_foto'),
    path('adicionar_comentario/<int:post_id>/', views.adicionar_comentario, name='adicionar_comentario'),
    path('post/<int:post_id>/', views.exibir_post, name='exibir_post'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)