from django.urls import path
from . import  views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.signupUser, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    
]