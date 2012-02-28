from django.http import HttpResponse as response
from django.shortcuts import render_to_response as render, get_object_or_404 as get_or_404, redirect
from django.template.context import RequestContext as rc
from characters.models import Character
from institutes.models import Institute
from comments.models import Comment

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
        comment = Comment.objects.create(
            text=request.POST['text']
        )
        character.comments.add(comment)
        return redirect('/char/%s' % (character.id))
    return redirect('/404')
    