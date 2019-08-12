from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
# Create your views here.
def home(request):

    races = Race.objects.all()

    form = RaceForm(request.POST)

    if form.is_valid():
        request.session['race'] = request.POST
        return HttpResponseRedirect('/classes')


    template = "home.html"
    return render(request, template, locals())

def classes(request):
    classes = Class_Base.objects.all()

    form = ClassBaseForm(request.POST)

    if form.is_valid():
        request.session['class'] = request.POST
        return HttpResponseRedirect('/bg')


    template = "classes.html"
    return render(request, template, locals())