from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class MyAuthenticationForm(AuthenticationForm):
    pass


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')