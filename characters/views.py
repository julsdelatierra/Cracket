#!/usr/bin/python
#encoding:utf-8
import re
from django.http import HttpResponse as response
from django.shortcuts import render_to_response as render, get_object_or_404 as get_or_404, redirect
from django.template.context import RequestContext as rc
from characters.models import Character
from institutes.models import Institute
from comments.models import Comment
from django.conf import settings
from tools import twitter

def index(request):
    args = {
        'characters':Character.objects.all()
    }
    return render('characters.html', args, context_instance=rc(request))

def view(request, character):
    character = get_or_404(Character, pk=character)
    i = Institute.objects.filter(characters__id=character.id)[0]
    args = {
        'character' : character,
        'institute' : i,
    }
    return render('view_character.html', args, context_instance=rc(request))

def create(request, institute):
    institute = get_or_404(Institute, pk=institute)
    if request.POST:
        character = Character.objects.create(
            name = request.POST['name'],
            alias = request.POST['alias'],
            image = request.FILES['image']
        )
        institute.characters.add(character)
        return redirect('/char/%s' % (character.id))
    args = {
        'institute': institute,
    }
    return render('create_character.html', args, context_instance=rc(request))

def comment(request, character):
    if request.POST:
        character = get_or_404(Character, pk=character)
        exp = ''
        for w in settings.UNAVAILABLE_WORDS:
            if exp is '':
                exp = w
            else:
                exp += '|'+w
        regexp = re.compile('('+exp+')+',re.UNICODE)
        if re.search(regexp,request.POST['text'].lower()):
            return redirect('/char/%s?unavailable=1' % (character.id))
        if character.comments.filter(text=request.POST['text']).count() > 0:
            return redirect('/char/%s?said=1' % (character.id))
        comment = Comment.objects.create(
            text=request.POST['text']
        )
        character.comments.add(comment)
        try:
            tw = twitter.Api(
                consumer_key=settings.CONSUMER_KEY_TWITTER,
                consumer_secret=settings.CONSUMER_SECRET_TWITTER,
                access_token_key=settings.TOKEN_TWITTER,
                access_token_secret=settings.SECRET_TOKEN_TWITTER,
            )
            tw.PostUpdate(
                u'hola %s, tienes un comentario anonimo %s (%s)' % (character.alias, settings.URL+'/char/'+str(character.id), comment.text[:25]+'...')
            )
        except:
            pass
        return redirect('/char/%s' % (character.id))
    return redirect('/404')
    