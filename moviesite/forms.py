from django import forms
from .models import Genre, Movie
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['views']
        labels = {
            "title": "Nomi",
            "description": "Tavsifi",
            "genre": "Janri",
            "image": "Rasm"
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Film nomini kiriting"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Film haqida qisqacha"
            }),
            "genre": forms.Select(attrs={
                "class": "form-select"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }