from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['first_name','last_name','username','email']

class Profile(forms.ModelForm):
    class Meta:
        model=profile
        fields = ['image']