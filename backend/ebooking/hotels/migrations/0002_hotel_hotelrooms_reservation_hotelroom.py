# Generated by Django 4.1.5 on 2023-01-07 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotelRooms',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotelroom'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='hotelRoom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotelroom'),
        ),
    ]
