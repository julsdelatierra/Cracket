from django.http import HttpResponse
from piston.handler import AnonymousBaseHandler, BaseHandler
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
from django.conf import settings
from django.db.models import Q
from piston.resource import Resource
from institutes.models import *
from characters.models import *
from comments.models import *


def institute_parser(institute):
    json_object = {
        'id':institute.id,
        'name':institute.name,
        'image':settings.MEDIA_URL+'/'+institute.image.name,
    }
    return json_object

def person_parser(person):
    json_object = {
        'id':person.id,
        'name':person.name,
        'alias':person.alias,
        'image':settings.MEDIA_URL+'/'+person.image.name,
    }
    return json_object

def comment_parser(comment):
    json_object = {
        'text':comment.text,
        'id':comment.id,
        'creation_date':comment.creation_date,
    }
    return json_object

class CORSResource(Resource):
    """
    Piston Resource to enable CORS.
    """
    
    cors_headers = [
        ('Access-Control-Allow-Origin','*'),
        ('Access-Control-Allow-Headers','*'),
    ]
    
    preflight_headers = cors_headers + [
        ('Access-Control-Allow-Methods','GET'),
        ('Access-Control-Allow-Credentials','true')
    ]
    
    def __call__(self, request, *args, **kwargs):
        request_method = request.method.upper()
        if request_method == "OPTIONS":
            resp = HttpResponse()
            for hk, hv in self.preflight_headers:
                resp[hk] = hv
        else:
            resp = super(CORSResource, self).__call__(request, *args, **kwargs)
            for hk, hv in self.cors_headers:
                resp[hk] = hv
        return resp

class InstitutesHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    
    def read(self, request):
        institutes = Institute.objects.all()
        json_object = {'data':[]}
        for i in institutes:
            json_object['data'].append(institute_parser(i))
        return json_object

class InstituteHandler(BaseHandler):
    
    allowed_methods = ('GET','POST','PUT')
    
    def read(self, request, institute):
        json_object = {'data':[]}
        institute = Institute.objects.get(pk=institute)
        for c in institute.comments.all():
            json_object['data'].append(comment_parser(c))
        return json_object
    
    def create(self, request):
        institute = Institute.objects.create(
            image = request.FILES['image'],
            name = request.POST['name'],
            alias = request.POST['alias'],
        )
        json_object = institute_parser(institute)
        return json_object
    
    def update(self, request, institute):
        institute = Institute.objects.get(pk=institute)
        comment = Comment.objects.create(
            text = request.POST['text']
        )
        institute.comments.add(comment)
        json_object = comment_parser(comment)
        return json_object

class PersonsHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    
    def read(self, request, institute):
        json_object = {'data':[]}
        institute = Institute.objects.get(pk=institute)
        for p in institute.characters.all():
            json_object['data'].append(person_parser(p))
        return json_object

class PersonHandler(BaseHandler):
    
    allowed_methods = ('GET','POST','PUT')
    
    def read(self, request, person):
        json_object = {'data':[]}
        person = Character.objects.get(pk=person)
        for c in person.comments.all():
            json_object['data'].append(comment_parser(c))
        return json_object
    
    def create(self, request, institute):
        institute = Institute.objects.get(pk=institute)
        p = Character.objects.create(
            name = request.POST['name'],
            alias = request.POST['alias'],
            image = request.FILES['image']
        )
        institute.characters.add(p)
        json_object = person_parser(p)
        return json_object
    
    def update(self, request, person):
        person = Character.objects.get(pk=person)
        comment = Comment.objects.create(
            text = request.POST['text']
        )
        person.comments.add(comment)
        json_object = comment_parser(comment)
        return json_object
