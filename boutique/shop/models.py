from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.core.validators import MinValueValidator
from datetime import datetime

class User(AbstractUser):
    image = models.ImageField(upload_to='images', default="No Image")

class Item(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    price = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    categories = models.ManyToManyField('Category', blank=True, related_name='items')
    image = models.ImageField(upload_to='images', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='shopping_cart')
    date_ordered = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart', default=None)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def get_total(self):
        total = self.item.price * self.quantity
        return total

    def get_image_url(self):
        return self.item.image

    def get_title(self):
        return self.item.title

    def get_price(self):
        return self.item.price

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    content = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

