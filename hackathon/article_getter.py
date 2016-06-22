import pandas as pd
import numpy as np
import requests
import json
import lxml.html
import unidecode
from random import choice
from models import InteractionType, UserArticleHistory


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
        category = article['category']
        new_cat = choice(self.categories.keys())
        different = self.__get_article(user=user, mode='search', params={'q':query, 'limit': limit, 'category': self.categories[new_cat]})

        return self.__get_article_data(different['documents'][0])
    
    def get_next_article(self, user, article_id):
        article = self.__get_article(user=user, mode='search/{}'.format(article_id))
        category = article['category']
        new_cat = choice([k for k in self.categories.keys() if k !=category])
        new_article = self.__get_article(user=user, mode='search',
                                  params={'category': self.categories[new_cat], 
                                           'sortBy':'latest'})
        
        return self.__get_article_data(new_article['documents'][0])
    
    def get_recommended_article(self, user):
        history = UserArticleHistory.objects.exclude(user_id='1')        
        
        rec = Recommendation(history)
        rec_article_id = rec.get_scores()
        r = rec.get_user_recommendation(user, rec_article_id)
#         return rec_article_id
        article = self.__get_article(user=user, mode='search/{}'.format(r))
#         return article
#         return rec_article_id
        
        return self.__get_article_data(article)

        

    def __process_text(self, text):
        return unidecode.unidecode(lxml.html.fromstring(text).text_content()).replace('\n','').replace("\'s",'')
    
    def __get_article_data(self, article):

        return json.dumps({'articleId': article['identifier'],
                 'category': article['category'],
                'title': article['title'],
                'text': self.__process_text(article['content']),
                'language': article['language'],
                })
        
    
class Recommendation(object):
    def __init__(self, history):
        self.Q = self.get_Q(history)
        self.lambda_ = 0.1
        self.n_factors = 100
        self.m, self.n = self.Q.shape
        self.n_iterations = 20
        
    def get_Q(self, history):
        interaction_mapping = {
                               InteractionType.COMPLETED: 1,
                               InteractionType.SKIPPED: -2,
                               InteractionType.MORE: 2
                               }
        hist_data = pd.DataFrame(list(history.values('article_id', 'user_id','interaction').distinct()))
        
        hist_data['value'] = hist_data['interaction'].map(interaction_mapping)
        hist_table = hist_data.pivot(index='user_id', columns='article_id', values='value')
        
        return hist_table.fillna(0)
                     
        
    def get_scores(self):
        X = np.random.rand(self.m, self.n_factors) 
        Y = np.random.rand(self.n_factors, self.n)
        errors = []
        for ii in range(self.n_iterations):
            X = np.linalg.solve(np.dot(Y, Y.T) + self.lambda_ * np.eye(self.n_factors), 
                                np.dot(Y, self.Q.T)).T
            Y = np.linalg.solve(np.dot(X.T, X) + self.lambda_ * np.eye(self.n_factors),
                                np.dot(X.T, self.Q))
            
        Q_hat = np.dot(X, Y)
        
        return pd.DataFrame(Q_hat, index=self.Q.index, columns=self.Q.columns)
    
    def get_user_recommendation(self, user_id, scores):
        return scores.loc[user_id].argmax()
    
        
    def __get_error(self, Q, X, Y, W):
        return np.sum((W * (Q - np.dot(X, Y)))**2)
            
class History(object):
    
    def __init__(self, history):
        self.history = history
        
    def filter_history(self, user, articles):
        return articles[~articles.index.isin(self.history[user])]
    
    
    

