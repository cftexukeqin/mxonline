# Generated by Django 2.0.5 on 2018-11-17 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20181117_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='avatar',
            new_name='image',
        ),
    ]