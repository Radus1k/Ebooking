# Generated by Django 4.1.5 on 2023-04-11 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='hotel/')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('rooms', models.PositiveIntegerField(default=1)),
                ('floors', models.PositiveIntegerField()),
                ('parking_places', models.PositiveIntegerField()),
                ('restaurant_places', models.PositiveIntegerField()),
                ('has_wifi', models.BooleanField()),
                ('has_breakfast', models.BooleanField()),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotels.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='hotelroom/')),
                ('beds', models.IntegerField()),
                ('has_terrace', models.BooleanField(default=True)),
                ('has_kitchen', models.BooleanField(default=True)),
                ('has_tv', models.BooleanField(default=True)),
                ('has_fridge', models.BooleanField(default=True)),
                ('floor_no', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField(default=100, null=True)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotelroom', to='hotels.hotel')),
            ],
            options={
                'db_table': 'hotelroom',
            },
        ),
    ]
