from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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

@login_required(login_url='login')
def createPost(request):
    form = CreatePost()
    tags = Tag.objects.all()

    if request.method == 'POST':
        # tag_name = request.POST.get('tag')
        # tag, created = Tag.objects.get_or_create(name = tag_name)
        # Post.objects.create(
        #     owner = request.user,
        #     tag = tag,
        #     desc = request.POST.get('desc'),
        #     image = request.POST.get('image')
        # )
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('home')

    context = {'form': form, 'tags': tags}
    return render(request, 'socialapp/create-post.html', context)


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    tags = Tag.objects.all()

    if request.user != post.owner:
        return HttpResponse("You are not owner of this post!")

    form = CreatePost(instance=post)

    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form ,'tags': tags}
    return render(request, 'socialapp/create-post.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'socialapp/delete.html', {'obj': post})


def profile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    context = {'user': user, 'posts': posts}
    return render(request, 'socialapp/userProfile.html', context)


@login_required(login_url='login')
def editProfile(request, pk):
    user = request.user
    form = CustomUserProfile(instance=user)
    if request.method == 'POST':
        form = CustomUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    
    context = {'form': form}
    return render(request, 'socialapp/edit-user.html', context)

@login_required(login_url='login')
def editBio(request, pk):
    user = request.user
    form = CustomUserBio(instance=user)
    if request.method == 'POST':
        form = CustomUserBio(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    
    context = {'form': form}
    return render(request, 'socialapp/edit-user.html', context)

