from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

# ProfileImage model for storing all profile pictures
class ProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_images')
    image = models.ImageField(upload_to='profile_images/')
    status = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Pages(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog_images/')
    status = models.IntegerField()
    description = models.TextField()


        
    
    
