from django.contrib import admin
from .models import Article, ArticleSeries


# Register your models here.

class ArticleSeriesAdmin(admin.ModelAdmin):
	fields = [
		'title',
		'subtitle',
		'slug',
		'author',
		#'published',
	]

class ArticleAdmin(admin.ModelAdmin):
	fieldsets = [
		('Header', {'fields': ['title', 'subtitle', 'article_slug', 'series', 'author']}),
		('Content', {'fields': ['content', 'notes']}),
		('Date', {'fields': ['modified']}),
	]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleSeries, ArticleSeriesAdmin)
