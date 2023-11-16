from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class MyUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['owner']