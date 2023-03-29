"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from WebTest.views import *
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('',LoginPage, name='loginpage'),
    path('main',Main,name='main'),
    path('login/',LogIn,name='login'),
    path('logout/',LogOut,name='logout'),
    path('testInfo/<int:idTest>',TestInfo,name='testInfo'),
    path('test/<int:idTest>',Test,name='test'),
    path('resultcreate',ResultCreate,name='resultcreate'),
    path('resultUser/<int:idResult>',ResultUser,name='resultUser'),

    path('questionAdmin/<int:idQuestion>',QuestionAdmin,name='questionAdmin'),
    path('resultAdmin/<int:idResult>',ResultAdmin,name='resultAdmin'),
    path('testAdmin/<int:idTest>',TestAdmin,name='testAdmin'),

    
    
    
]
