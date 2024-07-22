from django.urls import path
from .views import *

urlpatterns = [
    path('', profil, name='profil'),
    path('index/', index, name='index'),
    path('detail/<int:pk>', detail, name='detail'),
    path('qarz_delete/<int:pk>', qarz_delete, name='qarz_delete'),
    path('Xaydovchilar/', Xaydovchilar, name='Xaydovchilar'),
    path('car/<int:pk>', car, name='car'),
    path('payment/<int:pk>', payment, name='payment'),
    path('payment_edit/<int:pk>', payment_edit, name='payment_edit'),
    path('employee/', employee, name='employee'),
    path('avans/<int:pk>', avans, name='avans'),
    path('avans_edit/<int:pk>', avans_edit, name='avans_edit'),
    path('aftomabil/', aftomabil, name='aftomabil'),
]