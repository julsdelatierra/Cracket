from django.db import models
from django.conf import settings
from tools.thumbs import ImageWithThumbsField
from django.conf import settings
from comments.models import Comment

class Character(models.Model):
    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to='uploads/characters/')
    comments = models.ManyToManyField(Comment, related_name='character_comments')
    creation_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.name)
