from django import forms
from django.forms import ModelForm
from .models import users


class RegisterForm(ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Password',
                }
            ),
        }

    def clean_username(self):
        username = ((self.cleaned_data['username']).lower()).capitalize()
        return username


class LoginForm(ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Password'
                }
            ),
        }

    def clean_username(self):
        username = ((self.cleaned_data['username']).lower()).capitalize()
        return username
