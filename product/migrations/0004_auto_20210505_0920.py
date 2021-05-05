# Generated by Django 3.2 on 2021-05-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210504_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=390),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]
