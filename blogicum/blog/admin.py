from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post, User


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'posts_count')

    @admin.display(description='Кол-во постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category',
        'show_image',
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category',
        'location',
    )
    search_fields = ('title',)
    list_filter = ('category', 'location', 'is_published')
    list_display_links = ('title', 'author', )

    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url}'
                             'width="80" height="60">')
        return 'Нет изображения'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
    )

    search_fields = ('text',)
    list_filter = ('post',)
    list_display_links = ('text', 'post')


admin.site.empty_value_display = 'Не задано'
