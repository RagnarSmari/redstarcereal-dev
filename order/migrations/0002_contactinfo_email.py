# Generated by Django 3.2 on 2021-05-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='email',
            field=models.EmailField(default='helloworld@redstar.com', max_length=100),
            preserve_default=False,
        ),
    ]
