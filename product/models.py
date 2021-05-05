from django.db import models

# Create your models here.
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    logo_image = models.CharField(max_length=255)

class Category(models.Model):
    category = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    manufacturer_id = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    weight = models.IntegerField()
    @property
    def price_per_kilo(self):
<<<<<<< HEAD
        return (self.price / self.weight) * 1000
=======
        return round(((self.price / self.weight) * 1000), 2)
>>>>>>> 49d66aef09e0e70565d6a9beba368adee583ff6e
    @property
    def first_image(self):
        return ProductGallery.objects.filter(product_id=self.id).first().image
    


class NutritionalInfo(models.Model):
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    carbs = models.FloatField()
    sugar = models.FloatField()
    fat = models.FloatField()
    protein = models.FloatField()

    @property
    def calories(self):
        return round(((self.carbs + self.protein) * 4 + self.fat * 9), 2)

class ProductGallery(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=255)
    def __str__(self):
        return self.image





