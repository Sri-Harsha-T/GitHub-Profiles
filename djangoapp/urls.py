from os import name
from django.urls import path
from . import views
from .views import explore, refresh, register,home,profile,myprofile

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.home,name='login'),
    path('explore/',views.explore,name='explore'),
    path('profile/',views.myprofile,name='profile'),
    path('refresh/',views.refresh,name='refresh'),
    path('profiles/<str:name>',views.profile,name='profiles'),
]