from django.db import models
from django.contrib.auth.models import User
from pillow import
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=default.jpg, upload_to ='media/profile_pics')