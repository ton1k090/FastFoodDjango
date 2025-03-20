from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'watched', 'is_published', 'category', 'get_image')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('is_published', 'category')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="100" height="110" ')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
