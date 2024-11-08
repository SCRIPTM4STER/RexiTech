from django.db import models
from .models_product import Product, Category
from .models_order import Cart, CartItem, Order
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        default='default_profile_picture.jpg',  # Set your default image path here
        null=True, 
        blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create or update a user profile whenever a user is created or saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, email=instance.email)
    else:
        instance.userprofile.save()