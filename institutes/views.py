from django.http import HttpResponse as response
from django.shortcuts import render_to_response as render, get_object_or_404 as get_or_404, redirect
from django.template.context import RequestContext as rc
from institutes.models import Institute
from comments.models import Comment

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
            image = request.FILES['image']
        )
        return redirect('/%s' % (institute.id))
    args = {}
    return render('create_institute.html', args, context_instance=rc(request))

def comment(request, institute):
    if request.POST:
        institute = get_or_404(Institute, pk=institute)
        comment = Comment.objects.create(
            text=request.POST['text']
        )
        institute.comments.add(comment)
        return redirect('/%s' % (institute.id))
    return redirect('/404')