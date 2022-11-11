# Generated by Django 4.1.3 on 2022-11-06 21:49

import sorl.thumbnail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_customuser_username_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="avatar",
            field=sorl.thumbnail.fields.ImageField(
                blank=True, null=True, upload_to="images/"
            ),
        ),
        migrations.AddField(
            model_name="historicalcustomuser",
            name="avatar",
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
