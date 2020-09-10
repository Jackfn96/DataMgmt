from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class UserType(models.Model):
    user_type = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.user_type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    user_choices = (
        ('Individual User', 'Individual User'),
        ('Organisation', 'Organisation'),
    )
    user_type = models.CharField(max_length=100, choices=user_choices, default='Individual User', null=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
