from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_user = models.NullBooleanField(default = True)
    is_stylist = models.NullBooleanField(default=False)
    latitude = models.DecimalField(max_digits = 9, decimal_places=6 , null=True)
    longitude = models.DecimalField(max_digits = 9, decimal_places=6, null=True, default=0)
    TypeofStylist = models.CharField(max_length = 100, null=True, default = "Cosmetologist")
    DateOfBirth = models.DateField(null=True, blank=True)
    Profile_Picture = models.ImageField(upload_to='media', null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class UserImages(models.Model):
    Date_Time = models.DateTimeField(auto_now_add = True)
    Author = models.ForeignKey(User, on_delete = models.CASCADE)







