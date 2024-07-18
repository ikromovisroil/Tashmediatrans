from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','first_name','last_name','nomi','is_staff',)
    list_filter = ('is_staff',)
    search_fields = ('username','nomi','first_name','last_name','tel',)
