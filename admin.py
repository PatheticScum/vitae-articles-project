from django.contrib import admin
from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('pk', 'title')
    list_editable = ('is_published',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)



