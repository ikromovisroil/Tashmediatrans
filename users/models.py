from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Category(models.Model):
    nomi = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)

    
    def __str__(self):
        return self.nomi
    
    class Meta:
        db_table = 'category'
 

class User(AbstractUser):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    nomi = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    tg = models.CharField(max_length=50, null=True, blank=True)
    img = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'