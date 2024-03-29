from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario, PasswordResetToken, Photo, Post
from .forms import EditForm,UsuarioCreationForm,UsuarioLoginForm,Form_editar_informacoes,PhotoForm,PostForm,ComentarioForm
import uuid
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse

@login_required
def dashboard_view(request):
    postagens = Post.objects.exclude(photo__isnull=True).distinct
    query = request.GET.get('q')
    if query:
        results = Usuario.objects.filter(Q(username__icontains=query) | Q(nome__icontains=query))
    else:
        results = None  
    
    return render(request, 'meu_app/dashboard.html', {'postagens': postagens, 'results': results})

@login_required
def profile_view(request, username=None):
    if username is None:
        user = request.user
    else:
        user = Usuario.objects.get(username=username)
    post_form = PostForm()
    
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=user)
        photo_form = PhotoForm(request.POST, request.FILES)
        post_form = PostForm(request.POST)
        if form.is_valid() and photo_form.is_valid():
            form.save()
            photo_instance = photo_form.save(commit=False)
            photo_instance.user = user
            photo_instance.save()
            if photo_form.cleaned_data['publica']:
                photo_instance.is_public = True
                photo_instance.save()
            # add copia para posts
            descricao = request.POST.get('post_descricao', '') 
            post_instance = Post.objects.create(user=user, descricao=descricao, photo=photo_instance)

            update_session_auth_hash(request, user)
            return redirect('perfil', username=user.username)
        elif post_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.user = user
            post_instance.save()
            return redirect('perfil', username=user.username)
    else:
        form = EditForm(instance=user)
        photo_form = PhotoForm()
        post_form = PostForm()

    photos = Photo.objects.filter(user=user)
    posts = Post.objects.filter(user=user).select_related('photo')

    context = {'usuario': user, 'form': form, 'photo_form': photo_form, 'post_form': post_form, 
        'photos': photos, 'posts': posts, 'excluir_foto_url': reverse('excluir_foto', kwargs={'photo_id': 0}), 
    }
    return render(request, 'meu_app/perfil.html', context)



@login_required
def exibir_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = ComentarioForm()
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
            return redirect('exibir_post', post_id=post_id)
    return render(request, 'meu_app/post.html', {'post': post, 'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        post.save()
        
    else:
        post.likes.add(user)
        post.save()

    return redirect('exibir_post', post_id=post_id)

@login_required
def adicionar_comentario(request, post_id):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            # Salvando o comentário no banco de dados
            novo_comentario = form.save(commit=False)
            novo_comentario.autor = request.user
            novo_comentario.post_id = post_id
            novo_comentario.save()
            return redirect('exibir_post', post_id=post_id)
    else:
        form = ComentarioForm()
    return render(request, 'meu_app/adicionar_comentario.html', {'form': form})

@login_required
def postar_foto(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']
            post = Post.objects.create(user=request.user, descricao=descricao, photo=photo)
            return redirect('perfil', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'meu_app/postar_foto.html', {'form': form, 'photo': photo})
    
@login_required
def upload_perfil(request):
    form = EditForm(instance=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():  
            form.save()
            return redirect('perfil') 
    return render(request, 'meu_app/upload_perfil.html', {'form': form})

@login_required
def editar_info(request):
    if request.method == 'POST':
        form = Form_editar_informacoes(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user
            form.save()
            update_session_auth_hash(request, user)
            return redirect('perfil', username=user.username) 
    else: 
        form = Form_editar_informacoes(instance=request.user)
    return render(request, 'meu_app/editar_info.html', {'form': form})

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


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return redirect('perfil', username=post.user.username)


def excluir_foto(request, photo_id):
    # Recupera a foto do banco de dados
    photo = get_object_or_404(Photo, pk=photo_id)

    # Verifica se o usuário logado é o proprietário da foto
    if request.user == photo.user:
        # Exclui a foto do banco de dados
        photo.delete()
        return JsonResponse({'mensagem': 'Foto excluída com sucesso.'})
    else:
        return JsonResponse({'erro': 'Você não tem permissão para excluir esta foto.'}, status=403)