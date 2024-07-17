from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nomi = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    tg = models.CharField(max_length=50, null=True, blank=True)
    img = models.ImageField(upload_to='avatars/', null=True, blank=True)

    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'