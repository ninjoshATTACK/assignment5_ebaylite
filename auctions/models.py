from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files import File

# model for Users
class User(AbstractUser):
    pass

# model for Categories
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

# model for auction listings
class Listing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.TextField()
    startbid = models.IntegerField()
    available = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    photo = models.ImageField(upload_to='images/', blank=True)
    photo_url = models.URLField()
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="seller")

    # got this from the professor's movies example
    def save(self, *args, **kwargs):
        super(Listing, self).save(*args, **kwargs)
        if self.photo_url and not self.photo:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.photo_url).read())
            img_temp.flush()
            self.photo.save(f"image_{self.pk}", File(img_temp))
            super(Listing, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} {self.title}'

# model for bids  [NOT CORRECT]
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing", default=None)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", default=None)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

# model for comments  [NOT CORRECT]
class Comment(models.Model):
    content = models.CharField(max_length=9999, default='')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=None)

    def __str__(self):
        return f'{self.title}'