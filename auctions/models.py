from django.contrib.auth.models import AbstractUser
from django.db import models

# model for Users
class User(AbstractUser):
    pass

# model for auction listings
class Listing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=100)
    startbid = models.ImageField()

    def __str__(self):
        return f'{self.title}'

# model for bids
class Bid(models.Model):


# model for comments
class Comment(models.Model):
    pass