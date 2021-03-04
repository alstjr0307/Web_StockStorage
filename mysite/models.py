from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    username=models.CharField(max_length=10, unique=True)
    first_name=models.CharField(max_length=6, unique=True)
    email=models.charField(unique=True)
    is_active = models.BooleanField(default=False)
    
    get
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

