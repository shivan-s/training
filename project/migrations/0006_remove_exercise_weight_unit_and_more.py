# Generated by Django 4.1.3 on 2022-11-12 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        (
            "project",
            "0005_alter_comment_author_ct_alter_comment_location_ct_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exercise",
            name="weight_unit",
        ),
        migrations.RemoveField(
            model_name="historicalexercise",
            name="weight_unit",
        ),
        migrations.AddField(
            model_name="exerciseset",
            name="weight_unit",
            field=models.CharField(
                choices=[
                    ("KG", "kilograms"),
                    ("LB", "pounds"),
                    ("PE", "percentage"),
                ],
                default="KG",
                max_length=2,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalexerciseset",
            name="weight_unit",
            field=models.CharField(
                choices=[
                    ("KG", "kilograms"),
                    ("LB", "pounds"),
                    ("PE", "percentage"),
                ],
                default="KG",
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="author_ct",
            field=models.ForeignKey(
                limit_choices_to={
                    "app_label": "project",
                    "model__in": ("coach", "athlete"),
                },
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author",
                to="contenttypes.contenttype",
                verbose_name="author",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="location_ct",
            field=models.ForeignKey(
                limit_choices_to={"app_label": "project"},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location",
                to="contenttypes.contenttype",
                verbose_name="location",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcomment",
            name="author_ct",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={
                    "app_label": "project",
                    "model__in": ("coach", "athlete"),
                },
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="contenttypes.contenttype",
                verbose_name="author",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcomment",
            name="location_ct",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={"app_label": "project"},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="contenttypes.contenttype",
                verbose_name="location",
            ),
        ),
        migrations.AlterField(
            model_name="historicalteam",
            name="description",
            field=models.TextField(verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="historicalteam",
            name="name",
            field=models.CharField(
                db_index=True, max_length=25, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="description",
            field=models.TextField(verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="team",
            name="name",
            field=models.CharField(
                max_length=25, unique=True, verbose_name="name"
            ),
        ),
    ]
