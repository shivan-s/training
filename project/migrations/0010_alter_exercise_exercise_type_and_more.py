# Generated by Django 4.1.4 on 2022-12-20 01:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_historicalprogrammesession_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='exercise_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.exercisetype', verbose_name='exercise'),
        ),
        migrations.AlterField(
            model_name='historicalprogrammesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 20, 1, 56, 53, 776650, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='programmesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 20, 1, 56, 53, 776650, tzinfo=datetime.timezone.utc), verbose_name='date'),
        ),
    ]
