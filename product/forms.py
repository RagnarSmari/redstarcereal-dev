from django import forms
from .models import Review

RATE_CHOICES = [
    (5, '5 stars'),
    (4, '4 stars'),
    (3, '3 stars'),
    (2, '2 stars'),
    (1, '1 star')
]

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)
    class Meta:
        model = Review
        fields = ['rating', 'title', 'review']

