from django.contrib import admin

from .models import Comment, Food, FoodType

admin.site.register([Food, FoodType, Comment])
