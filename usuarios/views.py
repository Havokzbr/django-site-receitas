from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from todas_receitas.models import Receita


# Create your views here.
def register(request):
    """Cadatra um novo usuário no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('register')

        if campo_vazio(email):
            messages.error(request, 'O campo e-mail não pode ficar em branco')
            return redirect('register')

        if senhas_nao_conferem(password, password2):
            messages.error(request, 'As senhas não conferem')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado')
            return redirect('register')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('register')

        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/register.html')


def login(request):
    """Realiza o login de um usuário no sistema."""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos e-mail e senha não podem ficar em branco')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha inválida')
                return redirect('login')
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    """Realiza o logout de um usuário no sistema."""
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    """Exibe todas as receitas cadastradas por um usuário."""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    """Verifica se o campo está vazio."""
    return not campo.strip()


def senhas_nao_conferem(password, password2):
    """Verifica se as senhas são iguais."""
    return password != password2

