from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "placeholder": "Username",
        "id": "username",
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "id": "password",
    }))

class RegisterationFrom(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "placeholder": "Username",
        "id": "username",
    }))

    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "placeholder": "Email",
        "id": "email",
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "id": "password1",
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password reply",
        "id": "password2",
    }))

    class Meta:
        model = User
        fields = ('username', 'email')