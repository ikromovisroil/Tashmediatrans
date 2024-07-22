from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Aftomabil)
class AftomabilAdmin(admin.ModelAdmin):
    list_display = ('id','nomi','raqami','summa','status',)
    list_filter = ('status',)
    search_fields = ('nomi','raqami',)

@admin.register(Istemolchi)
class IstemolchiAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','pazivnoy','tel','status',)
    list_filter = ('aftomabil','status',)
    search_fields = ('full_name','pazivnoy','tel',)
    
@admin.register(Qarz)
class QarzAdmin(admin.ModelAdmin):
    list_display = ('id','istemolchi','summa','status','date_creat','date_delete',)
    list_filter = ('status',)
    search_fields = ('summa',)
    


@admin.register(Tolov)
class TolovAdmin(admin.ModelAdmin):
    list_display = ('id', 'istemolchi', 'naxt','karta','date', 'date_creat', 'date_edit',)
    list_filter = ('istemolchi__status','date','date_creat',)
    search_fields = ('istemolchi__full_name', 'istemolchi__pazivnoy',)
    
    
@admin.register(Xodim)
class XodimAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','tel','oylik','status',)
    list_filter = ('status',)
    search_fields = ('full_name','tel',)
    
@admin.register(Maosh)
class MaoshAdmin(admin.ModelAdmin):
    list_display = ('id', 'xodim_full_name', 'summa', 'date', 'date_creat','date_edit',)
    list_filter = ('xodim__full_name',)
    search_fields = ('xodim__full_name',)

    def xodim_full_name(self, obj):
        return obj.xodim.full_name
    xodim_full_name.short_description = 'Xodim'
    
@admin.register(Car_cost)
class Car_costAdmin(admin.ModelAdmin):
    list_display = ('id', 'aftomabil','date', 'summa',)
    list_filter = ('aftomabil__nomi',)
    search_fields = ('aftomabil__nomi',)

