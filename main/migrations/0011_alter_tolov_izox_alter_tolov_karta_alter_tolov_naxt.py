# Generated by Django 5.0.7 on 2024-07-28 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_car_cost_date_creat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tolov',
            name='izox',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='tolov',
            name='karta',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='tolov',
            name='naxt',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
