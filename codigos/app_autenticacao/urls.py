from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('criar_conta/', views.criar_conta_view, name='criar_conta'),
    path('confirmar-conta/', views.confirmar_conta, name='confirmar_conta'),
]
