from django.http import HttpResponse as response
from django.shortcuts import render_to_response as render, get_object_or_404 as get_or_404, redirect
from django.template.context import RequestContext as rc
from comments.models import Comment
from characters.models import Character

def create(request, character):
    if request.POST:
        character = get_or_404(Character, pk=character)
        Comment.objects.create(
            character=character,
            text=request.POST['text']
        )
        return redirect('/char/%s' % (character.id))
    return redirect('/404')
        
