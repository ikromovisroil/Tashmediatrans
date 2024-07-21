from django.db import models
from users.models import User
# Create your models here.


class Aftomabil(models.Model):
    nomi = models.CharField(max_length=100,null=True, blank=True)
    raqami = models.CharField(max_length=20,null=True, blank=True)
    summa = models.PositiveIntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return self.nomi
    
    class Meta:
        db_table = 'aftomabil'



class Istemolchi(models.Model):
    aftomabil = models.ForeignKey(Aftomabil, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    pazivnoy = models.CharField(max_length=20)
    tel = models.CharField(max_length=20,null=True)
    status = models.BooleanField(default=False)
    aktiv = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'istemolchi'

class Qarz(models.Model):
    summa = models.PositiveIntegerField()
    istemolchi = models.ForeignKey(Istemolchi, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    date_creat = models.DateField(auto_now_add=True)
    date_delete = models.DateField(auto_now=True)

    
    def __str__(self):
        return self.author.username
    
    class Meta:
        db_table = 'qarz'


class Tolov(models.Model):
    naxt = models.PositiveIntegerField(null=True, blank=True)
    karta = models.PositiveIntegerField(null=True, blank=True)
    izox = models.TextField(null=True, blank=True)
    istemolchi = models.ForeignKey(Istemolchi, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    date_creat = models.DateField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.author.username
    
    class Meta:
        db_table = 'tolov'


class Xodim(models.Model):
    full_name = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True)
    oylik = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'xodim'


class Maosh(models.Model):
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE, null=True)
    summa = models.PositiveIntegerField()
    izox = models.TextField(null=True, blank=True)
    date = models.DateField()
    date_creat = models.DateField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.xodim.full_name
    
    class Meta:
        db_table = 'maosh'