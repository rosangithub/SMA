from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='nRosan.jpg')
    location = models.CharField(max_length=100, blank=True)
    email=models.EmailField(blank=True, max_length=254)


    def __str__(self):
        return self.user.username  # This accesses the 'username' attribute from the User model.
