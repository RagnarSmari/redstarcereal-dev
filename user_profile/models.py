from django.db import models
from django.contrib.auth.models import User
from 
# Create your models here.

class Image(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='hello.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username}\'s profile'


