from django.http import HttpResponse
from article_getter import History, ArticleImporter, Parameters
from django.views.generic import View
from models import  InteractionType, UserArticleHistory
from django.core import serializers


class CategoryView(View):
    
    def get(self, request, category):

        history = [v[0] for v in UserArticleHistory.objects.filter(user_id='1').values_list('article_id')]
        importer = ArticleImporter(Parameters.URL, Parameters.AUTH, Parameters.CATEGORIES, history)
        articles = importer.get_search_category('1', category, 10)
      
        return HttpResponse(articles)
    
    
class RelatedView(View):
    
    def get(self, request, article_id): 
         
        history = [v[0] for v in UserArticleHistory.objects.filter(user_id='1').values_list('article_id')]
        importer = ArticleImporter(Parameters.URL, Parameters.AUTH, Parameters.CATEGORIES, history)
        articles = importer.get_related('1', article_id, 10)
        UserArticleHistory.objects.create(user_id='1', article_id=article_id, interaction=InteractionType.MORE)
        
        return HttpResponse(articles)
    
    
class DifferentView(View):
    
    def get(self, request, article_id):
        
        history = [v[0] for v in UserArticleHistory.objects.filter(user_id='1').values_list('article_id')]
        importer = ArticleImporter(Parameters.URL, Parameters.AUTH, Parameters.CATEGORIES, history)
        articles = importer.get_different('1', article_id, 1)
        
        UserArticleHistory.objects.create(user_id='1', article_id=article_id, interaction=InteractionType.SKIPPED)
      
        return HttpResponse(articles)
    
    
class CompletedtView(View):
    
    def get(self, request, article_id):
        
        history = [v[0] for v in UserArticleHistory.objects.filter(user_id='1').values_list('article_id')]
        importer = ArticleImporter(Parameters.URL, Parameters.AUTH, Parameters.CATEGORIES, history)
        articles = importer.get_next_article('1', article_id)
        UserArticleHistory.objects.create(user_id='1', article_id=article_id, interaction=InteractionType.COMPLETED)
      
        return HttpResponse(articles)
    
    
class RecommendView(View):
    
    def get(self, request, article_id):
        
        history = [v[0] for v in UserArticleHistory.objects.filter(user_id='1').values_list('article_id')]
        importer = ArticleImporter(Parameters.URL, Parameters.AUTH, Parameters.CATEGORIES, history)
        articles = importer.get_recommended_article('1')
        UserArticleHistory.objects.create(user_id='1', article_id=article_id, interaction=InteractionType.RECOMMENDED)
      
        return HttpResponse(articles)

    
