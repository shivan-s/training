# Generated by Django 4.1.3 on 2022-11-12 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0006_remove_exercise_weight_unit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exerciseset",
            name="weight",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="weight",
            ),
        ),
        migrations.AlterField(
            model_name="exerciseset",
            name="weight_unit",
            field=models.CharField(
                choices=[
                    ("KG", "kilograms (kg)"),
                    ("LB", "pounds (lbs)"),
                    ("PE", "percentage (%)"),
                ],
                default="KG",
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalexerciseset",
            name="weight",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="weight",
            ),
        ),
        migrations.AlterField(
            model_name="historicalexerciseset",
            name="weight_unit",
            field=models.CharField(
                choices=[
                    ("KG", "kilograms (kg)"),
                    ("LB", "pounds (lbs)"),
                    ("PE", "percentage (%)"),
                ],
                default="KG",
                max_length=2,
                null=True,
            ),
        ),
    ]
