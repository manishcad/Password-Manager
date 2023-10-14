from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField
from django.contrib.auth.models import User
from .models import UserPassword

#class LoginForm(AuthenticationForm):
 #   username = UsernameField(label=("Your Username"),
 #                            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
 #   password=forms.CharField(label=("Your Password"),strip=False,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    class Meta:
        model=User
        fields=("username","email","password1","password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@company.com'
            }),
           }
        
class LoginForm(AuthenticationForm):
    username=forms.CharField(label=("Username"),widget=forms.TextInput(attrs={"class":"form-control",}))
    password=forms.CharField(label=("Username"),widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=("username","password1")



class UpdatePasswordForm(forms.ModelForm):
    class Meta:
        model = UserPassword
        fields = ['id', 'username', 'password', 'application_type', 'website_name', 'website_url', 'application_name',
                  'game_name', 'game_developer']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'password'
            }),
            'application_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'application type',
                'readonly': 'readonly',
            }),
            'website_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'website name',
            }),
            'website_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'website url',
            }),
            'application_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'application name',
            }),
            'game_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'game name',
            }),
            'game_developer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'game developer',
            }),
        }