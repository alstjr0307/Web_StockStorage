from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

<<<<<<< HEAD
class User(models.Model):
    
    is_active = models.BooleanField(default=False)
=======
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
>>>>>>> f64f7a8d0b9819a4a2822b323c99e833a7085ee2

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()