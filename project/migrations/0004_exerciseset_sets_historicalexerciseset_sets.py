# Generated by Django 4.1.3 on 2022-11-11 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "project",
            "0003_remove_comment_project_com_content_e22fca_idx_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="exerciseset",
            name="sets",
            field=models.PositiveIntegerField(
                blank=True, default=1, verbose_name="sets"
            ),
        ),
        migrations.AddField(
            model_name="historicalexerciseset",
            name="sets",
            field=models.PositiveIntegerField(
                blank=True, default=1, verbose_name="sets"
            ),
        ),
    ]
