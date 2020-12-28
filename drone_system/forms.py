from django import forms
from django.forms import ModelForm
from user_system.models import users
from .models import drones


class BookForm(ModelForm):
    class Meta:
        model = drones
        fields = ['origin', 'destination']
        widgets = {
            'origin': forms.Select(
                attrs={
                    'class': 'custom-select my-1 mr-sm-2',
                },
            ),
            'destination': forms.Select(
                attrs={
                    'class': 'custom-select my-1 mr-sm-2',
                },
            )
        }

    def save(self, commit=True):
        return super(BookForm, self).save(commit=commit)


class FutureBook(ModelForm):
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Time(Format: HH:MM in 24 hour notation)'}))

    class Meta:
        model = drones
        fields = ['origin', 'destination']
        widgets = {
            'origin': forms.Select(
                attrs={
                    'class': 'custom-select my-1 mr-sm-2',
                },
            ),
            'destination': forms.Select(
                attrs={
                    'class': 'custom-select my-1 mr-sm-2',
                },
            )
        }

    def save(self, commit=True):
        return super(FutureBook, self).save(commit=commit)


class ChangePassword(ModelForm):
    new_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    repeat_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = users
        fields = ['password']
        widgets = {
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Current Password',
                }
            ),
        }


class DeleteAccount(ModelForm):
    class Meta:
        model = users
        fields = ['password']
        widgets = {
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Password',
                }
            ),
        }
