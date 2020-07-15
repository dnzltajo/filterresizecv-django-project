from django import forms
from .models import Picture

class PostForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['img']