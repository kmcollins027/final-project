from django.contrib import admin
from .models import User, Item, Category, Cart, Review

# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Review)
