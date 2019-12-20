from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """class for user registration
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='picture/', default='default.jpg')

    def __str__(self):
        return self.user.username
