from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=50)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, default=1)
    # category = models.ForeignKey(Category, on_delete=CASCADE, default=1)

    def __str__(self):
        return f"{self.title}: '{self.description[:50] if (len(self.description) > 50) else self.description}' starting_bid: {self.starting_bid}"

class Bid:
    pass

class Comment:
    pass

