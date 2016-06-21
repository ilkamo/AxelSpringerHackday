from django.db import models


class InteractionType(object):
    MORE = 'more'
    SKIPPED = 'skipped'
    COMPLETED = 'completed'
    RECOMMENDED = 'recommended'
#     
#     
class RASUser(models.Model):
    user_profile = models.CharField(max_length=30)
    
 
class UserArticleHistory(models.Model):
    user_id = models.CharField(max_length=30)
    article_id = models.CharField(max_length=30)
    interaction = models.CharField(max_length=30)