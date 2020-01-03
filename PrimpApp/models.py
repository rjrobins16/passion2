from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length = 300, null = True)
    is_stylist = models.BooleanField(blank=True, default=False)
    latitude = models.DecimalField(max_digits = 10, decimal_places=8 , null=True, default=35.148272)
    longitude = models.DecimalField(max_digits = 10, decimal_places=8, null=True, default=-90.1108723)
    TypeofStylist = models.CharField(max_length = 100, null=True, default = "Cosmetologist")
    DateOfBirth = models.DateField(null=True, blank=True)
    Profile_Picture = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return f"(user: {self.user}, Title:{self.title}, is_stylist:{self.is_stylist},latitude:{self.latitude} " \
               f" longitude:{self.longitude}, TypeofStylist:{self.TypeofStylist}, DateOfBirth:{self.DateOfBirth})"

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







