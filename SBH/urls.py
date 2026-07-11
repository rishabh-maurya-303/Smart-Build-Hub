"""
URL configuration for SBH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from sbhapp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('projects/',views.projects,name='projects'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('aboutdev/',views.aboutdev,name='aboutdev'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminapp/',include('adminapp.adminappurls')),       #this file will contains the adminapp
    path('homeowner/',include('homeownerapp.hurls')),        #this file will contains the homeownerapp 
    path('contractor/',include('contractorapp.curls')),      #this file will contains the contractorapp
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)