from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Image(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='hello.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username}\'s profile'

class Search(models.Model):
    keyword = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'keyword',)


