from django.shortcuts import render, redirect
from .models import Category, Post, Comment
from django.db.models import F, Q
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


'''==============================Вьюхи на основе функций==================================='''

# def index(request):
#     '''Главная страница'''
#     posts = Post.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'posts': posts,
#     }
#     return render(request, template_name='cooking/index.html', context=context)


# def category_list(request, pk):
#     '''Реакция на нажатие кнопок категорий'''
#     posts = Post.objects.filter(category_id=pk)
#     context = {
#         'title': posts[0].category,
#         'posts': posts,
#     }
#     return render(request, template_name='cooking/index.html', context=context)


# def post_detail(request, pk):
#     '''Страничка статьи'''
#     article = Post.objects.get(pk=pk)
#     Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
#     ext_post = Post.objects.all().exclude(pk=pk).order_by('-watched')
#     context = {
#         'title': article.title,
#         'post': article,
#         'ext_posts': ext_post
#     }
#     return render(request, template_name='cooking/detail_page.html', context=context)


# def add_post(request):
#     '''Добавление статьи от пользователя'''
#     if request.method == 'POST':
#         form = PostAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post.objects.create(**form.cleaned_data)
#             post.save()
#             return redirect('post_detail', post.pk)
#     else:
#         form = PostAddForm()
#     context = {
#         'form': form,
#         'title': 'Добавить статью'
#     }
#     return render(request, template_name='cooking/add_post.html', context=context)


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


def add_comment(request, post_id):
    '''Добавление комментария статьи'''
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен')
    return redirect('post_detail', post_id)


def profile(request, user_id):
    '''Профиль пользователя'''
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'cooking/profile.html', context=context)



'''========================================================================================'''

'''==============================Вьюхи на основе классов==================================='''


class Index(ListView):
    '''Главная страница'''
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Главная страница'}


class ArticleByCategory(Index):
    '''Реакция на нажатие кнопок категорий'''
    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Для динамических данных'''
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class PostDetail(DetailView):
    '''Страничка статьи'''
    model = Post
    template_name = 'cooking/detail_page.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        '''Для динамических данных'''
        context = super().get_context_data()
        Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
        post = Post.objects.get(pk=self.kwargs['pk'])
        posts = Post.objects.all().exclude(pk=self.kwargs['pk']).order_by('-watched')[:4]
        context['title'] = post.title
        context['ext_posts'] = posts
        context['comments'] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm
        return context


class AddPost(CreateView):
    '''Добавление статьи от пользователя'''
    form_class = PostAddForm
    template_name = 'cooking/add_post.html'
    extra_context = {'title': 'Добавить статью'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    '''Обновление статьи'''
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/add_post.html'


class PostDelete(DeleteView):
    '''Удаление поста'''
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'
    extra_context = {'title': 'Изменить статью'}


class SearchResult(Index):
    '''Поиск по сайту'''

    def get_queryset(self):
        word = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts