from django.conf.urls.defaults import *
from characters import views as characters
from comments import views as comments
from institutes import views as institutes
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    (r'^tos$', direct_to_template,{
        'template': 'tos.html',
        'mimetype': 'text/html'
    }),
    (r'^privacy$', direct_to_template,{
        'template': 'privacy.html',
        'mimetype': 'text/html'
    }),
    (r'^about$', direct_to_template,{
        'template': 'about.html',
        'mimetype': 'text/html'
    }),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', institutes.index),
    (r'^(\d+)$', institutes.view),
    (r'^create$', institutes.create),
    (r'^char/(\d+)$', characters.view),
    (r'^char/create/(\d+)$', characters.create),
    (r'^comment/character/(\d+)$', characters.comment),
    (r'^comment/institute/(\d+)$', institutes.comment),
    (r'^medios/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root' : settings.MEDIA_ROOT,
        'show_indexes':True
    }),
    (r'^api/', include('api.urls')),
)
