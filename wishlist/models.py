from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)

class Notes(models.Model):
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

