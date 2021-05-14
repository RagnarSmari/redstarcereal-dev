from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
        return round(((self.price / self.weight) * 1000), 2)

    @property
    def first_image(self):
        return ProductGallery.objects.filter(product_id=self.id).first().image

    @property
    def rating(self):
        if Review.objects.filter(product=self.id).exists():
            return round(Review.objects.filter(product=self.id).aggregate(models.Avg('rating'))['rating__avg'], 1)
        else:
            return 5

    @property
    def rating_count(self):
        if Review.objects.filter(product=self.id).exists():
            return Review.objects.filter(product=self.id).aggregate(models.Count('rating'))['rating__count']
        else:
            return 0

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

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=50)
    review = models.TextField()
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']






