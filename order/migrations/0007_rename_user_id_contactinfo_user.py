# Generated by Django 3.2 on 2021-05-13 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_contactinfo_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactinfo',
            old_name='user_id',
            new_name='user',
        ),
    ]
