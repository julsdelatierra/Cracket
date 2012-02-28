from django.db import models

class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.text)
