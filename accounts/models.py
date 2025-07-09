from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def user_profile_image_path(instance, filename):
    """Generate upload path for user profile images"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename as username + extension
    filename = f"{instance.user.username}_profile.{ext}"
    # Return the upload path
    return os.path.join('profile_pictures', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=user_profile_image_path,
        null=True,
        blank=True,
        help_text="Upload your profile picture"
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Create profile automatically when user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()