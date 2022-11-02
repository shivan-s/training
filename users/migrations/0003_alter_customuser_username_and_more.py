# Generated by Django 4.1.3 on 2022-11-01 23:13

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_customuser_deleted_at_alter_customuser_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator()
                ],
                verbose_name="username",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcustomuser",
            name="username",
            field=models.CharField(
                db_index=True,
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator()
                ],
                verbose_name="username",
            ),
        ),
    ]
