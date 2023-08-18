from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label = "First Name",required = True, max_length = 128)
    last_name = forms.CharField(label = "Last Name",required = False,max_length = 128)
    class Meta:
	    model = User
	    fields = ["username", "password1", "password2","first_name","last_name"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = "GitHub Username",required = True)
    class Meta:
        model = User
        fields = ['username',"password1"]