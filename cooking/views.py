from django.shortcuts import render, redirect
from .models import Category, Post
from django.db.models import F
from .forms import PostAddForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def index(request):
    '''Главная страница'''
    posts = Post.objects.all()
    context = {
        'title': 'Главная страница',
        'posts': posts,
    }
    return render(request, template_name='cooking/index.html', context=context)


def category_list(request, pk):
    '''Реакция на нажатие кнопок категорий'''
    posts = Post.objects.filter(category_id=pk)
    context = {
        'title': posts[0].category,
        'posts': posts,
    }
    return render(request, template_name='cooking/index.html', context=context)


def post_detail(request, pk):
    '''Страничка статьи'''
    article = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    ext_post = Post.objects.all().exclude(pk=pk).order_by('-watched')
    context = {
        'title': article.title,
        'post': article,
        'ext_posts': ext_post
    }
    return render(request, template_name='cooking/detail_page.html', context=context)


def add_post(request):
    '''Добавление статьи от пользователя'''
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('post_detail', post.pk)
    else:
        form = PostAddForm()
    context = {
        'form': form,
        'title': 'Добавить статью'
    }
    return render(request, template_name='cooking/add_post.html', context=context)


def user_login(request):
    '''Аунтификация пользователя'''
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')
    else:
        form = LoginForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'cooking/login.html', context=context)


def user_logout(request):
    '''Выход'''
    logout(request)
    return redirect('index')


def register(request):
    '''Регистрация пользователя'''
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'cooking/register.html', context=context)