from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileRegisterForm(forms.ModelForm):
    dp = forms.ImageField(label='set your profile image', required=False)
    Bio = forms.CharField(max_length=5000, label='write about yourself', required=False)

    class Meta:
        model = Profile
        fields = ['dp', 'bio']


class ProfileUpdateForm(forms.ModelForm):
    dp = forms.ImageField(label='Set your profile image', required=False)

    class Meta:
        model = Profile
        fields = ['dp', 'bio']


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']
