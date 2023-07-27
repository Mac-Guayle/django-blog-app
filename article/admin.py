from django.contrib import admin

from .models import Article, Comment

# Register your models here.

# Article alanini ozellestiriyoruz.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title"]
    list_filter = ["created_date", "title"]

    # ArticleAdmin ve Article'i arasinda baglanti kurar.
    class Meta:
        model = Article

admin.site.register(Comment)