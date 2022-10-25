from django.contrib import admin

# Register your models here.
from .models import Category, Listing

admin.site.register(Category)
admin.site.register(Listing)