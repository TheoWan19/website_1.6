from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.

from .models import Article, ArticleSeries
from users.forms import UserUpdateForm
def home(request):
	matching_series = ArticleSeries.objects.all()
	return render(request, 'core/home.html', {'objects': matching_series})



def series(request, series:str):
	matching_series = Article.objects.filter(series__slug=series).all()
	return render(request, 'core/home.html', {'objects': matching_series})


def article(request, series:str, article:str):
	matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()
	return render(
		request=request, 
		template_name='core/article.html', 
		context={'object': matching_article})

		

