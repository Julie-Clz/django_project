from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from easy_thumbnails.fields import ThumbnailerImageField


CROP_SETTINGS = {'size': (300, 300), 'crop': 'smart'}

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    image = ThumbnailerImageField(default='profile_pics/default.jpg', upload_to='profile_pics', resize_source=CROP_SETTINGS)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    