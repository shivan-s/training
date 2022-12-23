# Generated by Django 4.1.4 on 2022-12-19 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_historicalprogrammesession_is_draft_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalprogrammesession',
            name='is_draft',
        ),
        migrations.RemoveField(
            model_name='programmesession',
            name='is_draft',
        ),
        migrations.AlterField(
            model_name='historicalprogrammesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 19, 5, 17, 21, 52747, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='programmesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 19, 5, 17, 21, 52747, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
    ]