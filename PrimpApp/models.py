from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class AllUser(models.Model):
    PROFESSIONAL = 'P'
    PERSONAL = 'U'

    USER_TYPE_CHOICES = [
        (PERSONAL, 'Personal'),
        (PROFESSIONAL, 'Professional'),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key = True)
    BusinessName = models.CharField(max_length = 300, null = True, blank= True)
    address = models.CharField(max_length=5000, null = True, blank= True)
    city = models.CharField(max_length=100, null = True, blank= True)
    state = models.CharField(max_length=5000, null=True, blank=True)
    zip = models.DecimalField(max_digits=5,decimal_places=0, null = True, blank=True)
    lat = models.DecimalField(max_digits = 10, decimal_places=8 , null=True, blank = True,  default =0)
    lng = models.DecimalField(max_digits = 10, decimal_places=8, blank = True, null=True, default=0)
    DateOfBirth = models.DateField(null=True, blank=True)
    AccountType = models.CharField(max_length=1,choices=USER_TYPE_CHOICES)
    Profile_Picture = models.ImageField(upload_to='media', null=True, blank=True)
    TypeofStylist = models.CharField(max_length = 100, null=True, default = "Cosmetologist")

    def __str__(self):
        return f"(user:{self.user}, AccountType:{self.AccountType}, lat:{self.lat}, lng:{self.lng}) "


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

class ChatMessages(models.Model):
    Date_Time = models.DateTimeField(auto_now_add = True)
    Author = models.ForeignKey(User, on_delete = models.CASCADE)
    ChatMessages = models.CharField(max_length=3000, blank = False)







