from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']