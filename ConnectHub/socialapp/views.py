from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from .forms import *

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'socialapp/home.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = User.objects.get(username = username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page': page}
    return render(request, 'socialapp/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def signupUser(request):
    form = MyUserForm()

    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'socialapp/register.html', context)

