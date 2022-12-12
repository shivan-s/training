# Generated by Django 4.1.3 on 2022-12-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_programmesession_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='read',
            field=models.BooleanField(default=False, verbose_name='message read'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='read',
            field=models.BooleanField(default=False, verbose_name='message read'),
        ),
        migrations.AlterField(
            model_name='exerciseset',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('KG', 'kg'), ('LBS', 'lbs'), ('PER', '%'), ('RPE', 'RPE')], default='KG', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='historicalexerciseset',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('KG', 'kg'), ('LBS', 'lbs'), ('PER', '%'), ('RPE', 'RPE')], default='KG', max_length=3, null=True),
        ),
    ]