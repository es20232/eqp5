from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario, PasswordResetToken
from .forms import UsuarioCreationForm, UsuarioLoginForm
import uuid
from django.urls import reverse

@login_required
def dashboard_view(request):
    return render(request, 'meu_app/dashboard.html', {'usuario': request.user})

@login_required
def profile_view(request):
    return render(request, 'meu_app/perfil.html', {'usuario':request.user})

def login_view(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Conta não autenticada.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = UsuarioLoginForm(request)
    return render(request, 'meu_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def criar_conta_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            enviar_email_confirmacao(request, user.email, user.id)
            messages.success(request, 'Conta criada com sucesso! Um e-mail de confirmação foi enviado para o email cadastrado.')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UsuarioCreationForm()
    return render(request, 'meu_app/criarconta.html', {'form': form})

def enviar_email_confirmacao(request, email, user_id):
    subject = 'Confirmação de Conta'
    message = f'Clique no link abaixo para confirmar sua conta:\n\n'
    message += f'{request.build_absolute_uri("/confirmar-conta/")}?user_id={user_id}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]
    send_mail(subject, message, from_email, to_email)

def confirmar_conta(request):
    user_id = request.GET.get('user_id', '')
    try:
        user = Usuario.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        messages.success(request, 'Conta confirmada com sucesso! Faça login para continuar.')
    except Usuario.DoesNotExist:
        messages.error(request, 'Erro ao confirmar a conta. Usuário não encontrado ou link inválido.')
    return redirect('login')

def iniciar_redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Usuario.objects.get(email=email)
            #user = get_object_or_404(Usuario, email=email)
            token = str(uuid.uuid4())
            PasswordResetToken.objects.create(user=user, token=token)
            reset_link = request.build_absolute_uri(reverse('redefinir_senha', args=[token]))
            send_mail(
                'Redefinir Senha',
                f'Clique no link para redefinir sua senha: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,)
            return render(request, 'password/email_enviado.html')
        except Usuario.DoesNotExist:
            messages.error(request, 'O email fornecido não está associado a uma conta. Tente novamente ou crie uma nova conta.')
            return redirect('iniciar_redefinir_senha')
    return render(request, 'password/iniciar_redefinir_senha.html')

from django.contrib.auth.hashers import check_password

def redefinir_senha(request, token):
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')      
        if nova_senha == confirmar_senha:
            token_redefinir = PasswordResetToken.objects.get(token=token)
            user = token_redefinir.user
            if user.check_password(nova_senha):
                messages.error(request, 'A nova senha não pode ser igual à senha atual. Escolha uma senha diferente.')
                return redirect('redefinir_senha', token=token)
            user.set_password(nova_senha)
            user.save()
            token_redefinir.delete()
            return render(request, 'password/senha_alterada.html')
        else:
            messages.error(request, 'As senhas não coincidem. Tente novamente.')
            return redirect('redefinir_senha', token=token)
    return render(request, 'password/redefinir_senha.html', {'token': token})


