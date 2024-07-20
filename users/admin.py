from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','nomi','status',)
    list_filter = ('status',)
    search_fields = ('nomi',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','first_name','last_name','nomi','category','is_staff',)
    list_filter = ('is_staff',)
    search_fields = ('username','nomi','first_name','last_name','tel',)
