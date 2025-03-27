from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class PostAddForm(forms.ModelForm):
    '''Форма добавления новой статьи от пользователя'''
    class Meta:
        '''класс указывающий поведенческий характер, чертеж длякласса'''
        model = Post
        fields = ['title', 'content', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class LoginForm(AuthenticationForm):
    '''форма для аунтификации пользователя'''
    username = forms.CharField(label='Имя пользователя',
                               max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    '''Форма регистрации пользователя'''
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Почта'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Подтвердите Пароль'}))


class CommentForm(forms.ModelForm):
    '''Форма для написания комментрариев'''
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст вашего комментария'
            })
        }