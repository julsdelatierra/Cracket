#!/usr/bin/python
#encoding:utf-8
import re
from django.http import HttpResponse as response
from django.shortcuts import render_to_response as render, get_object_or_404 as get_or_404, redirect
from django.template.context import RequestContext as rc
from institutes.models import Institute
from comments.models import Comment
from django.conf import settings
from tools import twitter

def index(request):
    args = {
        'institutes':Institute.objects.all()
    }
    return render('institutes.html', args, context_instance=rc(request))

def view(request, institute):
    args = {
        'institute' : get_or_404(Institute, pk=institute),
        'characters' : get_or_404(Institute, pk=institute).characters.all()
    }
    return render('view_institute.html', args, context_instance=rc(request))

def create(request):
    if request.POST:
        institute = Institute.objects.create(
            name = request.POST['name'],
            alias = request.POST['alias'],
            image = request.FILES['image']
        )
        return redirect('/%s' % (institute.id))
    args = {}
    return render('create_institute.html', args, context_instance=rc(request))

def comment(request, institute):
    if request.POST:
        institute = get_or_404(Institute, pk=institute)
        exp = ''
        for w in settings.UNAVAILABLE_WORDS:
            if exp is '':
                exp = w
            else:
                exp += '|'+w
        regexp = re.compile('('+exp+')+',re.UNICODE)
        if re.search(regexp,request.POST['text'].lower()):
            return redirect('/%s?unavailable=1' % (institute.id))
        if institute.comments.filter(text=request.POST['text']).count() > 0:
            return redirect('/%s?said=1' % (institute.id))
        comment = Comment.objects.create(
            text=request.POST['text']
        )
        institute.comments.add(comment)
        try:
            tw = twitter.Api(
                consumer_key=settings.CONSUMER_KEY_TWITTER,
                consumer_secret=settings.CONSUMER_SECRET_TWITTER,
                access_token_key=settings.TOKEN_TWITTER,
                access_token_secret=settings.SECRET_TOKEN_TWITTER,
            )
            tw.PostUpdate(
                u'hola %s, tienes un comentario anonimo %s (%s)' % (institute.alias, settings.URL+'/'+str(institute.id), comment.text[:25]+'...')
            )
        except:
            pass
        return redirect('/%s' % (institute.id))
    return redirect('/404')