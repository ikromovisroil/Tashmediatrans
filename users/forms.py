from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import *


class Userloginform(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password',)


class Userregisterform(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2',)








