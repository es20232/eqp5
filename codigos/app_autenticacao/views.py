from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioLoginForm

@login_required
def dashboard_view(request):
    return render(request, 'meu_app/dashboard.html', {'usuario': request.user})

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
def criar_conta_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            # Adicionar lógica para envio do e-mail de confirmação
            enviar_email_confirmacao(request, user.email, user.id)

            messages.success(request, 'Conta criada com sucesso! Um e-mail de confirmação foi enviado.')
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
        messages.error(request, 'Erro ao confirmar a conta. Usuário não encontrado.')
    return redirect('login')
