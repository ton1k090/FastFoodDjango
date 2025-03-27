from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    '''Категория новостей'''
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    '''Для новостных постов'''
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Скоро здесь будет статья...', verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='media/', blank=True, null=True, verbose_name='Изображение')
    watched = models.IntegerField(default=0, verbose_name='Просмотры статьи')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='posts')
    author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    '''Комментарии к постам'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.TextField(verbose_name='комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'