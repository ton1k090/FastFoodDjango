from .models import Post, Category
from rest_framework import routers, serializers, viewsets


class PostSerializer(serializers.ModelSerializer):
    '''Поля для API'''

    class Meta:
        model = Post
        fields = ('title', 'category', 'created_at', 'content', 'author')


class CategorySerializer(serializers.ModelSerializer):
    '''Поля для API'''
    model = Category
    fields = ('title', 'id')