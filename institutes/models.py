from django.db import models
from tools.thumbs import ImageWithThumbsField
from comments.models import Comment
from characters.models import Character

class Institute(models.Model):
    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to='uploads/institutes/')
    comments = models.ManyToManyField(Comment, related_name='institute_comments')
    characters = models.ManyToManyField(Character, related_name='characters')

    def __unicode__(self):
        return unicode(self.name)
