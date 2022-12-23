# Generated by Django 4.1.4 on 2022-12-19 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_remove_historicalprogrammesession_is_draft_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprogrammesession',
            name='published',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='published'),
        ),
        migrations.AddField(
            model_name='programmesession',
            name='published',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='historicalprogrammesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 19, 5, 20, 23, 37831, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='programmesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 19, 5, 20, 23, 37831, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
    ]