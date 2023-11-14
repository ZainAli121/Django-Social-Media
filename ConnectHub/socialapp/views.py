from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'socialapp/home.html', context)