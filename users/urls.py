from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('', login, name='login'),
]
