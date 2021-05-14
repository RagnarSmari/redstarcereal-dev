from django.db import models
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from product import models as product_models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class ContactInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    country = CountryField()
    postal_code = models.IntegerField()
    archived = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, blank=True, null=True)

class PaymentInfo(models.Model): # þetta 3 party dummy
    card_holder = models.CharField(max_length=255)
    cc_number = CardNumberField()
    cc_expiry = CardExpiryField()
    cc_code = SecurityCodeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, blank=True, null=True)
    archived = models.BooleanField(default=False)

class Order(models.Model):
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE)
    payment_info = models.OneToOneField(PaymentInfo, on_delete=models.CASCADE)
    total_price = models.FloatField()


class OrderRow(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    row_price = models.FloatField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    @property
    def price(self):
        return self.product.price * self.amount

    @property
    def name(self):
        return product_models.Product.objects.get(id=self.product).name

    class Meta:
        unique_together = ['user', 'product',]
