from django import forms
from django.forms import ModelForm
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
