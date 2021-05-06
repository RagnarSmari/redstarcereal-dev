from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from django import forms

class ContactInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    street = forms.CharField(max_length=100)
    house_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()

class PaymentForm(forms.Form):
    card_holder = forms.CharField(max_length=100)
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')