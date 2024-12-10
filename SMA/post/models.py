from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='nRosan.jpg')
    location = models.CharField(max_length=100, blank=True)
    email=models.EmailField(blank=True, max_length=254)


    def __str__(self):
        return self.user.username  # This accesses the 'username' attribute from the User model.


class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)


    def __str__(self):
        return self.user