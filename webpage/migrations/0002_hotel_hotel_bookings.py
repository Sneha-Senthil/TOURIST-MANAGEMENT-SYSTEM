# Generated by Django 5.0 on 2023-12-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=1)),
                ('location', models.CharField(max_length=25)),
                ('room_2b_available', models.IntegerField()),
                ('room_2b_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('room_3b_available', models.IntegerField()),
                ('room_3b_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('food_price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel_Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('food', models.CharField(max_length=5)),
                ('room_type', models.CharField(max_length=7)),
                ('room_count', models.IntegerField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
