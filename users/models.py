from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    follows = models.ManyToManyField("self", related_name='followed_by', symmetrical=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'







