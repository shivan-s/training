# Generated by Django 4.1.3 on 2022-11-16 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_exerciseset_weight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseset',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('KG', 'kilograms (kg)'), ('LBS', 'pounds (lbs)'), ('PER', 'percentage (%)'), ('RPE', 'rate of perceived exertion (RPE)')], default='KG', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='historicalexerciseset',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('KG', 'kilograms (kg)'), ('LBS', 'pounds (lbs)'), ('PER', 'percentage (%)'), ('RPE', 'rate of perceived exertion (RPE)')], default='KG', max_length=3, null=True),
        ),
    ]
