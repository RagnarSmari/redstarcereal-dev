from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from django import forms
from django_countries.fields import CountryField
from .models import ContactInfo, PaymentInfo


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'last_name', 'email', 'street', 'house_number', 'city', 'country','postal_code']




class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields =['card_holder', 'cc_number', 'cc_expiry', 'cc_code']
