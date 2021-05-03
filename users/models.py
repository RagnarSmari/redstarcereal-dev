from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Users(models.Model):
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    profile_pic = models.CharField(max_length=9999)

    def get_full_name(self):
        return self.first_name + self.last_name


    def __str__(self):
        return self.user_name


class TestTable(models.Model):
    test_name = models.CharField(max_length=100)
    test_char = models.CharField(max_length=100)