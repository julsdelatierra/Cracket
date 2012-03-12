from django.conf.urls.defaults import *
from piston.resource import Resource
from handlers import *

institutes = CORSResource(InstitutesHandler)
persons = CORSResource(PersonsHandler)
institute = CORSResource(InstituteHandler)
person = CORSResource(PersonHandler)

urlpatterns = patterns('',
    url(r'institutes$', institutes),
    url(r'^persons/(\d+)$', persons),
    url(r'institute$', institute),
    url(r'institute/(\d+)$', institute),
    url(r'^person/(\d+)$', person),
)
