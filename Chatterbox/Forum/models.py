import random

from django.db import models
from ckeditor.fields import RichTextField

class User(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False, help_text="Пользователь подтвержден через email.")
    verification_code = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Ads(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="ads")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='ads_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    ad = models.ForeignKey(Ads, on_delete= models.CASCADE, related_name="responses")
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    created_time = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик от {self.user.username} на объявление {self.ad.title}"


