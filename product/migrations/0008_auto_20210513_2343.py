# Generated by Django 3.2 on 2021-05-13 23:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210513_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='review',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
    ]
