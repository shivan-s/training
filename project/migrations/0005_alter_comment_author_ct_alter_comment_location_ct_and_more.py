# Generated by Django 4.1.3 on 2022-11-11 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('project', '0004_exerciseset_sets_historicalexerciseset_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author_ct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='contenttypes.contenttype', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='location_ct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='contenttypes.contenttype', verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='historicalcomment',
            name='author_ct',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.contenttype', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='historicalcomment',
            name='location_ct',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.contenttype', verbose_name='location'),
        ),
    ]
