from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']