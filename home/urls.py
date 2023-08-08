"""
URL configuration for ToDoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.SigninSignup, name='Signin/Signup'),
    path('home', views.home, name='home'),
    path('home/tasks', views.tasks, name='tasks'),
    path('home/tasks/dashboard', views.dashboard, name='dashboard'),
    path('home/tasks/UpdateTask', views.UpdateTask, name='tasks'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('delete', views.handleDelete, name='handleDelete'),
    path('home/textutil',views.textutil, name="textutil"),
    path('home/textutil/analyze',views.textutilAnalyze, name="textutilAnalyze"),
    path("home/IcecreamHome", views.icecreamHome, name='icecreamHome'),
    path("home/IcecreamHome/about", views.icecreamAbout, name='icecreamAbout'),
    path("home/IcecreamHome/services", views.icecreamServices, name='icecreamServices'),
    path('home/IcecreamHome/contact', views.icecreamContact, name='icecreamContact'),
    path('home/CodeX', views.CodeXhome, name='CodeXhome'),
    path('home/CodeX/CodeXcontact', views.CodeXcontact, name='CodeXcontact'),
    path('home/CodeX/CodeXabout', views.CodeXabout, name='CodeXabout'),
    path('home/askAxel', views.chatBot, name='chatBot')
]
