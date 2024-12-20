from django.contrib import admin
from .models import UserProfile,Post,LikePost,FollowerCount

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowerCount)