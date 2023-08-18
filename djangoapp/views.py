import json
from djangoapp.models import Repositories
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import requests
from requests.exceptions import HTTPError,ConnectionError,Timeout,ReadTimeout,ConnectTimeout
from django.views.generic import TemplateView
from django.contrib import messages
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            # user.refresh_from_db()
            try:
                response=requests.get(f'https://api.github.com/users/{user.username}')
                response.raise_for_status()
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                pass
            else:
                try:
                    repolist=requests.get(f'https://api.github.com/users/{user.username}/repos')
                    repolist.raise_for_status()
                except(ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                    print("not working dude")
                else:
                    jsonlist=repolist.json()
                    print(jsonlist)
                    for files in jsonlist:
                        t=Repositories(repo=files['name'],stars=int(files['stargazers_count']))
                        t.user=user
                        t.save()
                        user.repos.add(t)
                    k=response.json()
                    user.profile.followers=k['followers']
                    user.profile.save()
                    login(request,user)
                    return redirect('explore')
                return redirect('explore')
    else:
        form = RegisterForm()
        args = {'form':form}
        return render(request,'register.html',args)
def home(request):
    if request.method == 'POST':
        form = LoginForm(data =request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)             
                return redirect('explore')
            else:
                messages.error(request,'username or password not correct')   
                return redirect('home')
        else:
            messages.error(request,'form is not in valid format')
            return redirect('home')

    else:
        form = LoginForm()
        return render(request,'home.html',{'form':form})

def explore(request):
    users=User.objects.all()
    context={'users':users}
    return render(request,'explore.html',context)

def refresh(request):
    c = request.user
    d = c.repos.all()
    d.delete()
    response=requests.get(f'https://api.github.com/users/{c.username}')
    k=response.json()
    z = requests.get(f'https://api.github.com/users/{c.username}/repos')
    jsonlist = z.json()
    for rep in jsonlist:
        t=Repositories(repo=rep['name'],stars=int(rep['stargazers_count']))
        t.user=c
        t.save()
        c.repos.add(t)
    c.profile.followers=k['followers']
    c.profile.save()
    context={'curruser':c}
    return profile(request,c.username)

def profile(request,name):
    curruser=User.objects.get(username=name)
    context={"curruser":curruser}
    return render(request,'profile.html',context)

def myprofile(request):
    return profile(request,request.user.username)
    
