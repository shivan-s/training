# Generated by Django 4.1.3 on 2022-12-01 00:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 0, 22, 45, 800875, tzinfo=datetime.timezone.utc), verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 0, 22, 45, 800875, tzinfo=datetime.timezone.utc), verbose_name='date joined'),
        ),
    ]
