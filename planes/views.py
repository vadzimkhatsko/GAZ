from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import messages
from django.core.mail import send_mail

# эТО КОМЕНТ ПРПРПРП

def index(request):
    context = {'pas': BaseUserManager().make_random_password(4)}
    return render(request, 'planes/index.html',context)

def logout_view(request):
    logout(request)
    return render(request, 'planes/index.html')


def login_view(request,):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('disable account')
            else:
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким адресом уже существует')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = email
                password = BaseUserManager.make_random_password(4)
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                user.save()
                messages.success(request, 'Регистрация прошла успешно')
#                send_mail('Hello from GAZ', password, '@gmail.com', [email], fail_silently=False )
                return redirect('/')

    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
