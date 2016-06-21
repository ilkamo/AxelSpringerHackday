import pandas as pd
import requests
import json
import lxml.html
import unidecode
from random import choice


class Parameters:
    URL = 'https://frontend-api.ipool.asideas.de/api/v3/'
    AUTH = ('hackathon', 'hackme')
    CATEGORIES = {"sports": '"Sport"',
                  "sport": '"Sport"',
                    "business": '"Wirtschaft"',
                    "politics": '"Politik"',
                    "international": '"Internationales"',
                    "culture": '"Kultur"',
                    'important': '"Vermischtes"',
                }

    
class ArticleImporter(object):
    
    def __init__(self, url, auth, categories, history):
        self.url = url
        self.auth = auth
        self.categories = categories
        self.history = history

        
    def __get_article(self, user, mode, params={}):
        url = '{}{}'.format(self.url, mode)
        response = requests.get(url=url, auth=self.auth, params=params)
        article = json.loads(response.text)
        
        return article

        
    def get_search_category(self, user, category, limit=10):
        articles = self.__get_article(user=user, mode='search',
                                  params={'category': self.categories[category], 
                                          'limit': limit, 'sortBy':'latest'})
        article = [a for a in articles['documents'] if a['identifier'] not in self.history][0]
        
        return self.__get_article_data(article)
    
    
    def get_related(self, user, article_id, limit=10):
        articles = self.__get_article(user=user, mode='related/{}'.format(article_id), params={'limit': limit})
        article = [a for a in articles['documents'] if a['identifier'] not in self.history][0]

        return self.__get_article_data(article)
    
    
    def get_different(self, user, article_id, limit=10):
        article = self.__get_article(user=user, mode='search/{}'.format(article_id))
        keywords = article['keywords']
        query = ''
        if keywords:
            query = ' NOT '.join(keywords)  
                             
        different = self.__get_article(user=user, mode='search', params={'q':query, 'limit': limit})
        
        return self.__get_article_data(article)
    
    def get_next_article(self, user, article_id):
        article = self.__get_article(user=user, mode='search/{}'.format(article_id))
        category = article['category']
        new_cat = choice([k for k in self.categories.keys() if k !=category])
        new_article = self.__get_article(user=user, mode='search',
                                  params={'category': self.categories[new_cat], 
                                           'sortBy':'latest'})
        
        return self.__get_article_data(new_article['documents'][0])
    
    def get_recommended_article(self, user):
        articles = self.__get_article(user=user, mode='search',
                                  params={'limit': 100, 'sortBy':'latest'})
        
    
    def __process_text(self, text):
        return unidecode.unidecode(lxml.html.fromstring(text).text_content()).replace('\n','').replace("\'s",'')
    
    def __get_article_data(self, article):

        return json.dumps({'articleId': article['identifier'],
                 'category': article['category'],
                'title': article['title'],
                'text': self.__process_text(article['content']),
                'language': article['language'],
                })
        
    
class History(object):
    
    def __init__(self, history):
        self.history = history
        
    def filter_history(self, user, articles):
        return articles[~articles.index.isin(self.history[user])]
    
    
    

