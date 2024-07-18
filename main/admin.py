from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Aftomabil)
class AftomabilAdmin(admin.ModelAdmin):
    list_display = ('id','nomi','raqami','summa','status',)
    list_filter = ('status',)
    search_fields = ('nomi','raqami',)

class QarzAdmin(admin.TabularInline):
    model = Qarz
    extra = 1

class TolovAdmin(admin.TabularInline):
    model = Tolov
    extra = 1

@admin.register(Istemolchi)
class IstemolchiAdmin(admin.ModelAdmin):
    inlines = (QarzAdmin,TolovAdmin,)
    list_display = ('id','full_name','pazivnoy','tel','status',)
    list_filter = ('aftomabil','status',)
    search_fields = ('full_name','pazivnoy','tel',)

